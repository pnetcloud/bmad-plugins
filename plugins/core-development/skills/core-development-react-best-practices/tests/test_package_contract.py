from pathlib import Path
import json
import re
import unittest


SKILL_DIR = Path(__file__).resolve().parents[1]
RULES_DIR = SKILL_DIR / "rules"
EXPECTED_RULES = {
    "advanced-event-handler-refs.md",
    "advanced-use-latest.md",
    "async-api-routes.md",
    "async-defer-await.md",
    "async-dependencies.md",
    "async-parallel.md",
    "async-suspense-boundaries.md",
    "bundle-barrel-imports.md",
    "bundle-conditional.md",
    "bundle-defer-third-party.md",
    "bundle-dynamic-imports.md",
    "bundle-preload.md",
    "client-event-listeners.md",
    "client-localstorage-schema.md",
    "client-passive-event-listeners.md",
    "client-swr-dedup.md",
    "js-batch-dom-css.md",
    "js-cache-function-results.md",
    "js-cache-property-access.md",
    "js-cache-storage.md",
    "js-combine-iterations.md",
    "js-early-exit.md",
    "js-hoist-regexp.md",
    "js-index-maps.md",
    "js-length-check-first.md",
    "js-min-max-loop.md",
    "js-set-map-lookups.md",
    "js-tosorted-immutable.md",
    "rendering-activity.md",
    "rendering-animate-svg-wrapper.md",
    "rendering-conditional-render.md",
    "rendering-content-visibility.md",
    "rendering-hoist-jsx.md",
    "rendering-hydration-no-flicker.md",
    "rendering-svg-precision.md",
    "rerender-defer-reads.md",
    "rerender-dependencies.md",
    "rerender-derived-state.md",
    "rerender-functional-setstate.md",
    "rerender-lazy-state-init.md",
    "rerender-memo.md",
    "rerender-memo-with-default-value.md",
    "rerender-simple-expression-in-memo.md",
    "rerender-transitions.md",
    "server-after-nonblocking.md",
    "server-auth-actions.md",
    "server-cache-lru.md",
    "server-cache-react.md",
    "server-dedup-props.md",
    "server-parallel-fetching.md",
    "server-serialization.md",
}


class PackageContractTests(unittest.TestCase):
    def test_every_original_path_and_rule_family_remains(self):
        for root_file in ("AGENTS.md", "README.md", "SKILL.md", "metadata.json"):
            self.assertTrue((SKILL_DIR / root_file).is_file(), root_file)
        for special_file in ("_sections.md", "_template.md"):
            self.assertTrue((RULES_DIR / special_file).is_file(), special_file)

        actual_rules = {
            path.name
            for path in RULES_DIR.glob("*.md")
            if not path.name.startswith("_")
        }
        self.assertEqual(actual_rules, EXPECTED_RULES)

    def test_entrypoint_routes_all_51_rules_and_preserves_contract(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Review is read-only by default", skill)
        self.assertIn("unmeasured recommendation", skill)
        self.assertIn("[AGENTS.md](AGENTS.md)", skill)
        self.assertIn("[rules/_sections.md](rules/_sections.md)", skill)
        for rule_file in EXPECTED_RULES:
            self.assertIn(f"`{Path(rule_file).stem}`", skill, rule_file)

        lines = skill.splitlines()
        self.assertLessEqual(len(lines), 220)
        self.assertLessEqual(len(skill.split()), 1600)

    def test_rule_units_keep_structured_content(self):
        for rule_file in EXPECTED_RULES:
            content = (RULES_DIR / rule_file).read_text(encoding="utf-8")
            self.assertRegex(content, r"(?m)^title:\s+\S")
            self.assertRegex(content, r"(?m)^impact:\s+\S")
            self.assertRegex(content, r"(?m)^tags:\s+\S")
            self.assertRegex(content, r"(?m)^##\s+\S")
            self.assertIn("```", content)

    def test_compatibility_snapshot_and_metadata_are_truthful(self):
        compiled = (SKILL_DIR / "AGENTS.md").read_text(encoding="utf-8")
        readme = (SKILL_DIR / "README.md").read_text(encoding="utf-8")
        metadata = json.loads(
            (SKILL_DIR / "metadata.json").read_text(encoding="utf-8")
        )

        self.assertGreaterEqual(len(compiled.splitlines()), 2500)
        self.assertIn("Compatibility status", compiled)
        self.assertIn("51 React and Next.js performance rules", metadata["abstract"])
        self.assertEqual(metadata["date"], "January 2026")
        self.assertIn("source_snapshot", metadata)
        self.assertIn("public_reviewed", metadata)
        self.assertEqual(
            metadata["review_basis"],
            {
                "react": "19.2.7 documentation snapshot",
                "nextjs": "16.2.9 documentation snapshot",
            },
        )
        for unavailable_command in (
            "pnpm install",
            "pnpm build",
            "pnpm validate",
            "pnpm extract-tests",
        ):
            self.assertNotIn(unavailable_command, readme)
        self.assertIn("[@shuding](https://x.com/shuding)", readme)
        self.assertIn("[Vercel](https://vercel.com)", readme)

    def test_version_and_security_caveats_cover_fragile_patterns(self):
        surfaces = {
            "activity": RULES_DIR / "rendering-activity.md",
            "hydration": RULES_DIR / "rendering-hydration-no-flicker.md",
            "process-cache": RULES_DIR / "server-cache-lru.md",
            "request-cache": RULES_DIR / "server-cache-react.md",
            "post-response": RULES_DIR / "server-after-nonblocking.md",
            "storage-cache": RULES_DIR / "js-cache-storage.md",
            "function-cache": RULES_DIR / "js-cache-function-results.md",
        }
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in surfaces.values()
        )
        for required in (
            "official documentation",
            "authorization",
            "Content Security Policy",
            "cross-user",
            "durable",
            "invalidation",
        ):
            self.assertIn(required, combined)
        storage_cache = surfaces["storage-cache"].read_text(encoding="utf-8")
        self.assertIn("NON_SENSITIVE_COOKIE_KEYS", storage_cache)
        self.assertIn("getCachedPreferenceCookie", storage_cache)
        self.assertIn("invalidatePreferenceCookie", storage_cache)
        self.assertIn("preferenceCookieCache.clear()", storage_cache)
        self.assertRegex(
            storage_cache,
            r"try \{\s+value = match \? decodeURIComponent",
        )

        function_cache = surfaces["function-cache"].read_text(encoding="utf-8")
        self.assertIn("MAX_SLUG_CACHE_ENTRIES", function_cache)
        self.assertIn("slugifyCache.delete(oldestKey)", function_cache)

        process_cache = surfaces["process-cache"].read_text(encoding="utf-8")
        self.assertIn("warm instance", process_cache)
        self.assertIn("affinity are not guaranteed", process_cache)

        request_cache = surfaces["request-cache"].read_text(encoding="utf-8")
        self.assertIn("`GET` or", request_cache)
        self.assertRegex(request_cache, r"Route\s+Handlers")
        self.assertIn("AbortController", request_cache)

        post_response = surfaces["post-response"].read_text(encoding="utf-8")
        self.assertNotIn("sessionCookie", post_response)
        self.assertIn("Do not send cookies", post_response)

        hydration = surfaces["hydration"].read_text(encoding="utf-8")
        self.assertIn("server and first client render agree", hydration)
        self.assertIn("does not guarantee", hydration)
        self.assertNotIn("dangerouslySetInnerHTML", hydration)

    def test_public_storage_example_is_not_env_syntax(self):
        storage_rule = (
            RULES_DIR / "client-localstorage-schema.md"
        ).read_text(encoding="utf-8")
        compiled = (SKILL_DIR / "AGENTS.md").read_text(encoding="utf-8")
        env_like_storage_key = "$" + "{VERSION}"
        self.assertNotIn(env_like_storage_key, storage_rule)
        self.assertNotIn(env_like_storage_key, compiled)
        self.assertIn("const STORAGE_KEY = 'userConfig:v2'", storage_rule)

    def test_frontmatter_nests_source_metadata(self):
        skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = skill.split("---", 2)[1]
        self.assertRegex(frontmatter, r"(?m)^metadata:\s*$")
        self.assertRegex(frontmatter, r"(?m)^  author:\s+vercel$")
        self.assertRegex(frontmatter, r'(?m)^  version:\s+"1\.0\.0"$')
        self.assertIsNone(re.search(r"(?m)^author:", frontmatter))
        self.assertIsNone(re.search(r"(?m)^version:", frontmatter))


if __name__ == "__main__":
    unittest.main()
