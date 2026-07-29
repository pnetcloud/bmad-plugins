from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    return " ".join(SKILL.read_text(encoding="utf-8").lower().replace("`", "").split())


class PostgreSQLStandardsContractTests(unittest.TestCase):
    def test_frontmatter_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-database-postgresql\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("postgresql-specific", "do not use", "another database engine"):
            self.assertIn(phrase, description)

    def test_entrypoint_is_concise(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 130)
        self.assertLessEqual(len(text.split()), 1500)

    def test_original_contract_is_literal(self):
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Use `snake_case` for table and column names.",
            "Always define primary keys.",
            "Use foreign keys for integrity; avoid orphan rows.",
            "Prefer UUIDs for identifiers in distributed systems.",
            "Write explicit migrations; avoid destructive changes without backups.",
            "Monitor slow queries and add indexes based on query plans.",
        ):
            self.assertIn(phrase, text)

    def test_complete_contract_and_authority(self):
        text = normalized()
        for phrase in (
            "complete contract",
            "require explicit authority",
            "confirm target and transaction state",
            "lock and statement timeouts",
            "backup claim is evidence only",
        ):
            self.assertIn(phrase, text)

    def test_schema_semantics(self):
        text = normalized()
        for phrase in (
            "not null, unique, check",
            "foreign-key constraints",
            "check passes on true or null",
            "assumes its expression remains immutable",
            "cross-row invariants",
            "does not automatically index",
            "native uuid type",
            "do not replace a sound local identifier",
        ):
            self.assertIn(phrase, text)

    def test_migration_safety(self):
        text = normalized()
        for phrase in (
            "expand–migrate–contract",
            "not valid",
            "concurrent index construction",
            "backup is not permission",
            "mixed application versions",
        ):
            self.assertIn(phrase, text)

    def test_plan_and_index_evidence(self):
        text = normalized()
        for phrase in (
            "explain analyze executes",
            "does not undo every sequence or external effect",
            "does not exercise deferred-trigger behavior",
            "estimated cost is not measured production improvement",
            "operator class",
            "write amplification",
            "before and after plans",
        ):
            self.assertIn(phrase, text)

    def test_evidence_states(self):
        text = normalized()
        for phrase in (
            "proposed sql",
            "applied migration",
            "validated constraints",
            "observed query plan",
            "measured workload",
            "healthy rollout",
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
