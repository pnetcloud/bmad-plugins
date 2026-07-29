from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    return " ".join(SKILL.read_text(encoding="utf-8").lower().replace("`", "").split())


class DocsGeneralContractTests(unittest.TestCase):
    def test_frontmatter(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-docs-general\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("general documentation", "do not use", "product copy", "framework-specific"):
            self.assertIn(phrase, description)

    def test_entrypoint_budget(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 180)
        self.assertLessEqual(len(text.split()), 1500)

    def test_original_taxonomy_retained(self):
        text = normalized()
        for name in (
            "api/", "architecture/", "business/", "compliance/", "deployment/",
            "development/", "governance/", "integration/", "knowledge-base/",
            "marketing/", "operations/", "security/", "testing/", "ui-ux/", "planning/",
        ):
            self.assertIn(name, text)

    def test_original_practices_retained(self):
        text = normalized()
        for phrase in (
            "keep docs in sync with code changes",
            "use adrs inside architecture/",
            "update openapi schemas with each api change",
            "maintain security and compliance checklists",
            "short, structured, and cross-linked",
        ):
            self.assertIn(phrase, text)

    def test_repository_aware_structure(self):
        text = normalized()
        for phrase in (
            "repository's declared documentation roots",
            "candidate taxonomy only",
            "not mandatory duplicates",
            "single source” is semantic",
            "do not create empty readme.md",
            "preserve the established file-naming convention",
            "use markdown as the default",
            "default to snake-case.md",
            "durable documentation or tooling contract",
        ):
            self.assertIn(phrase, text)

    def test_authority_safety_and_publication(self):
        text = normalized()
        for phrase in (
            "discovery and review are read-only",
            "require explicit authority",
            "resolve and confirm the active executor identity",
            "synthetic or composite examples",
            "never clean, reset, overwrite, or switch",
            "history remediation as a separate authorized incident",
            "local build does not prove publication",
            "report policy-blocked links as unverified",
            "spot evidence, not whole-site validation",
        ):
            self.assertIn(phrase, text)

    def test_docs_workflow_and_evidence(self):
        text = normalized()
        for phrase in (
            "build a content inventory",
            "one authority per claim",
            "tutorials, how-to guides, reference, and explanation",
            "current behavior, proposed or planned work, and historical records",
            "rendered form",
            "mark unresolved facts and owners",
            "revision-bound status overview",
        ):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 26)
        identifiers, expectations = [], set()
        for block in blocks:
            identifier = re.search(r"^  - id: (.+)$", block, re.MULTILINE).group(1)
            fields = dict(re.findall(r"^    (expect|prompt|evidence): (.+)$", block, re.MULTILINE))
            self.assertEqual(set(fields), {"expect", "prompt", "evidence"})
            self.assertGreaterEqual(len(fields["prompt"].split()), 8)
            self.assertGreaterEqual(len(fields["evidence"].split()), 8)
            identifiers.append(identifier)
            expectations.add(fields["expect"])
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(expectations, {"trigger", "no_trigger", "safe_behavior", "bounded_behavior", "workflow"})


if __name__ == "__main__":
    unittest.main()
