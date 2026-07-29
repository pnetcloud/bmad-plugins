from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCE = ROOT / "references" / "api-contract-decisions.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    package = SKILL.read_text(encoding="utf-8") + "\n" + REFERENCE.read_text(encoding="utf-8")
    return " ".join(package.lower().replace("`", "").split())


class APIDesignerContractTests(unittest.TestCase):
    def test_frontmatter_trigger_and_nontrigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-api-designer\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("rest and graphql", "do not use", "implementation-only", "ui component apis"):
            self.assertIn(phrase, description)

    def test_reviewed_entrypoint_budget(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 250)
        self.assertLessEqual(len(text.split()), 1400)

    def test_progressive_disclosure_link(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("[api-contract-decisions.md](references/api-contract-decisions.md)", text)
        self.assertTrue(REFERENCE.is_file())

    def test_original_capability_families_remain(self):
        text = normalized()
        for phrase in (
            "api design checklist:",
            "rest design principles:",
            "graphql schema design:",
            "api versioning strategies:",
            "authentication patterns:",
            "documentation standards:",
            "performance optimization:",
            "error handling design:",
            "pagination patterns:",
            "search and filtering:",
            "bulk operations:",
            "webhook design:",
        ):
            self.assertIn(phrase, text)

    def test_original_specific_capabilities_remain(self):
        text = normalized()
        for phrase in (
            "exact repository- and tooling-supported openapi specification complete",
            "content negotiation",
            "idempotency guarantees",
            "union and interface usage",
            "federation considerations",
            "version sunset planning",
            "token refresh strategies",
            "sdk usage examples",
            "graphql query depth",
            "retry guidance",
            "faceted search",
            "partial success",
            "event ordering",
            "subscription management",
        ):
            self.assertIn(phrase, text)

    def test_no_fictional_context_or_completion(self):
        text = normalized()
        for phrase in (
            "request unavailable evidence directly",
            "do not imply access to a context manager",
            "never fabricate counts",
            "report only artifacts actually produced",
        ):
            self.assertIn(phrase, text)
        self.assertNotIn('"endpoints": 24', SKILL.read_text(encoding="utf-8"))
        self.assertNotIn("Generated SDKs for 5 languages", SKILL.read_text(encoding="utf-8"))

    def test_authority_and_evidence_boundaries(self):
        text = normalized()
        for phrase in (
            "design and review are read-only",
            "require explicit authority",
            "already-clean isolated checkout",
            "never clean, reset, overwrite, or switch",
            "distinct evidence states",
        ):
            self.assertIn(phrase, text)

    def test_rest_contract_semantics(self):
        text = normalized()
        for phrase in (
            "method idempotence does not prove",
            "stable total order",
            "authenticated cursor or an unguessable",
            "key scope, payload binding",
            "accepted request sets must not shrink",
            "emitted response sets must not expand",
        ):
            self.assertIn(phrase, text)

    def test_graphql_contract_semantics(self):
        text = normalized()
        for phrase in (
            "distinguish input and output types",
            "model nullability as a client contract",
            "top-level fields of a graphql mutation serially",
            "breadth, aliases, list sizes",
            "operation, object, and field boundary",
            "authentication renewal",
            "federation requires ownership",
        ):
            self.assertIn(phrase, text)

    def test_security_webhook_and_bulk_boundaries(self):
        text = normalized()
        for phrase in (
            "current oauth security best practice",
            "verifier choose an explicit algorithm allowlist",
            "mutually exclusive validation rules",
            "tokens out of urls and logs",
            "signature input and key rotation",
            "registration and every delivery",
            "not proof of downstream processing",
            "authorization per item",
            "safe mass-delete confirmation",
        ):
            self.assertIn(phrase, text)

    def test_validation_and_public_abstraction(self):
        text = normalized()
        for phrase in (
            "test at least one real consumer path",
            "isolated no-secret environment",
            "generated output or mock success alone",
            "use synthetic or composite examples",
            "do not claim sunset",
            "bounded opaque correlation identifier",
            "never expose stack traces",
        ):
            self.assertIn(phrase, text)

    def test_scenarios_are_complete_and_discriminating(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 36)
        identifiers = []
        expectations = set()
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
