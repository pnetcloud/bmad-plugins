from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCE = ROOT / "references" / "fullstack-decisions.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    text = SKILL.read_text(encoding="utf-8") + "\n" + REFERENCE.read_text(encoding="utf-8")
    return " ".join(text.lower().replace("`", "").split())


class FullstackDeveloperContractTests(unittest.TestCase):
    def test_frontmatter_trigger_and_nontriggers(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-fullstack-developer\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("two or more application layers", "end-to-end contracts", "do not use", "isolated to one layer"):
            self.assertIn(phrase, description)

    def test_entrypoint_structural_exception_and_reference(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 300)
        self.assertLessEqual(len(text.split()), 1800)
        self.assertIn("[fullstack-decisions.md](references/fullstack-decisions.md)", text)
        self.assertTrue(REFERENCE.is_file())

    def test_original_capability_families_remain(self):
        text = normalized()
        for phrase in (
            "fullstack development checklist:",
            "data flow architecture:",
            "cross-stack authentication:",
            "real-time implementation:",
            "testing strategy:",
            "architecture decisions:",
            "performance optimization:",
            "deployment pipeline:",
            "technology selection matrix:",
            "shared code management:",
            "feature specification approach:",
            "integration patterns:",
            "integration with other agents:",
        ):
            self.assertIn(phrase, text)

    def test_original_cross_layer_workflow_remains(self):
        text = normalized()
        for phrase in (
            "database schema aligned with api contracts",
            "type-safe api implementation with shared types",
            "frontend components matching backend capabilities",
            "authentication flow spanning all layers",
            "end-to-end testing covering user journeys",
            "optimistic updates with proper rollback",
            "consistent validation rules throughout",
            "conflict resolution strategies",
        ):
            self.assertIn(phrase, text)

    def test_no_fictional_context_or_completion(self):
        text = normalized()
        for phrase in (
            "do not imply access to a context manager",
            "lists as decision surfaces",
            "never substitute a fictional stack",
            "production readiness only when",
            "capability labels, not guaranteed agents",
        ):
            self.assertIn(phrase, text)
        raw = SKILL.read_text(encoding="utf-8")
        self.assertNotIn('"request_type": "get_fullstack_context"', raw)
        self.assertNotIn("Implemented complete user management system with PostgreSQL", raw)

    def test_contract_data_and_concurrency(self):
        text = normalized()
        for phrase in (
            "required, optional, nullable, omitted",
            "expand, backfill, validate",
            "transaction boundaries and isolation",
            "outbox or equivalent publication strategy",
            "idempotency keys",
            "do not shrink accepted request",
            "do not expand emitted enum values",
            "canonical request fingerprint",
            "cache ownership",
        ):
            self.assertIn(phrase, text)

    def test_security_and_integration(self):
        text = normalized()
        for phrase in (
            "feature flags improve ux but are not authorization",
            "csrf defense",
            "verifier-controlled validation rules",
            "prevent access, refresh, identity",
            "row security",
            "identity matrix",
            "rejecting absolute and traversal paths",
            "deny loopback, private, link-local",
            "disposable no-secret environment",
            "local update is not durable success",
            "resume cursor",
        ):
            self.assertIn(phrase, text)

    def test_authority_testing_and_completion(self):
        text = normalized()
        for phrase in (
            "discovery and review are read-only",
            "require explicit authority",
            "never clean, reset, overwrite, or switch",
            "separate evidence states",
            "never infer production readiness",
        ):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 43)
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
