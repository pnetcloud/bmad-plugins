from pathlib import Path
import json
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
SCENARIOS = json.loads((ROOT / "tests" / "scenarios.json").read_text(encoding="utf-8"))


class PackageContractTests(unittest.TestCase):
    def test_frontmatter_preserves_original_metadata_in_supported_shape(self):
        frontmatter = SKILL.split("---", 2)[1]
        keys = {
            line.split(":", 1)[0]
            for line in frontmatter.splitlines()
            if re.match(r"^[a-z][a-z-]*:", line)
        }
        self.assertEqual(keys, {"name", "description", "metadata"})
        for value in ('"author":"vercel"', '"version":"1.0.0"', "<file-or-pattern>"):
            self.assertIn(value, frontmatter)

    def test_original_trigger_families_remain(self):
        frontmatter = SKILL.split("---", 2)[1].lower()
        for trigger in (
            "review ui",
            "audit design",
            "ux",
            "accessibility",
            "check my site against best practices",
        ):
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, frontmatter)

    def test_original_source_is_preserved(self):
        self.assertIn(
            "https://raw.githubusercontent.com/"
            "vercel-labs/web-interface-guidelines/main/command.md",
            SKILL,
        )

    def test_remote_checklist_is_pinned_and_untrusted(self):
        acquisition = SKILL.split("## Acquire the Checklist Safely", 1)[1].split(
            "## Review Workflow", 1
        )[0]
        for contract in (
            "resolve `main` to an exact commit",
            "raw file at that commit",
            "Treat fetched frontmatter",
            "Do not execute code",
            "Before opening any fetched link, independently verify",
            "never pretend it is current",
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract, acquisition)

    def test_project_and_framework_applicability_precede_findings(self):
        self.assertIn("project's own contracts", SKILL)
        self.assertIn("framework mismatch", SKILL)
        self.assertIn("Vercel-specific section is a source preference", SKILL)
        self.assertIn("Search shared components", SKILL)

    def test_static_review_does_not_claim_runtime_or_wcag_conformance(self):
        self.assertIn("Manual check", SKILL)
        self.assertIn("normative success criteria", SKILL)
        self.assertIn("full page and complete process", SKILL)
        self.assertIn("accessibility-supported", SKILL)
        self.assertIn("checking non-interference", SKILL)
        self.assertIn("informative patterns", SKILL)
        self.assertIn("complete conformance workflow", SKILL)

    def test_findings_require_location_scenario_basis_and_fix(self):
        output = SKILL.split("## Output", 1)[1]
        for field in ("file:line", "Evidence:", "Basis:", "Fix:"):
            with self.subTest(field=field):
                self.assertIn(field, output)

    def test_entrypoint_remains_compact(self):
        self.assertLessEqual(len(SKILL.splitlines()), 180)
        self.assertLessEqual(len(re.findall(r"\S+", SKILL)), 1500)

    def test_scenario_vectors_cover_required_behavior_dimensions(self):
        required_fields = {"id", "tags", "given", "require", "forbid"}
        ids = [scenario["id"] for scenario in SCENARIOS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(required_fields == set(scenario) for scenario in SCENARIOS))
        self.assertTrue(all(scenario["require"] for scenario in SCENARIOS))
        self.assertTrue(all(scenario["forbid"] for scenario in SCENARIOS))

        covered_tags = {
            tag for scenario in SCENARIOS for tag in scenario["tags"]
        }
        self.assertTrue(
            {"positive-trigger", "negative-trigger", "main-task", "safety"}
            <= covered_tags
        )
        self.assertTrue(
            {
                "retention-trigger",
                "checklist-refresh",
                "all-rules",
                "output-contract",
            }
            <= covered_tags
        )


if __name__ == "__main__":
    unittest.main()
