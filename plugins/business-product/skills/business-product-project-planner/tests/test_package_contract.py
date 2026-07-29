import json
from pathlib import Path
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]


def section(content, heading):
    start = content.index(heading) + len(heading)
    next_heading = content.find("\n## ", start)
    return content[start:] if next_heading == -1 else content[start:next_heading]


def between(content, start_heading, end_heading):
    start = content.index(start_heading) + len(start_heading)
    end = content.index(end_heading, start)
    return content[start:end]


class PackageContractTests(unittest.TestCase):
    def test_all_original_resources_remain_present(self):
        for relative in [
            "SKILL.md",
            "README.md",
            "plugin.json",
            "skill-report.json",
            "assets/requirements-template.md",
            "references/domain-templates.md",
            "scripts/generate_project_docs.py",
            "scripts/validate_documents.py",
        ]:
            self.assertTrue((SKILL_DIR / relative).is_file(), relative)

    def test_entrypoint_routes_every_packaged_capability(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        for destination in [
            "references/document-contracts.md",
            "references/domain-templates.md",
            "references/project-type-patterns.md",
            "assets/requirements-template.md",
            "scripts/generate_project_docs.py",
            "scripts/validate_documents.py",
        ]:
            self.assertIn(destination, skill)
        line_count = len(skill.splitlines())
        word_count = len(skill.split())
        self.assertGreaterEqual(line_count, 80)
        self.assertLessEqual(line_count, 180)
        self.assertGreaterEqual(word_count, 600)
        self.assertLessEqual(word_count, 1500)

    def test_document_contract_retains_planning_and_traceability_surfaces(self):
        contract = (
            SKILL_DIR / "references" / "document-contracts.md"
        ).read_text(encoding="utf-8")
        for heading in [
            "## Requirements Document",
            "## Design Document",
            "## Implementation Plan",
            "## Traceability",
            "## Update Mode",
            "## Validation Mode",
            "## Domain Routing",
        ]:
            self.assertIn(heading, contract)
        self.assertGreaterEqual(len(contract.splitlines()), 250)
        requirements = between(
            contract,
            "## Requirements Document",
            "## Design Document",
        )
        design = between(
            contract,
            "## Design Document",
            "## Implementation Plan",
        )
        plan = between(
            contract,
            "## Implementation Plan",
            "## Update Mode",
        )
        for marker in ["REQ-[N]", "Source:", "Acceptance evidence", "Unknowns:"]:
            self.assertIn(marker, requirements)
        for marker in ["COMP-1", "INT-[N]", "FLOW-[N]", "DEC-1"]:
            self.assertIn(marker, design)
        for marker in [
            "TASK-[N]",
            "In scope:",
            "Out of scope:",
            "Dependencies:",
            "Verification:",
            "Completion:",
        ]:
            self.assertIn(marker, plan)

    def test_domain_reference_retains_all_original_domain_families(self):
        reference = (
            SKILL_DIR / "references" / "domain-templates.md"
        ).read_text(encoding="utf-8")
        for heading in [
            "## Trading and Financial Systems",
            "## Real-time Systems",
            "## E-commerce",
            "## Content Management Systems",
            "## IoT",
            "## Machine Learning Pipelines",
            "## Developer Tools",
            "## SaaS",
            "## Data Lakehouse and Analytics Systems",
            "## AI Agent and Orchestration Systems",
            "## Enterprise Integration Platforms",
            "## Common Non-Functional Requirements",
            "## Cross-Cutting Concerns",
            "## Task Breakdown Patterns by Domain",
            "## Testing Strategies by Domain",
            "## Deployment Patterns",
        ]:
            self.assertIn(heading, reference)
        self.assertGreaterEqual(len(reference.splitlines()), 1200)
        self.assertGreaterEqual(len(reference.split()), 5000)
        for heading in [
            "## Trading and Financial Systems",
            "## Real-time Systems",
            "## E-commerce",
            "## Content Management Systems",
            "## IoT",
            "## Machine Learning Pipelines",
            "## Developer Tools",
            "## SaaS",
            "## Data Lakehouse and Analytics Systems",
            "## AI Agent and Orchestration Systems",
            "## Enterprise Integration Platforms",
        ]:
            domain = section(reference, heading)
            self.assertIn("### Specific Requirements Patterns", domain)
            self.assertIn("### Architecture Components", domain)

    def test_project_type_reference_retains_original_planning_families(self):
        reference = (
            SKILL_DIR / "references" / "project-type-patterns.md"
        ).read_text(encoding="utf-8")
        for heading in [
            "## Web Applications",
            "## Service APIs",
            "## Command-Line Tools and Libraries",
            "## Service-Decomposed Systems",
            "## Data Pipelines",
            "## Generic or Uncertain Projects",
            "## Shared Delivery Families",
        ]:
            self.assertIn(heading, reference)
        for heading in [
            "## Web Applications",
            "## Service APIs",
            "## Command-Line Tools and Libraries",
            "## Service-Decomposed Systems",
            "## Data Pipelines",
        ]:
            project_type = section(reference, heading)
            self.assertIn("Requirements", project_type)
            self.assertIn("Design", project_type)
            self.assertIn("Delivery", project_type)

    def test_public_metadata_has_no_email_and_report_is_historical(self):
        plugin = json.loads((SKILL_DIR / "plugin.json").read_text(encoding="utf-8"))
        report = json.loads(
            (SKILL_DIR / "skill-report.json").read_text(encoding="utf-8")
        )
        self.assertNotIn("email", plugin["author"])
        self.assertIn("Historical provenance", report["record_notice"])


if __name__ == "__main__":
    unittest.main()
