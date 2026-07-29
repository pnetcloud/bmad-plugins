from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized(path: Path) -> str:
    text = path.read_text(encoding="utf-8").lower().replace("`", "")
    return " ".join(text.split())


class DevOpsEngineerContractTests(unittest.TestCase):
    def test_frontmatter_and_precise_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: infrastructure-devops-engineer\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE)
        self.assertIsNotNone(description)
        value = description.group(1).lower()
        for phrase in ("ci/cd", "observability", "platform-engineering", "do not use"):
            self.assertIn(phrase, value)

    def test_entrypoint_is_bounded(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 380)
        self.assertLessEqual(len(text.split()), 1800)
        self.assertIn(
            "intentionally preserves the established capability catalog",
            text.lower(),
        )

    def test_all_linked_references_exist(self):
        text = SKILL.read_text(encoding="utf-8")
        links = re.findall(r"\]\((references/[^)]+\.md)\)", text)
        self.assertEqual(
            set(links),
            {
                "references/delivery-pipelines-and-artifacts.md",
                "references/infrastructure-platform-and-automation.md",
                "references/reliability-security-and-operations.md",
            },
        )
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)

    def test_long_references_have_navigation(self):
        for path in sorted((ROOT / "references").glob("*.md")):
            text = path.read_text(encoding="utf-8")
            if len(text.splitlines()) > 100:
                self.assertIn("## Contents", text, path.name)

    def test_fictional_protocol_and_metrics_are_absent(self):
        text = normalized(SKILL)
        for phrase in (
            "query context manager",
            '"automation_coverage": "94%"',
            "12 deployments/day",
            "25-minute mttr",
            "4.5/5",
            "transformation completed",
            "100% achieved",
            "> 80% coverage",
            "< 1 day",
            "> 99.9%",
        ):
            self.assertNotIn(phrase, text)

    def test_modes_and_remote_authority_are_explicit(self):
        text = normalized(SKILL)
        for phrase in (
            "establish the mode",
            "review and design are read-only",
            "before executing any repository-controlled command",
            "remove ambient credentials unconditionally",
            "require explicit authority",
            "triggering or cancelling pipelines",
            "publishing, promoting, signing, or deleting artifacts",
            "applying infrastructure",
            "deploying or rolling back",
            "changing traffic, dns, certificates, access, secrets, feature flags",
            "emergency language does not widen authority",
        ):
            self.assertIn(phrase, text)

    def test_original_capability_families_remain_reachable(self):
        package = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted(ROOT.rglob("*.md"))
        ).lower().replace("`", "")
        for phrase in (
            "terraform modules",
            "cloudformation templates",
            "ansible playbooks",
            "pulumi programs",
            "docker",
            "kubernetes",
            "helm",
            "service mesh",
            "gitops",
            "platform engineering",
            "self-service",
            "chatops",
            "distributed tracing",
            "sli",
            "slo",
            "incident response",
            "disaster recovery",
            "cost",
            "chargeback",
            "blameless",
            "hackathons",
            "open-source contribution",
        ):
            self.assertIn(phrase, package)

    def test_artifact_and_pipeline_evidence_are_bounded(self):
        package = normalized(SKILL) + normalized(
            ROOT / "references" / "delivery-pipelines-and-artifacts.md"
        )
        for phrase in (
            "untrusted contribution contexts",
            "immutable artifact identity",
            "provenance",
            "a valid workflow file is not an executed pipeline",
            "rollback as conditional",
            "serialize writers",
        ):
            self.assertIn(phrase, package)

    def test_delivery_metrics_are_not_universal_targets(self):
        text = normalized(SKILL) + " " + normalized(
            ROOT / "references" / "reliability-security-and-operations.md"
        )
        for phrase in (
            "deployment frequency",
            "change lead time",
            "failed-deployment recovery time",
            "change fail rate",
            "deployment rework rate",
            "not as cross-team rankings",
            "individual quotas",
            "universal targets",
        ):
            self.assertIn(phrase, text)

    def test_gitops_definition_is_complete(self):
        text = normalized(ROOT / "references" / "infrastructure-platform-and-automation.md")
        for phrase in (
            "desired state is declarative",
            "versioned with immutable history",
            "agents pull desired state",
            "continuously observe",
            "not automatically gitops",
        ):
            self.assertIn(phrase, text)

    def test_security_and_observability_limits_are_explicit(self):
        text = normalized(ROOT / "references" / "reliability-security-and-operations.md")
        for phrase in (
            "privacy,",
            "cardinality",
            "must not carry secrets",
            "one input, not security or compliance approval",
            "exceptions need owner, scope, reason, expiry",
            "blameless and evidence-based",
        ):
            self.assertIn(phrase, text)

    def test_completion_receipt_separates_evidence_states(self):
        text = normalized(SKILL) + " " + normalized(
            ROOT / "references" / "delivery-pipelines-and-artifacts.md"
        )
        for phrase in (
            "a passing build is not a deployable artifact",
            "a deployment command is not a healthy rollout",
            "artifact:",
            "operations:",
            "status:",
            "remaining:",
        ):
            self.assertIn(phrase, text)

    def test_scenario_vectors_have_complete_individual_contracts(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 49)
        ids = []
        expectations = set()
        for block in blocks:
            fields = dict(
                re.findall(
                    r"^    (expect|prompt|evidence): (.+)$",
                    block,
                    re.MULTILINE,
                )
            )
            identifier = re.search(r"^  - id: (.+)$", block, re.MULTILINE)
            self.assertIsNotNone(identifier, block)
            self.assertEqual(set(fields), {"expect", "prompt", "evidence"}, block)
            ids.append(identifier.group(1))
            expectations.add(fields["expect"])
            self.assertGreaterEqual(len(fields["prompt"].split()), 7, block)
            self.assertGreaterEqual(len(fields["evidence"].split()), 8, block)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(
            expectations,
            {"trigger", "no_trigger", "safe_behavior", "bounded_behavior", "workflow"},
        )


if __name__ == "__main__":
    unittest.main()
