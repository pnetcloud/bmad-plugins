from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "validate_documents.py"
SPEC = importlib.util.spec_from_file_location("planning_validator", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


VALID_REQUIREMENTS = """\
# Requirements
### REQ-001: Search
Acceptance:
1. Given an indexed item, when searched, then it is returned.
"""

VALID_DESIGN = """\
# Design
### DEC-001: Index
- Requirements: REQ-001
"""

VALID_TASKS = """\
# Tasks
### TASK-001: Search slice
- Requirements: REQ-001
- Design: DEC-001
- Dependencies: none
- Validation: focused search test
- Status: planned
"""


class ValidatorTests(unittest.TestCase):
    def validate(
        self,
        requirements: str = VALID_REQUIREMENTS,
        design: str = VALID_DESIGN,
        tasks: str = VALID_TASKS,
        allow_placeholders: bool = False,
    ):
        with tempfile.TemporaryDirectory() as tempdir:
            root = Path(tempdir)
            paths = []
            for name, content in (
                ("requirements.md", requirements),
                ("design.md", design),
                ("tasks.md", tasks),
            ):
                path = root / name
                path.write_text(content, encoding="utf-8")
                paths.append(path)
            return MODULE.validate(*paths, allow_placeholders=allow_placeholders)

    def test_valid_package_passes(self) -> None:
        report = self.validate()
        self.assertEqual([], report.errors)

    def test_unresolved_placeholder_blocks_completion(self) -> None:
        report = self.validate(requirements=VALID_REQUIREMENTS + "\n{{owner}}\n")
        self.assertTrue(any("placeholder" in error for error in report.errors))

    def test_draft_can_explicitly_allow_placeholders(self) -> None:
        report = self.validate(
            requirements=VALID_REQUIREMENTS + "\n{{owner}}\n",
            allow_placeholders=True,
        )
        self.assertEqual([], report.errors)

    def test_duplicate_requirement_is_rejected(self) -> None:
        report = self.validate(
            requirements=VALID_REQUIREMENTS
            + "\n### REQ-001: Duplicate\nAcceptance:\n1. Given x, when y, then z.\n"
        )
        self.assertTrue(any("duplicate requirement" in error for error in report.errors))

    def test_unknown_requirement_reference_is_rejected(self) -> None:
        report = self.validate(tasks=VALID_TASKS.replace("REQ-001", "REQ-404"))
        self.assertTrue(any("unknown requirement" in error for error in report.errors))

    def test_unimplemented_requirement_is_rejected(self) -> None:
        requirements = (
            VALID_REQUIREMENTS
            + "\n### REQ-002: Export\nAcceptance:\n"
            + "1. Given a result, when exported, then a file is produced.\n"
        )
        report = self.validate(requirements=requirements)
        self.assertTrue(any("no implementation task" in error for error in report.errors))

    def test_traceability_table_does_not_fake_task_coverage(self) -> None:
        requirements = (
            VALID_REQUIREMENTS
            + "\n### REQ-002: Export\nAcceptance:\n"
            + "1. Given a result, when exported, then a file is produced.\n"
        )
        design = VALID_DESIGN + "\n### DEC-002: Export\n- Requirements: REQ-002\n"
        tasks = VALID_TASKS + "\n## Traceability\n| REQ-002 | none |\n"
        report = self.validate(
            requirements=requirements, design=design, tasks=tasks
        )
        self.assertTrue(any("no implementation task" in error for error in report.errors))

    def test_requirement_without_design_trace_is_rejected(self) -> None:
        requirements = (
            VALID_REQUIREMENTS
            + "\n### REQ-002: Export\nAcceptance:\n"
            + "1. Given a result, when exported, then a file is produced.\n"
        )
        tasks = VALID_TASKS.replace(
            "- Requirements: REQ-001",
            "- Requirements: REQ-001, REQ-002",
        )
        report = self.validate(requirements=requirements, tasks=tasks)
        self.assertTrue(any("no design trace" in error for error in report.errors))

    def test_unknown_dependency_is_rejected(self) -> None:
        report = self.validate(
            tasks=VALID_TASKS.replace(
                "- Dependencies: none", "- Dependencies: TASK-404"
            )
        )
        self.assertTrue(any("unknown task" in error for error in report.errors))

    def test_unknown_design_reference_is_rejected(self) -> None:
        report = self.validate(
            tasks=VALID_TASKS.replace("DEC-001", "DEC-404")
        )
        self.assertTrue(
            any("unknown design ID" in error for error in report.errors)
        )

    def test_self_dependency_is_rejected(self) -> None:
        report = self.validate(
            tasks=VALID_TASKS.replace(
                "- Dependencies: none", "- Dependencies: TASK-001"
            )
        )
        self.assertTrue(any("depends on itself" in error for error in report.errors))

    def test_dependency_cycle_is_rejected(self) -> None:
        tasks = """\
# Tasks
### TASK-001: First
- Requirements: REQ-001
- Design: DEC-001
- Dependencies: TASK-002
- Validation: first test
- Status: planned
### TASK-002: Second
- Requirements: REQ-001
- Design: DEC-001
- Dependencies: TASK-001
- Validation: second test
- Status: planned
"""
        report = self.validate(tasks=tasks)
        self.assertTrue(any("cycle" in error for error in report.errors))


if __name__ == "__main__":
    unittest.main()
