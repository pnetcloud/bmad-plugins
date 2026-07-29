import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = ROOT / "tests" / "scenarios.json"
TEXT = SKILL.read_text(encoding="utf-8")
NORMALIZED = " ".join(TEXT.split()).lower()


class GolangProContractTests(unittest.TestCase):
    def test_original_entrypoint_and_identity_are_retained(self):
        self.assertTrue(SKILL.is_file())
        self.assertRegex(TEXT, r"(?m)^name: language-specialists-golang-pro$")

    def test_trigger_and_non_trigger_are_explicit(self):
        match = re.search(r"(?ms)^---\n.*?^description: (.+?)\n---$", TEXT)
        self.assertIsNotNone(match)
        description = match.group(1)
        for phrase in (
            "Go code",
            "concurrency",
            "gRPC",
            "databases",
            "CGO",
            "non-Go implementation",
        ):
            self.assertIn(phrase, description)

    def test_fictional_protocol_and_fabricated_results_are_absent(self):
        for phrase in (
            "query context manager",
            '"request_type": "get_golang_context"',
            "tests_written\": 47",
            "coverage\": \"87%",
            "sub-millisecond p99",
            "89% coverage",
            "50% performance improvement",
            "zero race conditions detected",
        ):
            self.assertNotIn(phrase.lower(), NORMALIZED)

    def test_original_capability_families_remain_reachable(self):
        families = {
            "language": ("gofmt", "golangci-lint", "functional options", "embedding", "reflection"),
            "concurrency": ("goroutine", "channel", "mutex", "atomic", "worker pools", "backpressure"),
            "errors": ("wrapped errors", "sentinel errors", "panic", "graceful degradation"),
            "performance": ("pprof", "benchmark", "sync.Pool", "escape analysis", "garbage collection"),
            "testing": ("table-driven", "golden files", "fuzzing", "race detector", "integration"),
            "services": ("gRPC", "REST", "circuit", "health checks", "graceful shutdown"),
            "cloud": ("Kubernetes", "service mesh", "serverless", "event-driven", "message queue"),
            "tooling": ("build tags", "cross-compilation", "CGO", "go generate", "multi-stage"),
            "grpc": ("streaming", "interceptor", "metadata", "load balancing", "TLS", "protocol buffer"),
            "data": ("connection pool", "prepared statement", "transaction", "migration", "NoSQL", "query optimization"),
            "observability": ("slog", "Prometheus", "distributed tracing", "dashboard", "alert"),
            "security": ("input validation", "SQL injection", "authentication", "authorization", "credential", "vulnerability"),
            "handoffs": ("consumers", "backend owners", "operations", "platform owners", "bindings", "architecture owners"),
        }
        for family, phrases in families.items():
            with self.subTest(family=family):
                for phrase in phrases:
                    self.assertIn(phrase.lower(), NORMALIZED)

    def test_context_and_concurrency_guidance_is_qualified(self):
        for required in (
            "without storing it in structs",
            "caller-owned context",
            "happens-before",
            "clean run is not proof",
            "goroutine ownership and termination",
        ):
            self.assertIn(required.lower(), NORMALIZED)

    def test_read_only_modes_and_repository_tooling_take_precedence(self):
        for required in (
            "for review, diagnosis, explanation, or design, remain read-only",
            "when edits are authorized",
            "repository's configured lint/static-analysis contract",
            "do not introduce `golangci-lint` solely to satisfy this skill",
            "repository-selected logger",
            "only when the declared toolchain and logging contract support it",
        ):
            self.assertIn(required.lower(), NORMALIZED)

    def test_service_controller_and_data_boundaries_are_explicit(self):
        for required in (
            "flow control/backpressure",
            "half-close",
            "grpc status codes/details",
            "commit ambiguity",
            "status/observed state",
            "no raw errors, request ids, secrets, or personal data in labels",
        ):
            self.assertIn(required.lower(), NORMALIZED)

    def test_performance_and_quality_claims_require_evidence(self):
        for required in (
            "measured hot paths",
            "active toolchain",
            "no universal percentage",
            "workload, build/toolchain, sample method, baseline, result, and variance",
            "stop at the verified boundary",
        ):
            self.assertIn(required.lower(), NORMALIZED)
        self.assertNotIn("test coverage > 80%", NORMALIZED)

    def test_security_and_external_authority_are_bounded(self):
        for required in (
            "never embed, print, or invent secret values",
            "do not silently downgrade",
            "transport credentials and identity",
            "trust, loading, versioning, and failure boundaries",
            "runtime, credentials, deployment, or external systems are unavailable",
        ):
            self.assertIn(required.lower(), NORMALIZED)

    def test_scenarios_cover_activation_safety_and_retention(self):
        scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        names = {scenario["name"] for scenario in scenarios}
        required = {
            "positive-go-trigger",
            "negative-language-neutral-architecture",
            "missing-context",
            "concurrent-state",
            "performance-claim",
            "race-detector-boundary",
            "grpc-stream",
            "operator-reconcile",
            "credential-and-deployment",
            "truthful-progress",
            "retention",
        }
        self.assertTrue(required.issubset(names))
        self.assertEqual(len(names), len(scenarios))
        self.assertGreaterEqual(len(scenarios), 16)
        for scenario in scenarios:
            self.assertTrue(scenario["prompt"].strip())
            self.assertTrue(scenario["expect"])

    def test_structural_exception_is_bounded(self):
        lines = TEXT.count("\n") + 1
        words = len(TEXT.split())
        self.assertLessEqual(lines, 300)
        self.assertLessEqual(words, 1800)


if __name__ == "__main__":
    unittest.main()
