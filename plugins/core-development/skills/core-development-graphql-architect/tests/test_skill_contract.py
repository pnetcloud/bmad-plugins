from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCE = ROOT / "references" / "graphql-decisions.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    text = SKILL.read_text(encoding="utf-8") + "\n" + REFERENCE.read_text(encoding="utf-8")
    return " ".join(text.lower().replace("`", "").split())


class GraphqlArchitectContractTests(unittest.TestCase):
    def test_frontmatter_trigger_and_nontriggers(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-graphql-architect\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("graphql schema", "resolvers", "federation", "do not use"):
            self.assertIn(phrase, description)

    def test_entrypoint_and_reference(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 300)
        self.assertLessEqual(len(text.split()), 1800)
        self.assertIn("[graphql-decisions.md](references/graphql-decisions.md)", text)
        self.assertTrue(REFERENCE.is_file())

    def test_original_capability_families_remain(self):
        text = normalized()
        for phrase in (
            "graphql architecture checklist:",
            "schema design principles:",
            "federation architecture:",
            "query optimization strategies:",
            "subscription implementation:",
            "type system mastery:",
            "schema validation:",
            "client considerations:",
            "schema evolution strategy:",
            "monitoring and observability:",
            "security implementation:",
            "testing methodology:",
            "integration with other agents:",
        ):
            self.assertIn(phrase, text)

    def test_original_workflow_and_handoffs_remain(self):
        text = normalized()
        for phrase in (
            "domain modeling",
            "schema implementation",
            "performance optimization",
            "entity relationship mapping",
            "subgraph schema creation",
            "dataloader integration",
            "federation_progress",
            "backend-developer",
            "api-designer",
            "microservices-architect",
            "frontend-developer",
            "database-optimizer",
            "security-auditor",
            "performance-engineer",
            "fullstack-developer",
        ):
            self.assertIn(phrase, text)

    def test_context_and_completion_are_evidence_bound(self):
        text = normalized()
        for phrase in (
            "do not imply access to a context manager",
            "decision surface",
            "separate current behavior",
            "report schema source edit",
            "never infer production readiness",
            "capability labels rather than guaranteed agents",
        ):
            self.assertIn(phrase, text)
        raw = SKILL.read_text(encoding="utf-8")
        self.assertNotIn('"request_type": "get_graphql_context"', raw)
        self.assertNotIn("Implemented 5 subgraphs with Apollo Federation 2.5", raw)

    def test_schema_contracts(self):
        text = normalized()
        for phrase in (
            "non-null field error propagates",
            "adding a required input field",
            "singular non-null input-object fields",
            "adding an emitted enum value",
            "mutation is not automatically atomic",
            "canonical operation and variables fingerprint",
            "cursor opacity and stability",
            "reject altered, expired, or cross-scope cursors",
            "partial data",
            "still a draft",
        ):
            self.assertIn(phrase, text)

    def test_performance_federation_and_security(self):
        text = normalized()
        for phrase in (
            "global dataloader can leak data",
            "depth alone is not a sufficient budget",
            "composition success alone does not prove",
            "directives as metadata",
            "introspection is defense in depth",
            "per-event revalidation",
            "minimal read-only inputs",
            "no network by default",
        ):
            self.assertIn(phrase, text)

    def test_authority_and_completion(self):
        text = normalized()
        for phrase in (
            "discovery and review are read-only",
            "require explicit authority",
            "disposable no-secret environment",
            "never clean, reset, overwrite, or switch",
            "published schema",
            "healthy release",
        ):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 45)
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
