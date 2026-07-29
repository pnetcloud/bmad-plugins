from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCE = ROOT / "references" / "electron-decisions.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    package = SKILL.read_text(encoding="utf-8") + "\n" + REFERENCE.read_text(encoding="utf-8")
    return " ".join(package.lower().replace("`", "").split())


class ElectronProContractTests(unittest.TestCase):
    def test_frontmatter(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-electron-pro\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("electron desktop", "do not use", "browser-only", "another desktop framework"):
            self.assertIn(phrase, description)

    def test_entrypoint_budget_and_reference(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 250)
        self.assertLessEqual(len(text.split()), 1500)
        self.assertIn("[electron-decisions.md](references/electron-decisions.md)", text)
        self.assertTrue(REFERENCE.is_file())

    def test_original_capability_families(self):
        text = normalized()
        for phrase in (
            "desktop development checklist:",
            "security implementation:",
            "process architecture:",
            "native os integration:",
            "window management:",
            "auto-update system:",
            "performance optimization:",
            "build configuration:",
            "platform-specific handling:",
            "file system operations:",
            "debugging and diagnostics:",
            "native module management:",
        ):
            self.assertIn(phrase, text)

    def test_original_specific_capabilities(self):
        text = normalized()
        for phrase in (
            "context isolation enabled everywhere",
            "node integration disabled in renderers",
            "strict content security policy",
            "ipc channel validation",
            "permission request handling",
            "differential updates",
            "rollback mechanism",
            "system tray functionality",
            "display management",
            "file associations",
            "crash reporting",
            "module compilation",
        ):
            self.assertIn(phrase, text)

    def test_no_fixed_versions_metrics_or_fictional_evidence(self):
        text = normalized()
        for phrase in (
            "resolve the repository's exact electron",
            "installer size within the measured project budget",
            "startup time within the measured journey budget",
            "never fabricate security, size, startup",
            "do not imply access to a context manager",
            "report only artifacts and behavior actually produced",
        ):
            self.assertIn(phrase, text)
        raw = SKILL.read_text(encoding="utf-8")
        self.assertNotIn("Electron 27+", raw)
        self.assertNotIn("Achieved 2.5s startup", raw)

    def test_renderer_ipc_permissions(self):
        text = normalized()
        for phrase in (
            "never enable node.js integration for remote",
            "never expose raw ipcrenderer",
            "sender frame/origin/webcontents eligibility",
            "capture and validate event.senderframe synchronously",
            "event.reply or an equivalent origin-frame mechanism",
            "permission request and permission check",
            "disable unused command-execution surfaces",
            "embedded asar integrity validation",
        ):
            self.assertIn(phrase, text)

    def test_navigation_files_and_lifecycle(self):
        text = normalized()
        for phrase in (
            "deny unexpected navigation",
            "avoid loading application pages through broad file:// privileges",
            "narrow custom standard and secure protocol",
            "never forward untrusted arguments to a shell",
            "validate deep links and command-line arguments",
            "resist traversal and symlink races",
            "recover windows that are off-screen",
            "keep blocking or cpu-heavy work out of the main process",
        ):
            self.assertIn(phrase, text)

    def test_packaging_updates_and_performance(self):
        text = normalized()
        for phrase in (
            "isolated no-secret environment",
            "each materially distinct os, architecture, package format",
            "availability, download, verification, installation",
            "never generalize one platform's guarantee",
            "measure cold/warm startup",
            "profile before optimizing",
        ):
            self.assertIn(phrase, text)

    def test_authority_diagnostics_and_validation(self):
        text = normalized()
        for phrase in (
            "require explicit authority",
            "active identity, exact artifact",
            "never clean, reset, overwrite, or switch",
            "redact and bound logs and crash data",
            "every materially different platform path",
            "measurement variability, and optimization acceptance",
        ):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 41)
        identifiers, expectations = [], set()
        for block in blocks:
            identifier = re.search(r"^  - id: (.+)$", block, re.MULTILINE).group(1)
            fields = dict(re.findall(r"^    (expect|prompt|evidence): (.+)$", block, re.MULTILINE))
            self.assertEqual(set(fields), {"expect", "prompt", "evidence"})
            self.assertGreaterEqual(len(fields["prompt"].split()), 8)
            self.assertGreaterEqual(len(fields["evidence"].split()), 8)
            identifiers.append(identifier)
            expectations.add(fields["expect"])
        self.assertEqual(len(identifiers), len(set(identifiers)))
        self.assertEqual(expectations, {"trigger", "no_trigger", "safe_behavior", "bounded_behavior", "workflow"})


if __name__ == "__main__":
    unittest.main()
