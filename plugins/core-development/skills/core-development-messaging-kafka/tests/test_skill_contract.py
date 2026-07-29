from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    return " ".join(SKILL.read_text(encoding="utf-8").lower().replace("`", "").split())


class KafkaStandardsContractTests(unittest.TestCase):
    def test_frontmatter_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-messaging-kafka\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("apache kafka-specific", "do not use", "another queue product"):
            self.assertIn(phrase, description)

    def test_entrypoint_is_concise(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 130)
        self.assertLessEqual(len(text.split()), 1500)

    def test_original_contract_is_literal(self):
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Design topics carefully: `domain.entity.event`.",
            "Always specify partitions and replication factor.",
            "Use a schema registry (Avro/JSON/Protobuf) for compatibility.",
            "Enable idempotent producers and safe configs for exactly-once.",
            "Consumer groups must commit offsets explicitly.",
            "Monitor lag and rebalance events.",
        ):
            self.assertIn(phrase, text)

    def test_complete_path_and_authority(self):
        text = normalized()
        for phrase in (
            "complete path",
            "require explicit authority",
            "confirm cluster, topic, group, partitions, offsets",
            "replays and offset resets are new writes",
            "untrusted code or data",
        ):
            self.assertIn(phrase, text)

    def test_topic_and_schema_semantics(self):
        text = normalized()
        for phrase in (
            "increasing partitions can change",
            "maximum useful consumers",
            "min.insync.replicas",
            "subject strategy",
            "registry acceptance proves",
        ):
            self.assertIn(phrase, text)

    def test_delivery_and_offset_boundaries(self):
        text = normalized()
        for phrase in (
            "idempotent-producer requirements",
            "does not make arbitrary external side effects",
            "stable unique transactional identity",
            "auto-commit disabled",
            "reset each consumer position to its last committed offset",
            "send the consumed offsets in the transaction",
            "without committing unprocessed records",
        ):
            self.assertIn(phrase, text)

    def test_rebalance_replay_and_observability(self):
        text = normalized()
        for phrase in (
            "on graceful revocation",
            "on partition loss, do not commit",
            "fence and discard stale work",
            "dead-letter topic is not completion",
            "time-to-catch-up",
            "a snapshot does not prove progress",
            "transaction fencing",
        ):
            self.assertIn(phrase, text)

    def test_evidence_states(self):
        text = normalized()
        for phrase in (
            "proposed config",
            "accepted schema",
            "created topic",
            "acknowledged record",
            "committed transaction",
            "processed side effect",
            "committed offset",
            "measured lag",
            "recovered workload",
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
