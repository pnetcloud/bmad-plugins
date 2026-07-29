import importlib.util
import contextlib
import io
from pathlib import Path
import tempfile
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
GENERATOR_SCRIPT = SKILL_DIR / "scripts" / "generate_project_docs.py"
VALIDATOR_SCRIPT = SKILL_DIR / "scripts" / "validate_documents.py"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


generator_module = load("project_docs_generator_for_validation", GENERATOR_SCRIPT)
validator_module = load("project_docs_validator", VALIDATOR_SCRIPT)


class DocumentValidatorTests(unittest.TestCase):
    def test_canonical_document_contract_is_accepted(self):
        validator = validator_module.DocumentValidator()
        requirements = """## Purpose and Outcomes
## Glossary
## Functional Requirements
### REQ-1: Review evidence
**Outcome:** A reviewer can make a supported decision.
**Acceptance evidence:**
GIVEN a planning set, WHEN it is reviewed, THEN gaps are observable.
## Traceability
| Requirement | Design coverage | Delivery tasks | Verification | Status |
|---|---|---|---|---|
| REQ-1 | DEC-1, COMP-1, INT-1, FLOW-1 | TASK-1, TASK-2 | review | covered |
"""
        design = """## Context and Goals
## System Boundary
### Component Map
| Component ID | Name |
|---|---|
| COMP-1 | Planner |
## Component Responsibilities
## Interfaces and Integration Points
### INT-1: Review input
```
[contract]
```
## Data and State
## End-to-End Flows
### FLOW-1: Review
```
[flow]
```
| ID | Decision |
|---|---|
| DEC-1 | Preserve evidence |
## Deployment and Environments
"""
        tasks = """## Boundaries and Non-Goals
## Milestones or Vertical Slices
## Tasks
- [ ] TASK-1: Establish contract
  - In scope: Define the review boundary.
  - Out of scope: Implementation.
  - Requirements: REQ-1
  - Design: DEC-1, COMP-1, INT-1, FLOW-1
  - Dependencies: none
  - Verification: Document review.
  - Completion: Contract accepted.
- [ ] TASK-2: Verify traceability
  - In scope: Check mappings.
  - Out of scope: Implementation.
  - Requirements: REQ-1
  - Design: DEC-1, COMP-1, INT-1, FLOW-1
  - Dependencies: TASK-1
  - Verification: Validator output.
  - Completion: No dangling IDs.
"""
        results = {
            "requirements": validator.validate_requirements(requirements),
            "design": validator.validate_design(design),
            "tasks": validator.validate_tasks(tasks),
            "consistency": validator.validate_consistency(
                requirements,
                design,
                tasks,
            ),
        }
        errors = [error for group, _ in results.values() for error in group]
        self.assertEqual(errors, [])

    def test_generated_triplet_has_no_structural_or_consistency_errors(self):
        with tempfile.TemporaryDirectory() as directory:
            generator = generator_module.ProjectDocumentGenerator(
                "Synthetic Project",
                "generic",
            )
            generator.generate_all_documents(
                features=["inspect evidence", "approve a plan"],
                components=["Planner", "Evidence Store"],
                output_dir=directory,
            )
            validator = validator_module.DocumentValidator()
            results = validator.validate_all(
                str(Path(directory) / "requirements.md"),
                str(Path(directory) / "design.md"),
                str(Path(directory) / "tasks.md"),
            )

            errors = [error for group, _ in results.values() for error in group]
            warnings = [warning for _, group in results.values() for warning in group]
            self.assertEqual(errors, [])
            self.assertTrue(warnings, "scaffolds must retain visible review work")

    def test_duplicate_and_dangling_requirement_ids_are_errors(self):
        validator = validator_module.DocumentValidator()
        requirements = """## Introduction
## Glossary
## Requirements
### REQ-1: First
**User Story:** As a reviewer, I want evidence, so that I can decide.
#### Acceptance Criteria
THE system SHALL report evidence.
### REQ-1: Duplicate
#### Acceptance Criteria
THE system SHALL reject duplicates.
"""
        errors, _ = validator.validate_requirements(requirements)
        self.assertIn("Duplicate requirement IDs: REQ-1", errors)

        consistency_errors, _ = validator.validate_consistency(
            requirements,
            "## Components\n",
            "_Requirements: REQ-2_\n",
        )
        self.assertIn(
            "Tasks reference unknown requirements: REQ-2",
            consistency_errors,
        )

    def test_duplicate_and_dangling_component_ids_are_errors(self):
        validator = validator_module.DocumentValidator()
        design = """## Overview
## System Architecture
### Component Map
| Component ID | Name |
|---|---|
| COMP-1 | First |
| COMP-1 | Duplicate |
## Data Flow
## Integration Points
## Components
## Data Models
## Deployment
"""
        errors, _ = validator.validate_design(design)
        self.assertIn("Duplicate component IDs: COMP-1", errors)

        consistency_errors, _ = validator.validate_consistency(
            "### REQ-1: Example\n",
            design.replace("| COMP-1 | Duplicate |\n", ""),
            "_Requirements: REQ-1_\n_Components: COMP-2_\n",
        )
        self.assertIn(
            "Tasks reference unknown components: COMP-2",
            consistency_errors,
        )

    def test_duplicate_dangling_and_cyclic_task_links_are_errors(self):
        validator = validator_module.DocumentValidator()
        tasks = """## Project Boundaries
### Must Have
### Out of Scope
## Tasks
- [ ] TASK-1: First
  - _Requirements: REQ-1_
  - _Dependencies: TASK-2_
- [ ] TASK-1: Duplicate
  - _Requirements: REQ-1_
- [ ] TASK-2: Second
  - _Requirements: REQ-1_
  - _Dependencies: TASK-1, TASK-3_
"""
        errors, _ = validator.validate_tasks(tasks)
        self.assertIn("Duplicate task IDs: TASK-1", errors)
        self.assertIn("Tasks reference unknown dependencies: TASK-3", errors)
        self.assertTrue(
            any(error.startswith("Task dependency cycle:") for error in errors)
        )

        consistency_errors, _ = validator.validate_consistency(
            "### REQ-1: Example\n",
            "| COMP-1 | Planner |\n| DEC-1 | Choice |\n### INT-1: Input\n",
            "_Requirements: REQ-1_\n_Design: DEC-2, INT-2, FLOW-1_\n",
        )
        self.assertIn(
            "Tasks reference unknown design IDs: DEC-2, FLOW-1, INT-2",
            consistency_errors,
        )

    def test_traceability_table_rejects_duplicate_and_dangling_ids(self):
        validator = validator_module.DocumentValidator()
        requirements = """### REQ-1: Example
## Traceability
| Requirement | Design coverage | Delivery tasks | Verification | Status |
|---|---|---|---|---|
| REQ-1 | DEC-1, COMP-1, INT-1, FLOW-1 | TASK-1 | review | covered |
| REQ-1 | DEC-999, INT-999, FLOW-999 | TASK-999 | review | covered |
| REQ-999 | COMP-999 | TASK-1 | review | gap |
"""
        design = """| COMP-1 | Planner |
| DEC-1 | Preserve evidence |
### INT-1: Input
### FLOW-1: Review
"""
        tasks = """- [ ] TASK-1: Review evidence
  - Requirements: REQ-1
"""

        errors, _ = validator.validate_consistency(
            requirements,
            design,
            tasks,
        )

        self.assertIn("Duplicate traceability rows: REQ-1", errors)
        self.assertIn(
            "Traceability references unknown requirements: REQ-999",
            errors,
        )
        self.assertIn(
            "Traceability references unknown design IDs: "
            "COMP-999, DEC-999, FLOW-999, INT-999",
            errors,
        )
        self.assertIn(
            "Traceability references unknown tasks: TASK-999",
            errors,
        )

    def test_completion_counts_only_actual_task_records(self):
        validator = validator_module.DocumentValidator()
        content = """## Project Boundaries
### Must Have
### Out of Scope
## Tasks
- [x] TASK-1: Accepted task
- [ ] TASK-2: Pending task
## Review Checklist
- [x] Unrelated review item
"""
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            validator.validate_tasks(content)

        self.assertIn("Task completion: 1/2 (50.0%)", output.getvalue())

    def test_user_story_check_does_not_match_across_unrelated_lines(self):
        validator = validator_module.DocumentValidator()
        content = """## Introduction
## Glossary
## Requirements
### REQ-1: Example
As a reviewer
I want evidence
so that I can decide
#### Acceptance Criteria
THE system SHALL report evidence.
"""
        _, warnings = validator.validate_requirements(content)
        self.assertIn("No user stories found in requirements", warnings)

    def test_read_document_rejects_symlinks_and_oversized_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = root / "document.md"
            document.write_text("content", encoding="utf-8")
            linked = root / "linked.md"
            linked.symlink_to(document)
            with self.assertRaisesRegex(ValueError, "non-symlink"):
                validator_module.read_document(str(linked))

            oversized = root / "oversized.md"
            oversized.write_bytes(
                b"x" * (validator_module.max_document_bytes + 1)
            )
            with self.assertRaisesRegex(ValueError, "exceeds"):
                validator_module.read_document(str(oversized))


if __name__ == "__main__":
    unittest.main()
