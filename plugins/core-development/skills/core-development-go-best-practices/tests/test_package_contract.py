from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
REFERENCES = "\n".join(
    path.read_text(encoding="utf-8")
    for path in sorted((SKILL_DIR / "references").glob("*.md"))
)
SCENARIOS = json.loads(
    (SKILL_DIR / "tests" / "scenarios.json").read_text(encoding="utf-8")
)


class PackageContractTests(unittest.TestCase):
    def test_original_paths_and_routed_resources_exist(self) -> None:
        expected = {
            "SKILL.md",
            "skill-report.json",
            "references/types-interfaces-and-options.md",
            "references/errors-context-and-logging.md",
            "references/packages-tests-and-configuration.md",
            "tests/scenarios.json",
            "tests/test_package_contract.py",
        }
        for relative in expected:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL_DIR / relative).is_file())

    def test_entrypoint_is_compact_and_routes_all_resources(self) -> None:
        self.assertLessEqual(len(SKILL.splitlines()), 180)
        self.assertLessEqual(len(re.findall(r"\S+", SKILL)), 1500)
        for path in (
            "references/types-interfaces-and-options.md",
            "references/errors-context-and-logging.md",
            "references/packages-tests-and-configuration.md",
            "skill-report.json",
        ):
            with self.subTest(path=path):
                self.assertIn(f"]({path})", SKILL)

    def test_original_trigger_and_pattern_families_remain(self) -> None:
        frontmatter = SKILL.split("---", 2)[1].lower()
        for trigger in ("read", "write", "review", "go code", "go files"):
            with self.subTest(trigger=trigger):
                self.assertIn(trigger, frontmatter)
        for pattern in (
            "type-first",
            "custom types",
            "interfaces",
            "functional options",
            "errors",
            "context",
            "logging",
            "configuration",
            "modules",
            "tests",
        ):
            with self.subTest(pattern=pattern):
                self.assertIn(pattern, frontmatter)

    def test_every_baseline_topic_has_a_reachable_destination(self) -> None:
        topics = (
            "Contract-First Type Design",
            "Named Domain Primitives",
            "Consumer-Owned Interfaces",
            "Enum-Like Values",
            "Functional Options",
            "Embedding",
            "Receivers and Ownership",
            "Errors",
            "Switch and Failure Paths",
            "Panic and Recovery",
            "Context and Timeouts",
            "Goroutine Lifetimes",
            "Structured Logging",
            "Module and Package Structure",
            "Files and API Surface",
            "Tests and Tooling",
            "Typed Configuration",
            "Configuration Source Boundary",
        )
        for topic in topics:
            with self.subTest(topic=topic):
                self.assertIn(topic, REFERENCES)

    def test_dogmatic_absolutes_are_replaced_without_losing_patterns(self) -> None:
        combined = SKILL + "\n" + REFERENCES
        self.assertIn("consumer", combined.lower())
        self.assertIn("returning an interface", combined.lower())
        self.assertIn("there is no universal", combined.lower())
        self.assertIn("exhaustive-switch analyzer", combined)
        self.assertNotIn("one type or concern per file", combined)
        self.assertNotIn("Every function returns a value or an error", combined)
        self.assertNotIn("Panics crash the program", combined)

    def test_examples_preserve_and_harden_original_capabilities(self) -> None:
        for marker in (
            "type User struct",
            "type UserID string",
            "type UserRepository interface",
            "StatusActive",
            "type ServerOption",
            "type Timestamps struct",
            "fmt.Errorf(\"fetch widget: %w\"",
            "slog.Logger",
            "func TestParseStatus",
            "type Config struct",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, REFERENCES)
        self.assertIn("errors.Is", REFERENCES)
        self.assertIn("context.WithTimeout", REFERENCES)
        self.assertIn("caller owns `response.Body`", REFERENCES)
        self.assertIn("option == nil", REFERENCES)
        self.assertIn("happens-before relationship", SKILL + REFERENCES)
        self.assertIn("actual concurrent reads and writes", REFERENCES)
        self.assertNotIn('"widget_id"', REFERENCES)

    def test_public_configuration_example_has_no_concrete_source_keys(self) -> None:
        normalized = re.sub(r"\s+", " ", REFERENCES)
        self.assertNotIn("os.Getenv(", SKILL + REFERENCES)
        self.assertNotIn("os.LookupEnv(", SKILL + REFERENCES)
        self.assertIn("Keep concrete source keys", normalized)
        self.assertIn("without printing current values", normalized)

    def test_historical_report_is_valid_and_non_authoritative(self) -> None:
        report = json.loads(
            (SKILL_DIR / "skill-report.json").read_text(encoding="utf-8")
        )
        self.assertEqual("historical-upstream-snapshot", report["meta"]["scope"])
        self.assertIn("not current Go guidance", report["meta"]["review_notice"])
        for key in (
            "actual_capabilities",
            "limitations",
            "use_cases",
            "prompt_templates",
            "output_examples",
            "best_practices",
            "anti_patterns",
            "faq",
        ):
            with self.subTest(key=key):
                self.assertTrue(report["content"][key])

    def test_scenarios_cover_required_dimensions(self) -> None:
        required = {"id", "tags", "given", "require", "forbid"}
        ids = [scenario["id"] for scenario in SCENARIOS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(set(scenario) == required for scenario in SCENARIOS))
        tags = {tag for scenario in SCENARIOS for tag in scenario["tags"]}
        self.assertTrue(
            {"positive-trigger", "negative-trigger", "main-task", "safety"} <= tags
        )


if __name__ == "__main__":
    unittest.main()
