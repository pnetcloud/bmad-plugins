import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_DIR / "scripts" / "generate_project_docs.py"
SPEC = importlib.util.spec_from_file_location("project_docs_generator", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ProjectDocumentGeneratorTests(unittest.TestCase):
    def test_generates_all_documents_with_resolvable_requirement_traces(self):
        with tempfile.TemporaryDirectory() as directory:
            generator = MODULE.ProjectDocumentGenerator("Synthetic Project", "generic")
            documents = generator.generate_all_documents(
                features=["review a planning change", "validate traceability"],
                components=["Planning API", "Evidence Store"],
                output_dir=directory,
            )

            self.assertEqual(set(documents), set(MODULE.OUTPUT_FILES))
            for filename in MODULE.OUTPUT_FILES:
                self.assertTrue((Path(directory) / filename).is_file())

            requirements = documents["requirements.md"]
            tasks = documents["tasks.md"]
            requirement_ids = set(MODULE.re.findall(r"^### (REQ-\d+):", requirements, MODULE.re.MULTILINE))
            traceability_ids = set(
                MODULE.re.findall(
                    r"^\| (REQ-\d+) \|",
                    requirements,
                    MODULE.re.MULTILINE,
                )
            )
            task_ids = set(MODULE.re.findall(r"\bREQ-\d+\b", tasks))
            self.assertEqual(requirement_ids, {"REQ-1", "REQ-2"})
            self.assertEqual(traceability_ids, requirement_ids)
            self.assertEqual(task_ids, requirement_ids)
            self.assertNotIn("REQ-12.1", tasks)

    def test_generated_templates_do_not_embed_working_secrets_or_fake_targets(self):
        generator = MODULE.ProjectDocumentGenerator("Synthetic Project")
        design = generator.generate_design_template(["Auth Service"])

        for unsafe in [
            "user:pass@",
            "your-api-key",
            "your-secret-key",
            "p95 < 500ms",
            "100 concurrent users",
            "POSTGRES_PASSWORD=",
        ]:
            self.assertNotIn(unsafe, design)
        self.assertIn("[APPROVED PERCENTILE AND THRESHOLD]", design)
        self.assertIn("class AuthServiceInterface", design)
        for unsupported_default in [
            "Frontend Layer",
            "API Gateway | Services",
            "postgres:15",
            "JWT-based authentication",
            "Opens after 5 consecutive failures",
        ]:
            self.assertNotIn(unsupported_default, design)

    def test_default_prompts_match_project_shape_without_claiming_architecture(self):
        cases = {
            "web-app": ("browser-based outcome", "User Interaction Boundary"),
            "cli-tool": ("primary command", "Command Interface"),
            "api-service": ("primary interface", "API Interface"),
            "generic": ("primary supported outcome", "Primary Interface"),
        }
        for project_type, (feature, component) in cases.items():
            with self.subTest(project_type=project_type):
                with tempfile.TemporaryDirectory() as directory:
                    generator = MODULE.ProjectDocumentGenerator(
                        "Synthetic Project",
                        project_type,
                    )
                    documents = generator.generate_all_documents(
                        output_dir=directory,
                    )
                    self.assertIn(feature, documents["requirements.md"])
                    self.assertIn(component, documents["design.md"])
                    self.assertIn(
                        "candidate planning prompts",
                        documents["tasks.md"],
                    )

    def test_refuses_overwrite_without_force_and_replaces_with_force(self):
        with tempfile.TemporaryDirectory() as directory:
            generator = MODULE.ProjectDocumentGenerator("Synthetic Project", "generic")
            generator.generate_all_documents(output_dir=directory)
            requirements = Path(directory) / "requirements.md"
            requirements.write_text("owned content", encoding="utf-8")

            with self.assertRaises(FileExistsError):
                generator.generate_all_documents(output_dir=directory)
            self.assertEqual(requirements.read_text(encoding="utf-8"), "owned content")

            generator.generate_all_documents(output_dir=directory, force=True)
            self.assertIn("# Requirements Document", requirements.read_text(encoding="utf-8"))

    def test_cli_reports_expected_overwrite_failure_without_traceback(self):
        with tempfile.TemporaryDirectory() as directory:
            generator = MODULE.ProjectDocumentGenerator("Synthetic Project", "generic")
            generator.generate_all_documents(output_dir=directory)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "Synthetic Project",
                    "--type",
                    "generic",
                    "--output",
                    directory,
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("Refusing to replace existing documents", result.stderr)
            self.assertNotIn("Traceback", result.stderr)

    def test_rejects_symlinked_output_components_and_destinations(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            real = root / "real"
            real.mkdir()
            linked = root / "linked"
            linked.symlink_to(real, target_is_directory=True)
            generator = MODULE.ProjectDocumentGenerator("Synthetic Project", "generic")

            with self.assertRaisesRegex(ValueError, "symlink"):
                generator.generate_all_documents(output_dir=linked / "docs")

            broken = root / "broken"
            broken.symlink_to(root / "missing", target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "symlink"):
                generator.generate_all_documents(output_dir=broken / "docs")

            destination = real / "requirements.md"
            external = root / "external.md"
            external.write_text("external", encoding="utf-8")
            destination.symlink_to(external)
            with self.assertRaisesRegex(ValueError, "symlinked document"):
                generator.generate_all_documents(output_dir=real, force=True)
            self.assertEqual(external.read_text(encoding="utf-8"), "external")

    def test_rejects_multiline_or_control_character_inputs(self):
        with self.assertRaisesRegex(ValueError, "single printable line"):
            MODULE.ProjectDocumentGenerator("Unsafe\nHeading")
        with self.assertRaisesRegex(ValueError, "single printable line"):
            MODULE.validate_single_line("feature\tvalue", "feature")
        with self.assertRaisesRegex(ValueError, "project type"):
            MODULE.ProjectDocumentGenerator("Synthetic Project", "unknown")
        generator = MODULE.ProjectDocumentGenerator("Synthetic Project", "generic")
        with self.assertRaisesRegex(ValueError, "feature prompt"):
            generator.generate_requirements_template([])
        with self.assertRaisesRegex(ValueError, "component prompt"):
            generator.generate_design_template([])
        with self.assertRaisesRegex(ValueError, "candidate phase"):
            generator.generate_tasks_template([])

    def test_escapes_dynamic_markdown_without_changing_identifiers(self):
        generator = MODULE.ProjectDocumentGenerator("Plan <One> | Review", "generic")
        requirements = generator.generate_requirements_template(
            ["review | approve <evidence>"],
        )
        design = generator.generate_design_template(["Review | Boundary"])

        self.assertIn("Plan &lt;One&gt; \\| Review", requirements)
        self.assertIn("review \\| approve &lt;evidence&gt;", requirements)
        self.assertIn("| COMP-1 | Review \\| Boundary |", design)
        self.assertIn("class ReviewBoundaryInterface", design)


if __name__ == "__main__":
    unittest.main()
