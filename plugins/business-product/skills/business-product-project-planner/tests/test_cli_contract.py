from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
GENERATOR = SKILL_DIR / "scripts" / "generate_project_docs.py"
VALIDATOR = SKILL_DIR / "scripts" / "validate_documents.py"


def run_script(script, *arguments):
    return subprocess.run(
        [sys.executable, str(script), *arguments],
        capture_output=True,
        text=True,
        check=False,
    )


class CliContractTests(unittest.TestCase):
    def test_generator_help_preserves_public_flags_and_project_types(self):
        result = run_script(GENERATOR, "--help")

        self.assertEqual(result.returncode, 0)
        for flag in ["--type", "--features", "--components", "--output", "--force"]:
            self.assertIn(flag, result.stdout)
        for project_type in ["web-app", "cli-tool", "api-service", "generic"]:
            self.assertIn(project_type, result.stdout)

    def test_validator_help_preserves_public_flags(self):
        result = run_script(VALIDATOR, "--help")

        self.assertEqual(result.returncode, 0)
        for flag in ["--requirements", "--design", "--tasks", "--strict"]:
            self.assertIn(flag, result.stdout)

    def test_cli_exit_semantics_for_generated_scaffolds(self):
        with tempfile.TemporaryDirectory() as directory:
            generated = run_script(
                GENERATOR,
                "Synthetic Project",
                "--type",
                "generic",
                "--output",
                directory,
            )
            self.assertEqual(generated.returncode, 0, generated.stderr)
            for name in ["requirements.md", "design.md", "tasks.md"]:
                self.assertTrue((Path(directory) / name).is_file())

            arguments = [
                "--requirements",
                str(Path(directory) / "requirements.md"),
                "--design",
                str(Path(directory) / "design.md"),
                "--tasks",
                str(Path(directory) / "tasks.md"),
            ]
            non_strict = run_script(VALIDATOR, *arguments)
            strict = run_script(VALIDATOR, *arguments, "--strict")

            self.assertEqual(non_strict.returncode, 0, non_strict.stderr)
            self.assertEqual(strict.returncode, 1, strict.stderr)
            self.assertIn("Total Warnings:", strict.stdout)


if __name__ == "__main__":
    unittest.main()
