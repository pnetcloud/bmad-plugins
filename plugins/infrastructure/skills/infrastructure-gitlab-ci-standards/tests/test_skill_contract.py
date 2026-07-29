from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    return " ".join(SKILL.read_text(encoding="utf-8").lower().replace("`", "").split())


class GitLabCIStandardsContractTests(unittest.TestCase):
    def test_frontmatter_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: infrastructure-gitlab-ci-standards\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("gitlab ci/cd", "do not use", "another ci provider"):
            self.assertIn(phrase, description)

    def test_entrypoint_is_concise(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 130)
        self.assertLessEqual(len(text.split()), 1500)

    def test_original_contract_is_literal(self):
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Define stages: lint -> test -> build -> deploy.",
            "Use `rules:` instead of `only/except` for clarity.",
            "Cache dependencies with proper keys.",
            "Store artifacts with expirations; limit retention.",
            "Use protected variables for secrets.",
            "Require pipeline green status before merge.",
        ):
            self.assertIn(phrase, text)

    def test_complete_configuration_and_authority(self):
        text = normalized()
        for phrase in (
            "complete configuration graph",
            "remove ambient credentials unconditionally",
            "isolated unprivileged runners",
            "automatically issued ci_job_token",
            "inbound and outbound allowlists",
            "require explicit authority",
            "emergency language does not widen authority",
        ):
            self.assertIn(phrase, text)

    def test_gitlab_semantics_are_explicit(self):
        text = normalized()
        for phrase in (
            "workflow:rules",
            "first-match order",
            "duplicate-pipeline behavior",
            "variable source, precedence, expansion",
            "masking is neither authorization nor containment",
            "typed inputs",
        ):
            self.assertIn(phrase, text)

    def test_cache_artifact_and_merge_boundaries(self):
        text = normalized()
        for phrase in (
            "disposable optimization",
            "sole carrier of a required build result",
            "immutable identity",
            "expire_in alone does not prove deletion",
            "keep-latest-successful policy",
            "full environment dumps",
            "green pipeline is necessary only",
            "stale or duplicate pipelines",
        ):
            self.assertIn(phrase, text)

    def test_evidence_states(self):
        text = normalized()
        for phrase in (
            "resolved syntax",
            "pipeline creation",
            "job selection",
            "job execution",
            "artifact identity",
            "rollout health",
            "ci lint proves configuration validity only",
        ):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 29)
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
