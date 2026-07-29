from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE = SKILL_DIR / "Makefile.template"


@unittest.skipUnless(shutil.which("make"), "GNU Make is not installed")
class MakefileTemplateTests(unittest.TestCase):
    GROUPS = {
        "Setup & Config": ("up", "down", "restart"),
        "Development": ("watch",),
        "Quality": ("test", "lint", "format", "check"),
        "Build & Deploy": ("build", "deploy", "release", "publish"),
        "Maintenance": ("clean", "clean-all"),
        "Logs & Info": ("logs", "status", "info", "version"),
    }

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        shutil.copy2(TEMPLATE, self.root / TEMPLATE.name)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_make(self, *targets: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["make", "-f", TEMPLATE.name, *targets],
            cwd=self.root,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_help_lists_annotated_targets_in_groups(self) -> None:
        result = self.run_make("help")

        self.assertEqual(0, result.returncode, result.stderr)
        output = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout)
        positions = {
            heading: output.index(heading) for heading in self.GROUPS
        }
        ordered_headings = list(self.GROUPS)

        for index, heading in enumerate(ordered_headings):
            start = positions[heading]
            end = (
                positions[ordered_headings[index + 1]]
                if index + 1 < len(ordered_headings)
                else len(output)
            )
            section = output[start:end]
            for target in self.GROUPS[heading]:
                with self.subTest(heading=heading, target=target):
                    self.assertRegex(
                        section,
                        rf"(?m)^\s+{re.escape(target)}\s",
                    )

    def test_external_and_cleanup_placeholders_fail_closed(self) -> None:
        for target in ("deploy", "release", "publish", "clean", "clean-all"):
            with self.subTest(target=target):
                result = self.run_make(target)
                self.assertNotEqual(0, result.returncode)
                self.assertIn("project.mk", result.stderr)

    def test_project_file_overrides_variables_recipes_and_help(self) -> None:
        (self.root / "project.mk").write_text(
            "\n".join(
                [
                    "PROJECT := synthetic-service",
                    "CMD_CLEAN := printf '%s\\n' 'override clean'",
                    "",
                    "clean: ## Maintenance: Run synthetic cleanup",
                    "",
                    "smoke: ## Quality: Run synthetic smoke check",
                    "\t@printf '%s\\n' 'smoke ok'",
                    "",
                ]
            ),
            encoding="utf-8",
        )

        help_result = self.run_make("help")
        clean_result = self.run_make("clean")
        plain_help = re.sub(r"\x1b\[[0-9;]*m", "", help_result.stdout)

        self.assertEqual(0, help_result.returncode, help_result.stderr)
        self.assertIn("synthetic-service", plain_help)
        self.assertIn("smoke", plain_help)
        self.assertEqual(
            1,
            len(re.findall(r"(?m)^\s+clean\s", plain_help)),
        )
        self.assertIn("Run synthetic cleanup", plain_help)
        self.assertEqual(0, clean_result.returncode, clean_result.stderr)
        self.assertIn("override clean", clean_result.stdout)
        self.assertNotIn("overriding recipe", help_result.stderr)
        self.assertNotIn("overriding recipe", clean_result.stderr)


if __name__ == "__main__":
    unittest.main()
