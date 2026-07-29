from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    return " ".join(SKILL.read_text(encoding="utf-8").lower().replace("`", "").split())


class TimescaleDBStandardsContractTests(unittest.TestCase):
    def test_frontmatter_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-database-timescaledb\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("timescaledb-specific", "do not use", "core postgresql"):
            self.assertIn(phrase, description)

    def test_entrypoint_is_concise(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 130)
        self.assertLessEqual(len(text.split()), 1500)

    def test_original_contract_is_literal(self):
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Use hypertables for time-series data.",
            "Set chunk interval based on data rate (for example, 1 day).",
            "Create continuous aggregates for rollups.",
            "Use compression for older chunks to save space.",
            "Monitor chunk sizes and adjust retention policies.",
            "Always index the time column and foreign keys.",
        ):
            self.assertIn(phrase, text)

    def test_complete_contract_and_authority(self):
        text = normalized()
        for phrase in (
            "complete contract",
            "require explicit authority",
            "confirm target and transaction state",
            "retention and chunk drops are destructive",
            "verify version-specific apis",
        ):
            self.assertIn(phrase, text)

    def test_hypertable_and_chunk_semantics(self):
        text = normalized()
        for phrase in (
            "do not convert a plain postgresql table",
            "one-day interval is an example",
            "future chunks",
            "generated during hypertable creation",
            "every partitioning dimension",
        ):
            self.assertIn(phrase, text)

    def test_aggregate_semantics(self):
        text = normalized()
        for phrase in (
            "acceptable staleness",
            "refresh window",
            "late arrivals",
            "real-time behavior",
            "not dropped before required refresh",
        ):
            self.assertIn(phrase, text)

    def test_storage_and_retention_safety(self):
        text = normalized()
        for phrase in (
            "compression or columnstore model",
            "row-level-security support",
            "cannot preserve the hypertable's access contract",
            "segment and order keys",
            "does not prove every eligible chunk",
            "retention as a data-lifecycle contract",
            "do not infer deletion",
        ):
            self.assertIn(phrase, text)

    def test_evidence_states(self):
        text = normalized()
        for phrase in (
            "proposed sql",
            "created object",
            "scheduled policy",
            "successful job run",
            "measured query or ingest workload",
            "retained data boundary",
            "healthy rollout",
        ):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 28)
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
