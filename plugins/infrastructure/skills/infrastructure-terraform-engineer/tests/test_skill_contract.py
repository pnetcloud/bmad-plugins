from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized(value):
    return " ".join(value.replace("`", "").split())


class TerraformEngineerContractTests(unittest.TestCase):
    def test_frontmatter_and_precise_trigger(self):
        self.assertTrue(SKILL.startswith("---\nname: infrastructure-terraform-engineer\n"))
        description = re.search(r"^description: (.+)$", SKILL, re.MULTILINE).group(1)
        for phrase in ("Implement", "review", "Terraform-specific", "do not use"):
            self.assertIn(phrase, description)

    def test_all_linked_references_exist(self):
        links = re.findall(r"\]\((references/[^)]+)\)", SKILL)
        self.assertEqual(len(links), 3)
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)

    def test_long_references_have_navigation(self):
        for path in sorted((ROOT / "references").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if len(text.splitlines()) > 100:
                self.assertIn("## Contents", text, path.name)

    def test_original_capability_families_remain_reachable(self):
        package = normalized(
            "\n".join(
                path.read_text(encoding="utf-8")
                for path in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
            )
        ).lower()
        families = (
            "remote backend", "state locking", "workspace", "state migration",
            "import", "disaster recovery", "provider aliases", "dependency lock",
            "dynamic blocks", "meta-arguments", "data sources", "provisioners",
            "cost", "chargeback", "policy", "compliance", "audit", "rbac",
            "unit", "integration", "performance", "end-to-end", "ci/cd",
            "module registry", "mono-repository", "incident", "training",
        )
        for family in families:
            self.assertIn(family, package, family)

    def test_fictional_protocol_and_metrics_are_absent(self):
        lowered = normalized(SKILL).lower()
        for phrase in (
            "query context manager", '"requesting_agent"', "modules_created",
            "47 reusable modules", "85% code reuse", "30% savings",
            "reusability > 80%",
        ):
            self.assertNotIn(phrase, lowered)

    def test_modes_and_mutation_authority_are_explicit(self):
        text = normalized(SKILL)
        for phrase in (
            "Review and design are read-only",
            "diagnosis does not silently become a fix",
            "requires explicit authority",
            "force-unlock",
        ):
            self.assertIn(phrase, text)

    def test_plan_and_state_sensitivity_are_explicit(self):
        text = normalized(SKILL + (ROOT / "references" / "plans-state-and-operations.md").read_text())
        for phrase in (
            "potentially sensitive", "cleartext sensitive values",
            "speculative plan", "final executable plan", "live writer",
        ):
            self.assertIn(phrase, text)

    def test_test_command_is_not_assumed_safe(self):
        text = normalized(SKILL)
        self.assertIn("terraform test can create billable real infrastructure", text.lower())
        self.assertIn("cleanup can fail", text.lower())

    def test_scenario_vectors_have_complete_individual_contracts(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 36)
        ids = []
        expectations = set()
        for block in blocks:
            fields = dict(re.findall(r"^    (expect|prompt|evidence): (.+)$", block, re.MULTILINE))
            identifier = re.search(r"^  - id: (.+)$", block, re.MULTILINE)
            self.assertIsNotNone(identifier, block)
            self.assertEqual(set(fields), {"expect", "prompt", "evidence"}, block)
            ids.append(identifier.group(1))
            expectations.add(fields["expect"])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue({"trigger", "no_trigger", "safe_behavior", "workflow"} <= expectations)

    def test_completion_receipt_separates_evidence_states(self):
        for field in (
            "Changed:", "State:", "Plan:", "Tests/Checks:", "Security/Cost:",
            "Operations:", "Remaining:",
        ):
            self.assertIn(field, SKILL)
        self.assertIn("Do not declare success from an exit code alone", SKILL)

    def test_entrypoint_is_bounded(self):
        self.assertLessEqual(len(SKILL.splitlines()), 250)
        self.assertLessEqual(len(re.findall(r"\b[\w'-]+\b", SKILL)), 2000)


if __name__ == "__main__":
    unittest.main()
