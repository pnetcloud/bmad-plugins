from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    return " ".join(SKILL.read_text(encoding="utf-8").lower().replace("`", "").split())


class DevOpsStandardsContractTests(unittest.TestCase):
    def test_frontmatter_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: infrastructure-devops-standards\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("gitlab ci/cd", "configuration-management", "do not use", "terraform"):
            self.assertIn(phrase, description)

    def test_entrypoint_is_concise(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 140)
        self.assertLessEqual(len(text.split()), 1400)

    def test_original_contract_is_literal(self):
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Use YAML pipelines with modular, reusable configurations.",
            "Include stages for build, test, security scans, and deployment.",
            "Implement gated deployments and rollback mechanisms.",
            "Prefer Terraform for IaC.",
            "Use Ansible only when explicitly needed and documented.",
            "Test pipelines in sandbox environments.",
            "Write unit tests for custom scripts or code with mocking for cloud APIs.",
        ):
            self.assertIn(phrase, text)

    def test_authority_and_execution_boundaries(self):
        text = normalized()
        for phrase in (
            "review and proposal are read-only",
            "remove ambient credentials unconditionally",
            "untrusted contribution pipelines",
            "require explicit authority",
            "emergency language does not widen authority",
        ):
            self.assertIn(phrase, text)

    def test_evidence_states_are_distinct(self):
        text = normalized()
        for phrase in (
            "ci lint establishes configuration validity only",
            "a created pipeline is not a passing pipeline",
            "a passing pipeline is not a verified artifact",
            "a deployment command is not a healthy rollout",
        ):
            self.assertIn(phrase, text)

    def test_configuration_tools_are_conditional(self):
        text = normalized()
        for phrase in (
            "repository's established iac tool",
            "state, locking, identity, import, drift",
            "ordered host or application configuration",
            "second source of truth",
            "clean plan can become stale",
        ):
            self.assertIn(phrase, text)

    def test_testing_layers_are_not_overclaimed(self):
        text = normalized()
        for phrase in (
            "mocks for deterministic unit boundaries",
            "not as proof of provider",
            "authorized isolated target",
            "residual-state reconciliation",
            "user-facing signals",
        ):
            self.assertIn(phrase, text)

    def test_untrusted_runners_caches_and_variables_are_precise(self):
        text = normalized()
        for phrase in (
            "isolated unprivileged runners",
            "trust-scoped disposable caches",
            "protected or privileged runners",
            "trusted release caches",
            "variable source, precedence, expansion",
            "forwarding into downstream pipelines",
            "masking is neither authorization nor containment",
        ):
            self.assertIn(phrase, text)

    def test_scenarios_are_complete(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 25)
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
