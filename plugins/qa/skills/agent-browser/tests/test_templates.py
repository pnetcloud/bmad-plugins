from __future__ import annotations

import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = SKILL_DIR / "templates"
TEMPLATES = sorted(TEMPLATE_DIR.glob("*.sh"))


class TemplateTests(unittest.TestCase):
    def test_templates_are_executable_and_parse_as_bash(self) -> None:
        self.assertEqual(3, len(TEMPLATES))
        for template in TEMPLATES:
            with self.subTest(template=template.name):
                self.assertTrue(template.stat().st_mode & stat.S_IXUSR)
                result = subprocess.run(
                    ["bash", "-n", str(template)],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(0, result.returncode, result.stderr)

    @unittest.skipUnless(shutil.which("shellcheck"), "shellcheck is not installed")
    def test_templates_pass_shellcheck(self) -> None:
        result = subprocess.run(
            ["shellcheck", *(str(template) for template in TEMPLATES)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_templates_keep_browser_and_artifacts_scoped(self) -> None:
        for template in TEMPLATES:
            text = template.read_text(encoding="utf-8")
            with self.subTest(template=template.name):
                self.assertIn("--allowed-domains", text)
                self.assertIn("--content-boundaries", text)
                self.assertIn("--session", text)
                self.assertIn("trap cleanup EXIT", text)

    def test_templates_run_against_a_local_mock_only(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            log_path = root / "calls.log"
            fake = bin_dir / "agent-browser"
            fake.write_text(
                """#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$*" >> "$template_test_log"
if [[ "${template_test_fail_marker:-0}" == "1" && "$*" == *" wait --text "* ]]; then
  exit 1
fi
case "$*" in
  "session id --scope worktree --prefix auth-reuse" | \\
  "session id --scope worktree --prefix capture" | \\
  "session id --scope worktree --prefix form-review")
    printf '%s\\n' "synthetic-session"
    ;;
  "--session synthetic-session --allowed-domains app.example --content-boundaries --state "*" open https://app.example")
    ;;
  "--session synthetic-session --allowed-domains app.example --content-boundaries --max-output 20000 open https://app.example")
    ;;
  "--session synthetic-session --allowed-domains app.example --content-boundaries open https://app.example/form")
    ;;
  "--session synthetic-session wait --load networkidle")
    ;;
  "--session synthetic-session wait --url **/dashboard")
    ;;
  "--session synthetic-session wait --text Authenticated")
    ;;
  "--session synthetic-session get url")
    printf '%s\\n' "https://app.example/dashboard"
    ;;
  "--session synthetic-session get title")
    printf '%s\\n' "Synthetic page"
    ;;
  "--session synthetic-session snapshot -i")
    printf '%s\\n' "@e1 [button] Synthetic"
    ;;
  "--session synthetic-session get text body")
    printf '%s\\n' "Synthetic body"
    ;;
  "--session synthetic-session screenshot --full capture/page-full.png" | \\
  "--session synthetic-session screenshot form/form-review.png" | \\
  "--session synthetic-session pdf capture/page.pdf")
    touch -- "${@: -1}"
    ;;
  "--session synthetic-session close")
    ;;
  *)
    printf '%s\\n' "unexpected agent-browser contract: $*" >&2
    exit 64
    ;;
esac
""",
                encoding="utf-8",
            )
            fake.chmod(0o755)

            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}{os.pathsep}{env['PATH']}"
            env["template_test_log"] = str(log_path)

            state_file = root / "state.json"
            state_file.write_text("{}\n", encoding="utf-8")

            cases = (
                (
                    TEMPLATE_DIR / "authenticated-session.sh",
                    (
                        "https://app.example",
                        "app.example",
                        str(state_file),
                        "**/dashboard",
                        "Authenticated",
                    ),
                ),
                (
                    TEMPLATE_DIR / "capture-workflow.sh",
                    ("https://app.example", "app.example", "capture"),
                ),
                (
                    TEMPLATE_DIR / "form-automation.sh",
                    ("https://app.example/form", "app.example", "form"),
                ),
            )
            for script, arguments in cases:
                with self.subTest(template=script.name):
                    result = subprocess.run(
                        [str(script), *arguments],
                        cwd=root,
                        env=env,
                        check=False,
                        capture_output=True,
                        text=True,
                    )
                    self.assertEqual(0, result.returncode, result.stderr)

            calls = log_path.read_text(encoding="utf-8")
            self.assertIn("--allowed-domains app.example", calls)
            self.assertIn("--content-boundaries", calls)
            self.assertIn("--session synthetic-session close", calls)
            self.assertTrue((root / "capture/page-full.png").is_file())
            self.assertTrue((root / "capture/page.pdf").is_file())
            self.assertTrue((root / "form/form-review.png").is_file())

            rejected_env = env.copy()
            rejected_env["template_test_fail_marker"] = "1"
            rejected = subprocess.run(
                [
                    str(TEMPLATE_DIR / "authenticated-session.sh"),
                    "https://app.example",
                    "app.example",
                    str(state_file),
                    "**/dashboard",
                    "Authenticated",
                ],
                cwd=root,
                env=rejected_env,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(0, rejected.returncode)
            self.assertNotIn("state restored", rejected.stdout)

    def test_output_and_state_path_guards_fail_before_browser_use(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            env = os.environ.copy()
            env["PATH"] = str(Path(shutil.which("bash") or "/bin/bash").parent)

            capture = subprocess.run(
                [
                    str(TEMPLATE_DIR / "capture-workflow.sh"),
                    "https://app.example",
                    "app.example",
                    "/absolute-output",
                ],
                cwd=root,
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(0, capture.returncode)
            self.assertIn("task-owned relative path", capture.stderr)

            external = root / "external"
            external.mkdir()
            parent_link = root / "parent-link"
            parent_link.symlink_to(external, target_is_directory=True)
            for template, start_url in (
                (TEMPLATE_DIR / "capture-workflow.sh", "https://app.example"),
                (TEMPLATE_DIR / "form-automation.sh", "https://app.example/form"),
            ):
                escaped = subprocess.run(
                    [
                        str(template),
                        start_url,
                        "app.example",
                        "parent-link/output",
                    ],
                    cwd=root,
                    env=env,
                    check=False,
                    capture_output=True,
                    text=True,
                )
                with self.subTest(template=template.name):
                    self.assertNotEqual(0, escaped.returncode)
                    self.assertIn("must not contain a symlink", escaped.stderr)
                    self.assertFalse((external / "output").exists())

            state_file = root / "state.json"
            state_file.write_text("{}\n", encoding="utf-8")
            state_link = root / "state-link.json"
            state_link.symlink_to(state_file)
            auth = subprocess.run(
                [
                    str(TEMPLATE_DIR / "authenticated-session.sh"),
                    "https://app.example",
                    "app.example",
                    str(state_link),
                    "**/dashboard",
                    "Authenticated",
                ],
                cwd=root,
                env=env,
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(0, auth.returncode)
            self.assertIn("non-symlink", auth.stderr)


if __name__ == "__main__":
    unittest.main()
