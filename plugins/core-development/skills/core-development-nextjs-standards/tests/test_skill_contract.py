from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    return " ".join(SKILL.read_text(encoding="utf-8").lower().replace("`", "").split())


class NextJSStandardsContractTests(unittest.TestCase):
    def test_frontmatter_trigger(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-nextjs-standards\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("next.js-specific", "do not use", "another react framework"):
            self.assertIn(phrase, description)

    def test_entrypoint_is_concise(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 130)
        self.assertLessEqual(len(text.split()), 1500)

    def test_original_contract_is_literal(self):
        text = SKILL.read_text(encoding="utf-8")
        for phrase in (
            "Use App Router (`app/`) for new work; avoid legacy `pages/`.",
            "Prefer Server Components by default; use Client Components only when needed.",
            "Use dynamic imports for heavy components (code splitting).",
            "Organize routes in nested folders with `layout.tsx` for shared layouts.",
            "Use API Routes only for lightweight tasks; keep business logic in backend services.",
        ):
            self.assertIn(phrase, text)

    def test_router_scoped_baseline_rules(self):
        text = normalized()
        for phrase in (
            "when the target repository uses an apps/ convention",
            "otherwise preserve the repository's established root",
            "route-appropriate metadata with next.js apis",
            "open graph images where indexing and sharing policy require",
            "configured locale routing in pages router",
            "locale-segment routing and negotiation in app router",
            "use getserversideprops only in pages router",
            "generatestaticparams only for known dynamic route parameters",
        ):
            self.assertIn(phrase, text)

    def test_graph_authority_and_evidence(self):
        text = normalized()
        for phrase in (
            "complete application graph",
            "require explicit authority",
            "confirm exact revision, artifact, target",
            "client-reachable graphs",
            "rendered route",
            "indexed metadata",
        ):
            self.assertIn(phrase, text)

    def test_router_and_component_boundaries(self):
        text = normalized()
        for phrase in (
            "do not mix routers mechanically",
            "route-ownership and collision map",
            "verified pages-route retirement",
            "smallest boundary",
            "server component may render",
            "loading/error/not-found",
            "persistence, reset, fallback",
        ):
            self.assertIn(phrase, text)

    def test_metadata_i18n_and_dynamic_imports(self):
        text = normalized()
        for phrase in (
            "metadata presence alone",
            "effective http status and metadata",
            "ssr: false belongs in a client component",
            "for pages router, verify locales",
            "app router commonly uses",
            "routing does not translate content",
        ):
            self.assertIn(phrase, text)

    def test_data_and_mutation_boundaries(self):
        text = normalized()
        for phrase in (
            "getserversideprops guidance as pages router compatibility only",
            "generatestaticparams supplies known dynamic route parameters",
            "unknown-path behavior",
            "delegated contract's timeout and cancellation",
            "do not cache user-specific",
            "route handlers or pages router api routes",
            "server actions as remotely invokable mutation boundaries",
        ):
            self.assertIn(phrase, text)

    def test_validation_safety(self):
        text = normalized()
        for phrase in (
            "already-clean isolated checkout",
            "never clean, reset, overwrite, or switch",
            "cache hit/miss",
            "server and client artifacts",
            "rollback or repair",
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
