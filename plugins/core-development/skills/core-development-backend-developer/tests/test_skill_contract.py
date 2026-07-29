from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized(value):
    return " ".join(value.split())


class BackendDeveloperContractTests(unittest.TestCase):
    def test_frontmatter_and_precise_trigger(self):
        self.assertTrue(SKILL.startswith("---\nname: core-development-backend-developer\n"))
        description = re.search(r"^description: (.+)$", SKILL, re.MULTILINE).group(1)
        for phrase in ("Implement", "review", "debug", "do not use"):
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
        package = normalized("\n".join(
            path.read_text(encoding="utf-8")
            for path in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
        )).lower()
        families = (
            "openapi", "pagination", "cors", "rate limit", "migration",
            "connection pool", "read-after-write", "backup", "authentication",
            "authorization", "ssrf", "cache", "load test", "contract test",
            "circuit breaker", "service discovery", "saga", "dead-letter",
            "priority queue", "replay", "distributed tracing", "health",
            "graceful shutdown", "feature flags", "rollback", "owasp", "rbac",
            "multi-stage build",
        )
        for family in families:
            self.assertIn(family, package, family)

    def test_no_fictional_context_protocol_or_stack(self):
        forbidden = (
            "query context manager",
            '"requesting_agent"',
            '"request_type"',
            "go/gin",
            "achieved 88%",
            "sub-100ms",
            "test coverage exceeding",
        )
        lowered = normalized(SKILL).lower()
        for phrase in forbidden:
            self.assertNotIn(phrase, lowered)

    def test_modes_and_authority_are_explicit(self):
        for phrase in (
            "Review and design are read-only",
            "diagnosis does not silently become a fix",
            "without explicit authority",
        ):
            self.assertIn(phrase, normalized(SKILL))

    def test_no_universal_metric_or_coverage_target(self):
        self.assertNotRegex(SKILL, r"\b(?:80|88|100)\s*%")
        self.assertIn("Coverage is diagnostic evidence", SKILL)
        self.assertIn("task-specific budgets rather than universal targets", SKILL)

    def test_security_boundaries_cover_object_and_upstream_trust(self):
        reference = (ROOT / "references" / "security-reliability-and-testing.md").read_text()
        for phrase in (
            "specific action, object, field, tenant",
            "server-initiated requests",
            "Treat upstream APIs as untrusted",
            "Keep secrets out of source",
        ):
            self.assertIn(phrase, reference)

    def test_data_failure_semantics_are_not_blind_retries(self):
        reference = (ROOT / "references" / "api-and-data.md").read_text()
        self.assertIn("uncertain commit outcomes", reference)
        self.assertIn("do not blindly retry", reference)
        self.assertIn("source of truth", reference)
        self.assertIn("read-after-write", reference)

    def test_messaging_contract_is_end_to_end(self):
        reference = (
            ROOT / "references" / "distributed-systems-and-messaging.md"
        ).read_text()
        for phrase in (
            "acknowledgement point",
            "side-effect deduplication",
            "Exactly once",
            "Replay is a privileged write operation",
            "Bound in-flight messages",
        ):
            self.assertIn(phrase, reference)

    def test_completion_receipt_separates_evidence_states(self):
        for field in (
            "Changed:", "Contracts:", "Tests:", "Performance:",
            "Security:", "Operations:", "Remaining:",
        ):
            self.assertIn(field, SKILL)
        self.assertIn(
            "does not prove deployment or production behavior", normalized(SKILL)
        )

    def test_each_scenario_vector_has_a_complete_contract(self):
        # These are structural vectors. Actual model behavior is evaluated
        # independently and recorded in the local improvement receipt.
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 25)
        ids = []
        expectations = set()
        for block in blocks:
            fields = dict(
                re.findall(
                    r"^    (expect|prompt|evidence): (.+)$", block, re.MULTILINE
                )
            )
            identifier = re.search(r"^  - id: (.+)$", block, re.MULTILINE)
            self.assertIsNotNone(identifier, block)
            self.assertEqual(set(fields), {"expect", "prompt", "evidence"}, block)
            self.assertTrue(all(value.strip() for value in fields.values()), block)
            ids.append(identifier.group(1))
            expectations.add(fields["expect"])
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(
            {"trigger", "no_trigger", "safe_behavior", "workflow"}
            <= expectations
        )

    def test_testing_and_handoff_families_are_explicit(self):
        package = normalized(
            SKILL
            + (ROOT / "references" / "security-reliability-and-testing.md").read_text()
        )
        for phrase in (
            "endpoint integration tests",
            "database transaction tests",
            "authentication-flow tests",
            "implemented endpoints",
            "schemas, queries, migrations",
            "built artifact",
            "benchmark method, baseline, result",
        ):
            self.assertIn(phrase, package)

    def test_entrypoint_is_bounded(self):
        lines = SKILL.splitlines()
        words = re.findall(r"\b[\w'-]+\b", SKILL)
        self.assertLessEqual(len(lines), 250)
        self.assertLessEqual(len(words), 2000)


if __name__ == "__main__":
    unittest.main()
