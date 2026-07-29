from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
SCENARIOS = json.loads(
    (SKILL_DIR / "tests" / "scenarios.json").read_text(encoding="utf-8")
)


class PackageContractTests(unittest.TestCase):
    def test_original_paths_and_new_routed_resources_exist(self) -> None:
        expected = {
            "SKILL.md",
            "skill-report.json",
            "references/components-and-styling.md",
            "references/data-routing-and-states.md",
            "references/typescript-and-performance.md",
            "references/templates-and-structure.md",
            "tests/scenarios.json",
            "tests/test_package_contract.py",
        }
        for relative in expected:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL_DIR / relative).is_file())

    def test_entrypoint_is_compact_and_routes_every_topic(self) -> None:
        self.assertLessEqual(len(SKILL.splitlines()), 180)
        self.assertLessEqual(len(re.findall(r"\S+", SKILL)), 1500)
        for reference in (
            "components-and-styling.md",
            "data-routing-and-states.md",
            "typescript-and-performance.md",
            "templates-and-structure.md",
            "skill-report.json",
        ):
            with self.subTest(reference=reference):
                path = reference if reference == "skill-report.json" else f"references/{reference}"
                self.assertIn(f"]({path})", SKILL)

    def test_legacy_trigger_and_framework_families_remain(self) -> None:
        frontmatter = SKILL.split("---", 2)[1]
        for value in (
            "Next.js",
            "React",
            "TypeScript",
            "components",
            "pages",
            "file organization",
            "data fetching",
            "styling",
            "routing",
            "컴포넌트",
            "파일 구조",
            "데이터 페칭",
            "스타일링",
            "라우팅",
        ):
            with self.subTest(value=value):
                self.assertIn(value, frontmatter)

    def test_baseline_topic_families_have_reachable_destinations(self) -> None:
        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((SKILL_DIR / "references").glob("*.md"))
        )
        expected_topics = (
            "New Component Checklist",
            "New Page Checklist",
            "Import Aliases",
            "Common Imports",
            "Server Component Pattern",
            "Client Component Pattern",
            "Server Data Reads",
            "Server Actions and Mutations",
            "File Organization Alternatives",
            "Tailwind CSS and Conditional Classes",
            "App Router Structure",
            "Loading UI and Suspense",
            "Error Boundaries",
            "Performance Workflow",
            "Image Pattern",
            "Suspense Pattern",
            "TypeScript Contract",
            "Forms",
            "Metadata",
            "Server Component Template",
            "Client Component Template",
        )
        for topic in expected_topics:
            with self.subTest(topic=topic):
                self.assertIn(topic, combined)

    def test_stale_absolutes_are_replaced_with_project_and_version_gates(self) -> None:
        combined = SKILL + "\n" + "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((SKILL_DIR / "references").glob("*.md"))
        )
        self.assertIn("installed Next.js version", combined)
        self.assertIn("project owns that code", combined)
        self.assertIn("project choices, not universal rules", combined)
        self.assertIn("optimizations, not", combined)
        self.assertNotIn("components/ui/: Shadcn/ui components (don't modify directly)", combined)
        self.assertNotIn("Components are already styled and accessible", combined)

    def test_mutation_cache_and_evidence_boundaries_are_explicit(self) -> None:
        data = (
            SKILL_DIR / "references" / "data-routing-and-states.md"
        ).read_text(encoding="utf-8")
        performance = (
            SKILL_DIR / "references" / "typescript-and-performance.md"
        ).read_text(encoding="utf-8")
        normalized_data = re.sub(r"\s+", " ", data.lower())
        for contract in (
            "Authenticate the actor",
            "authorization inside the mutation",
            "freshness, cache, revalidation, and invalidation",
            "Validate again on the trusted server boundary",
        ):
            with self.subTest(contract=contract):
                self.assertIn(contract.lower(), normalized_data)
        self.assertIn("production-like baseline", performance)
        self.assertIn("Re-measure", performance)
        self.assertIn("useActionState", data)
        self.assertIn("durable uniqueness", data)
        self.assertIn("test that replay", data)
        self.assertIn("state.issues?.title", data)
        self.assertIn("state.issues?.content", data)
        self.assertIn("state.issues?.submissionId", data)
        self.assertNotIn("return { ok: false", data)

    def test_historical_report_remains_valid_and_non_authoritative(self) -> None:
        report = json.loads(
            (SKILL_DIR / "skill-report.json").read_text(encoding="utf-8")
        )
        self.assertEqual("2.0", report["schema_version"])
        self.assertEqual("historical-upstream-snapshot", report["meta"]["scope"])
        self.assertIn("not current framework guidance", report["meta"]["review_notice"])
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
        data_safety = next(
            item
            for item in report["content"]["faq"]
            if item["question"] == "Is my data safe when using Server Components?"
        )
        self.assertEqual("rejected-unsafe-absolute", data_safety["review_status"])
        self.assertIn("Data never leaves your server", data_safety["historical_answer"])
        self.assertIn("serialized values can reach the browser", data_safety["answer"])

    def test_scenarios_cover_required_dimensions(self) -> None:
        required_fields = {"id", "tags", "given", "require", "forbid"}
        ids = [scenario["id"] for scenario in SCENARIOS]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(all(set(scenario) == required_fields for scenario in SCENARIOS))
        covered = {tag for scenario in SCENARIOS for tag in scenario["tags"]}
        self.assertTrue(
            {
                "positive-trigger",
                "negative-trigger",
                "main-task",
                "safety",
                "retention-trigger",
            }
            <= covered
        )


if __name__ == "__main__":
    unittest.main()
