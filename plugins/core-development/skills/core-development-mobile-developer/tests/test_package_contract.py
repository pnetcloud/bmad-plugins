import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
SCENARIOS = ROOT / "tests" / "scenarios.json"
TEXT_FILES = sorted(ROOT.rglob("*.md"))
PACKAGE_TEXT = "\n".join(path.read_text(encoding="utf-8") for path in TEXT_FILES)
NORMALIZED_PACKAGE_TEXT = " ".join(PACKAGE_TEXT.split()).lower()


class MobileSkillContractTests(unittest.TestCase):
    def test_original_entrypoint_is_retained(self):
        self.assertTrue(SKILL.is_file())

    def test_frontmatter_name_and_trigger_contract(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertRegex(
            text,
            r"(?m)^name: core-development-mobile-developer$",
        )
        description = re.search(
            r"(?ms)^---\n.*?^description: (.+?)\n---$",
            text,
        )
        self.assertIsNotNone(description)
        trigger = description.group(1)
        for phrase in (
            "React Native",
            "Flutter",
            "offline data",
            "performance",
            "signing",
            "mobile security",
            "mobile-responsive web-only",
            "backend-only",
        ):
            self.assertIn(phrase, trigger)

    def test_all_conditional_references_are_directly_routed(self):
        text = SKILL.read_text(encoding="utf-8")
        expected = {
            "references/architecture-and-data.md",
            "references/platform-experience-and-integrations.md",
            "references/performance-and-testing.md",
            "references/security-build-and-release.md",
        }
        linked = set(re.findall(r"\]\((references/[^)]+\.md)\)", text))
        self.assertEqual(expected, linked)
        for relative in expected:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_original_capability_families_remain_reachable(self):
        families = {
            "frameworks": ("React Native", "Flutter", "Kotlin Multiplatform"),
            "architecture": (
                "Clean Architecture",
                "repository",
                "dependency injection",
                "MVVM",
                "MVI",
                "code generation",
            ),
            "offline": (
                "SQLite",
                "Realm",
                "WatermelonDB",
                "conflict",
                "delta",
                "backoff",
                "TTL",
                "LRU",
                "pagination",
            ),
            "native_capabilities": (
                "camera",
                "location",
                "biometric",
                "Bluetooth Low Energy",
                "health",
                "background",
            ),
            "experience": (
                "navigation",
                "gesture",
                "haptics",
                "Dynamic Type",
                "dark",
                "VoiceOver",
                "TalkBack",
                "foldable",
            ),
            "platform_surfaces": (
                "widgets",
                "Live Activities",
                "shortcuts",
                "Wear OS",
                "CarPlay",
                "Android Auto",
            ),
            "performance": (
                "startup",
                "memory",
                "battery",
                "frame",
                "app size",
                "Hermes",
                "Impeller",
                "FFI",
            ),
            "testing": (
                "unit",
                "widget",
                "native integration",
                "end-to-end",
                "performance",
                "leak",
                "ANR",
            ),
            "build_release": (
                "build variants",
                "code shrinking",
                "app thinning",
                "dynamic feature",
                "Fastlane",
                "Codemagic",
                "Bitrise",
                "TestFlight",
                "Firebase App Distribution",
                "staged",
                "rollback",
            ),
            "store": (
                "screenshots",
                "keywords",
                "localization",
                "privacy",
                "age",
                "export",
                "release notes",
            ),
            "security": (
                "certificate",
                "Keychain",
                "Keystore",
                "root",
                "obfuscation",
                "deep links",
                "MASVS",
            ),
            "telemetry": (
                "Sentry",
                "Crashlytics",
                "Amplitude",
                "Mixpanel",
                "A/B",
                "feature flags",
            ),
            "coordination": (
                "Backend/API",
                "Product/design",
                "QA",
                "Security/privacy/legal",
                "Release/operations",
                "Performance",
                "Analytics/experimentation",
            ),
        }
        for family, phrases in families.items():
            with self.subTest(family=family):
                for phrase in phrases:
                    self.assertIn(phrase.lower(), PACKAGE_TEXT.lower())

    def test_fixed_metrics_are_replaced_by_measurement_contract(self):
        for unsupported in (
            "code sharing exceeding 80%",
            "app size under 40mb",
            "cold start time under 1.5 seconds",
            "memory usage below 120mb",
            "battery consumption under 4% per hour",
            "crash rate below 0.1%",
        ):
            self.assertNotIn(unsupported, PACKAGE_TEXT.lower())
        for required in (
            "device",
            "build",
            "conditions",
            "sample size",
            "baseline",
            "budget",
            "before/after",
        ):
            self.assertIn(required, PACKAGE_TEXT.lower())

    def test_fictional_protocol_and_fabricated_summary_are_removed(self):
        self.assertNotIn("query context manager", PACKAGE_TEXT.lower())
        self.assertNotIn('"request_type": "get_mobile_context"', PACKAGE_TEXT)
        self.assertNotIn("mobile app delivered successfully", PACKAGE_TEXT.lower())
        self.assertIn("do not invent", SKILL.read_text(encoding="utf-8").lower())

    def test_security_boundaries_are_explicit(self):
        for phrase in (
            "shipped client cannot keep an embedded service secret",
            "explicit authority",
            "pinning only when",
            "risk signals",
            "sole authorization boundary",
            "untrusted input",
            "authorized credential system",
        ):
            self.assertIn(phrase, NORMALIZED_PACKAGE_TEXT)

    def test_release_states_are_distinct(self):
        text = PACKAGE_TEXT.lower()
        for state in (
            "tests passed locally",
            "signed artifact verified",
            "beta distribution completed",
            "store review approved",
            "staged production rollout healthy",
            "full rollout healthy",
        ):
            self.assertIn(state, text)

    def test_interim_progress_contract_is_preserved(self):
        entrypoint = " ".join(SKILL.read_text(encoding="utf-8").split()).lower()
        for field in (
            "status:",
            "shared:",
            "ios:",
            "android:",
            "tests/evidence:",
            "blockers:",
            "next:",
        ):
            self.assertIn(field, entrypoint)
        self.assertIn(
            "do not report a platform, feature, test, or measurement as complete",
            entrypoint,
        )

    def test_scenarios_are_discriminating_and_cover_retention(self):
        scenarios = json.loads(SCENARIOS.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(scenarios), 16)
        names = {scenario["name"] for scenario in scenarios}
        required = {
            "positive-mobile-trigger",
            "negative-responsive-web-trigger",
            "negative-backend-only-trigger",
            "offline-conflict",
            "performance-claim-requires-measurement",
            "signing-without-secret-exposure",
            "interim-progress-update",
            "truthful-delivery-receipt",
            "preservation-first-structural-split",
        }
        self.assertTrue(required.issubset(names))
        self.assertEqual(len(names), len(scenarios))
        for scenario in scenarios:
            self.assertTrue(scenario["prompt"].strip())
            self.assertGreaterEqual(len(scenario["expect"]), 1)

    def test_entrypoint_stays_within_context_goal(self):
        text = SKILL.read_text(encoding="utf-8")
        lines = text.count("\n") + 1
        words = len(text.split())
        self.assertLessEqual(lines, 180)
        self.assertLessEqual(words, 1500)


if __name__ == "__main__":
    unittest.main()
