from __future__ import annotations

import os
import shutil
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts/build-push.sh"


class BuildPushTests(unittest.TestCase):
    def run_script(
        self,
        root: Path,
        fake_bin: Path,
        *arguments: str,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        environment["PATH"] = f"{fake_bin}{os.pathsep}{environment['PATH']}"
        environment["docker_call_log"] = str(root / "docker-calls.log")
        return subprocess.run(
            [str(SCRIPT), *arguments],
            cwd=root,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_script_is_executable_and_static_checks_pass(self) -> None:
        self.assertTrue(SCRIPT.stat().st_mode & stat.S_IXUSR)
        syntax = subprocess.run(
            ["bash", "-n", str(SCRIPT)],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, syntax.returncode, syntax.stderr)
        if shutil.which("shellcheck"):
            lint = subprocess.run(
                ["shellcheck", str(SCRIPT)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, lint.returncode, lint.stdout + lint.stderr)

    def test_build_and_push_contract_uses_only_the_resolved_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            (root / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
            fake_bin = root / "bin"
            fake_bin.mkdir()
            fake_docker = fake_bin / "docker"
            fake_docker.write_text(
                """#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$*" >> "$docker_call_log"
if [[ "$#" -eq 5 &&
      "$1" == "image" &&
      "$2" == "inspect" &&
      "$3" == "registry.example/team/service-api:review-7" &&
      "$4" == "--format" &&
      "$5" == '{{.Id}} {{json .RepoDigests}}' ]]; then
  printf '%s\\n' 'sha256:synthetic ["registry.example/team/service-api@sha256:synthetic"]'
  exit 0
fi
case "$*" in
  "build --tag registry.example/team/service-api:review-7 --file Dockerfile -- .")
    ;;
  "push registry.example/team/service-api:review-7")
    ;;
  *)
    printf 'unexpected docker invocation: %s\\n' "$*" >&2
    exit 64
    ;;
esac
""",
                encoding="utf-8",
            )
            fake_docker.chmod(0o755)

            result = self.run_script(
                root,
                fake_bin,
                "--image",
                "team/service-api",
                "--tag",
                "review-7",
                "--registry",
                "registry.example",
                "--push",
            )
            self.assertEqual(0, result.returncode, result.stderr)
            calls = (root / "docker-calls.log").read_text(encoding="utf-8")
            self.assertEqual(3, len(calls.splitlines()))
            self.assertIn("push registry.example/team/service-api:review-7", calls)

    def test_build_only_never_pushes(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            (root / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
            fake_bin = root / "bin"
            fake_bin.mkdir()
            fake_docker = fake_bin / "docker"
            fake_docker.write_text(
                """#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$*" >> "$docker_call_log"
case "$1" in
  build) ;;
  image) printf '%s\\n' "sha256:synthetic" ;;
  *) exit 64 ;;
esac
""",
                encoding="utf-8",
            )
            fake_docker.chmod(0o755)

            result = self.run_script(
                root,
                fake_bin,
                "--image",
                "service-api",
                "--tag",
                "review-7",
            )
            self.assertEqual(0, result.returncode, result.stderr)
            calls = (root / "docker-calls.log").read_text(encoding="utf-8")
            self.assertNotIn("push", calls)

    def test_unsafe_or_incomplete_requests_fail_before_docker(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            root = Path(temp_name)
            (root / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
            fake_bin = root / "bin"
            fake_bin.mkdir()
            fake_docker = fake_bin / "docker"
            fake_docker.write_text("#!/usr/bin/env bash\nexit 99\n", encoding="utf-8")
            fake_docker.chmod(0o755)

            cases = (
                (("--image", "service-api", "--tag", "latest"), "mutable tag"),
                (
                    ("--image", "service-api", "--tag", "review-7", "--push"),
                    "requires --registry",
                ),
                (("--image", "UPPER", "--tag", "review-7"), "image name"),
                (
                    (
                        "--image",
                        "service-api",
                        "--tag",
                        "review-7",
                        "--registry",
                        "--bad",
                    ),
                    "registry must be",
                ),
                (("--image", "service-api", "--tag"), "missing value"),
            )
            for arguments, expected in cases:
                with self.subTest(arguments=arguments):
                    result = self.run_script(root, fake_bin, *arguments)
                    self.assertNotEqual(0, result.returncode)
                    self.assertIn(expected, result.stderr)
            self.assertFalse((root / "docker-calls.log").exists())


if __name__ == "__main__":
    unittest.main()
