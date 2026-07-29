from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCE = ROOT / "references" / "frontend-decisions.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    package = SKILL.read_text(encoding="utf-8") + "\n" + REFERENCE.read_text(encoding="utf-8")
    return " ".join(package.lower().replace("`", "").split())


class FrontendDeveloperContractTests(unittest.TestCase):
    def test_frontmatter(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-frontend-developer\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("browser ui implementation", "do not use", "design-only", "backend-only"):
            self.assertIn(phrase, description)

    def test_entrypoint_budget_and_reference(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 180)
        self.assertLessEqual(len(text.split()), 1500)
        self.assertIn("[frontend-decisions.md](references/frontend-decisions.md)", text)
        self.assertTrue(REFERENCE.is_file())

    def test_original_capability_families(self):
        text = normalized()
        for phrase in (
            "typescript configuration:",
            "real-time features:",
            "documentation requirements:",
            "deliverables organized by type:",
            "component scaffolding with typescript interfaces",
            "implementing responsive layouts and interactions",
            "integrating with existing state management",
            "writing tests alongside implementation",
            "ensuring accessibility from the start",
        ):
            self.assertIn(phrase, text)

    def test_no_fixed_version_coverage_or_fictional_context(self):
        text = normalized()
        for phrase in (
            "resolve the repository's exact framework",
            "do not imply access to a context manager",
            "populate status fields only with observable work",
            "repository-required behavior and coverage evidence",
            "never fabricate coverage",
        ):
            self.assertIn(phrase, text)
        raw = SKILL.read_text(encoding="utf-8")
        self.assertNotIn("React 18+", raw)
        self.assertNotIn("90% test coverage", raw)

    def test_components_state_and_rendering(self):
        text = normalized()
        for phrase in (
            "controlled versus uncontrolled behavior",
            "keep render or template evaluation pure",
            "narrowest owner",
            "stable semantic identity",
            "server/client, ssr/ssg/csr",
        ):
            self.assertIn(phrase, text)

    def test_data_forms_routing_and_realtime(self):
        text = normalized()
        for phrase in (
            "treat external data as untrusted",
            "push from replace",
            "duplicate submission",
            "temporary identity",
            "resume cursor",
            "presence is observation",
        ):
            self.assertIn(phrase, text)

    def test_accessibility_i18n_and_security(self):
        text = normalized()
        for phrase in (
            "applicable accessibility standard",
            "bounded signal, not conformance proof",
            "long/translated text",
            "do not concatenate translatable sentence fragments",
            "prevent dom xss",
            "feature flags need safe defaults",
        ):
            self.assertIn(phrase, text)

    def test_performance_testing_and_authority(self):
        text = normalized()
        for phrase in (
            "profile before memoizing",
            "bundle analysis is evidence about bytes",
            "coverage is a diagnostic",
            "already-clean isolated checkout",
            "never clean, reset, overwrite, or switch",
            "confirm active identity",
        ):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 41)
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

    def test_conditional_typescript_and_collaboration(self):
        text = normalized()
        for phrase in (
            "typescript does not provide runtime polyfills",
            "generate declaration files only for library or module consumers",
            "capability labels, not guaranteed agents",
            "report the unresolved evidence or owner gap",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
