from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    return " ".join(SKILL.read_text(encoding="utf-8").lower().replace("`", "").split())


class OpenAPIStandardsContractTests(unittest.TestCase):
    def test_frontmatter_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-openapi-standards\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("openapi-specific", "do not use", "another interface-description format"):
            self.assertIn(phrase, description)

    def test_entrypoint_is_concise(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 130)
        self.assertLessEqual(len(text.split()), 1500)

    def test_original_contract_is_literal(self):
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Keep API schemas as the source of truth.",
            "Use OpenAPI 3.x format.",
            "Document all endpoints, params, request/response bodies, and error codes.",
            "Provide examples for each endpoint.",
            "Use tags to organize endpoints logically.",
            "Generate docs and clients automatically from schemas.",
            "Validate schema changes in CI.",
        ):
            self.assertIn(phrase, text)

    def test_graph_and_authority(self):
        text = normalized()
        for phrase in (
            "complete contract graph",
            "bound reference resolution",
            "require explicit authority",
            "confirm source revision, artifact, destination",
            "stable paths, methods, operation ids",
        ):
            self.assertIn(phrase, text)

    def test_version_operation_and_security_semantics(self):
        text = normalized()
        for phrase in (
            "do not mix 3.0 and 3.1",
            "every public path operation, webhook, and callback",
            "allof combines independent constraints",
            "or alternatives",
            "and requirements",
            "empty security: []",
        ):
            self.assertIn(phrase, text)

    def test_examples_and_generation_safety(self):
        text = normalized()
        for phrase in (
            "synthetic, schema-valid",
            "tags improve navigation",
            "pinned, inspected tools",
            "never execute generated code",
            "successful generation does not prove",
        ):
            self.assertIn(phrase, text)

    def test_validation_and_evidence(self):
        text = normalized()
        for phrase in (
            "consumer-aware compatibility diff",
            "already-clean isolated checkout",
            "never clean, reset, overwrite, or switch",
            "authored source",
            "resolved or bundled graph",
            "generated artifact",
            "deployed runtime behavior",
            "released client",
        ):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 27)
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
