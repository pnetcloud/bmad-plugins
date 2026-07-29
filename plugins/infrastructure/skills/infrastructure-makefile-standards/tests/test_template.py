from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).parents[1]
TEMPLATE = SKILL_DIR / "Makefile.template"


@unittest.skipUnless(shutil.which("make"), "GNU Make is required")
class TemplateTests(unittest.TestCase):
    def run_make(
        self, workdir: Path, *args: str, check: bool = True
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["make", "-f", str(workdir / "Makefile"), *args],
            cwd=workdir,
            check=check,
            capture_output=True,
            text=True,
        )

    def make_project(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        tempdir = tempfile.TemporaryDirectory()
        root = Path(tempdir.name)
        shutil.copyfile(TEMPLATE, root / "Makefile")
        return tempdir, root

    def test_help_lists_each_public_target_once(self) -> None:
        tempdir, root = self.make_project()
        self.addCleanup(tempdir.cleanup)

        result = self.run_make(root, "help")
        targets = [line.split()[0] for line in result.stdout.splitlines()]

        expected = {
            "help",
            "config",
            "up",
            "down",
            "restart",
            "logs",
            "status",
            "watch",
            "test",
            "lint",
            "format",
            "check",
            "build",
            "validate",
            "clean",
            "info",
            "version",
        }
        self.assertEqual(expected, set(targets))
        self.assertEqual(len(targets), len(set(targets)))

    def test_help_discovers_documented_project_target(self) -> None:
        tempdir, root = self.make_project()
        self.addCleanup(tempdir.cleanup)
        (root / "project.mk").write_text(
            ".PHONY: smoke\n"
            "smoke: ## Quality: Run the smoke check\n"
            "\t@printf '%s\\n' smoke\n",
            encoding="utf-8",
        )

        result = self.run_make(root, "help")

        self.assertIn("smoke", result.stdout)
        self.assertIn("Quality: Run the smoke check", result.stdout)

    def test_missing_project_command_fails_clearly(self) -> None:
        tempdir, root = self.make_project()
        self.addCleanup(tempdir.cleanup)

        result = self.run_make(root, "test", check=False)

        self.assertEqual(2, result.returncode)
        self.assertIn("CMD_TEST is not configured", result.stdout)

    def test_quality_target_is_non_interactive(self) -> None:
        tempdir, root = self.make_project()
        self.addCleanup(tempdir.cleanup)

        result = self.run_make(
            root,
            "--dry-run",
            "test",
            "COMPOSE=printf compose",
            "CMD_TEST=printf test",
        )

        self.assertIn("exec -T", result.stdout)

    def test_clean_rejects_hidden_paths_without_deleting_them(self) -> None:
        tempdir, root = self.make_project()
        self.addCleanup(tempdir.cleanup)
        protected = root / ".protected"
        protected.mkdir()

        result = self.run_make(root, "clean", "BUILD_DIR=.protected", check=False)

        self.assertEqual(2, result.returncode)
        self.assertTrue(protected.is_dir())
        self.assertIn("unsafe BUILD_DIR shape", result.stdout)

    def test_clean_rejects_path_outside_allowlist(self) -> None:
        tempdir, root = self.make_project()
        self.addCleanup(tempdir.cleanup)
        protected = root / "protected-output"
        protected.mkdir()

        result = self.run_make(
            root, "clean", "BUILD_DIR=protected-output", check=False
        )

        self.assertEqual(2, result.returncode)
        self.assertTrue(protected.is_dir())
        self.assertIn("outside SAFE_CLEAN_DIRS", result.stdout)

    def test_clean_rejects_unsafe_path_even_when_allowlisted(self) -> None:
        tempdir, root = self.make_project()
        self.addCleanup(tempdir.cleanup)

        result = self.run_make(
            root,
            "clean",
            "BUILD_DIR=/",
            "SAFE_CLEAN_DIRS=/",
            check=False,
        )

        self.assertEqual(2, result.returncode)
        self.assertIn("unsafe BUILD_DIR shape", result.stdout)

    def test_clean_removes_only_the_named_top_level_output(self) -> None:
        tempdir, root = self.make_project()
        self.addCleanup(tempdir.cleanup)
        output = root / "build-output"
        output.mkdir()
        (output / "artifact").write_text("generated", encoding="utf-8")
        sibling = root / "keep"
        sibling.write_text("source", encoding="utf-8")

        self.run_make(
            root,
            "clean",
            "BUILD_DIR=build-output",
            "SAFE_CLEAN_DIRS=build-output",
        )

        self.assertFalse(output.exists())
        self.assertEqual("source", sibling.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
