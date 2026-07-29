from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").lower().replace("`", "").split())


class CloudArchitectContractTests(unittest.TestCase):
    def test_frontmatter_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: infrastructure-cloud-architect\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("aws", "azure", "google cloud", "do not use", "terraform"):
            self.assertIn(phrase, description)

    def test_entrypoint_budget_preserves_catalog(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 360)
        self.assertLessEqual(len(text.split()), 1800)
        self.assertGreaterEqual(len(text.splitlines()), 275)

    def test_references(self):
        links = re.findall(r"\]\((references/[^)]+\.md)\)", SKILL.read_text())
        self.assertEqual(len(set(links)), 3)
        for link in links:
            self.assertTrue((ROOT / link).is_file())

    def test_fictional_protocol_and_metrics_absent(self):
        text = normalized(SKILL)
        for phrase in ("query context manager", "50m requests/day", '"workloads_migrated": 24', '"cost_reduction": "42%"', "compliance_score", "cost optimization > 30%"):
            self.assertNotIn(phrase, text)

    def test_authority_and_evidence(self):
        text = normalized(SKILL)
        for phrase in ("review, assessment, and design are read-only", "never infer a production target", "remove ambient credentials unconditionally", "live reads can disclose", "require explicit authority", "emergency language does not widen authority", "a clean plan is not an applied change"):
            self.assertIn(phrase, text)

    def test_capability_catalogs_remain(self):
        text = "\n".join(p.read_text() for p in sorted(ROOT.rglob("*.md"))).lower()
        for phrase in ("multi-cloud strategy", "well-architected framework", "reserved instance planning", "zero-trust principles", "rto/rpo definitions", "6rs assessment", "function architectures", "event-driven design", "data lake design", "ml/ai infrastructure", "hybrid cloud", "landing zone design", "vpc/vnet design", "gpu workloads", "object storage tiers", "distributed tracing"):
            self.assertIn(phrase, text)

    def test_all_handoffs_remain(self):
        text = normalized(SKILL)
        for phrase in ("guide devops-engineer", "support sre-engineer", "collaborate with security-engineer", "work with network-engineer", "help kubernetes-specialist", "assist terraform-engineer", "partner with database-administrator", "coordinate with platform-engineer"):
            self.assertIn(phrase, text)

    def test_reliability_migration_limits(self):
        text = normalized(ROOT / "references" / "workloads-reliability-and-migration.md")
        for phrase in ("availability is an observed outcome", "multi-cloud is not automatically resilient", "current aws guidance uses 7 rs", "completed transfer is not a completed migration", "decommission only with separate authority"):
            self.assertIn(phrase, text)

    def test_frameworks_are_not_flattened_across_providers(self):
        text = normalized(SKILL)
        for phrase in ("exact provider", "framework revision", "non-equivalent pillar mapping"):
            self.assertIn(phrase, text)

    def test_security_governance_limits(self):
        text = normalized(ROOT / "references" / "landing-zones-security-networking-and-governance.md")
        for phrase in ("not as a completion label", "architecture can support compliance", "must not independently certify", "successful control-plane request is not proof"):
            self.assertIn(phrase, text)

    def test_cost_delivery_limits(self):
        text = normalized(ROOT / "references" / "data-cost-observability-and-delivery.md")
        for phrase in ("potential saving before implementation", "realized comparable outcome", "plans can become stale", "do not borrow recipient approval"):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 52)
        ids, expectations = [], set()
        for block in blocks:
            identifier = re.search(r"^  - id: (.+)$", block, re.MULTILINE).group(1)
            fields = dict(re.findall(r"^    (expect|prompt|evidence): (.+)$", block, re.MULTILINE))
            self.assertEqual(set(fields), {"expect", "prompt", "evidence"})
            self.assertGreaterEqual(len(fields["prompt"].split()), 7)
            self.assertGreaterEqual(len(fields["evidence"].split()), 8)
            ids.append(identifier)
            expectations.add(fields["expect"])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(expectations, {"trigger", "no_trigger", "safe_behavior", "bounded_behavior", "workflow"})


if __name__ == "__main__":
    unittest.main()
