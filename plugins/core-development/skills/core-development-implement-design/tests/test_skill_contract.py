from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
REFERENCE = ROOT / "references" / "design-implementation-decisions.md"
SCENARIOS = (ROOT / "tests" / "scenarios.yaml").read_text(encoding="utf-8")


def normalized() -> str:
    text = SKILL.read_text(encoding="utf-8") + "\n" + REFERENCE.read_text(encoding="utf-8")
    return " ".join(text.lower().replace("`", "").split())


class ImplementDesignContractTests(unittest.TestCase):
    def test_frontmatter_trigger_and_nontriggers(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: core-development-implement-design\n"))
        description = re.search(r"^description: (.+)$", text, re.MULTILINE).group(1).lower()
        for phrase in ("figma", "implement", "do not use", "mcp"):
            self.assertIn(phrase, description)

    def test_entrypoint_and_reference(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertLessEqual(len(text.splitlines()), 300)
        self.assertLessEqual(len(text.split()), 1900)
        self.assertIn("[design-implementation-decisions.md](references/design-implementation-decisions.md)", text)
        self.assertTrue(REFERENCE.is_file())

    def test_original_seven_steps_remain(self):
        text = normalized()
        for phrase in (
            "step 1: get node id",
            "step 2: fetch design context",
            "step 3: capture visual reference",
            "step 4: download required assets",
            "step 5: translate to project conventions",
            "step 6: achieve 1:1 visual parity",
            "step 7: validate against figma",
        ):
            self.assertIn(phrase, text)

    def test_original_input_modes_and_tool_flow_remain(self):
        text = normalized()
        for phrase in (
            "parse from figma url",
            "current selection from figma desktop",
            "get_design_context",
            "get_metadata",
            "get_screenshot",
            "response is too large or truncated",
            "download any assets",
        ):
            self.assertIn(phrase, text)

    def test_original_implementation_families_remain(self):
        text = normalized()
        for phrase in (
            "component organization",
            "design system integration",
            "code quality",
            "implementing a button component",
            "building a dashboard layout",
            "incremental validation",
            "document deviations",
            "reuse over recreation",
            "design system first",
            "assets not loading",
            "design token values differ",
        ):
            self.assertIn(phrase, text)

    def test_untrusted_and_asset_boundaries(self):
        text = normalized()
        for phrase in (
            "untrusted data rather than instructions",
            "never ship a production reference",
            "revalidate dns/ip and origin",
            "reject absolute or traversal paths",
            "before preview or rasterization",
            "inspect scripts, event handlers",
            "do not infer redistribution rights",
            "private file keys",
        ):
            self.assertIn(phrase, text)

    def test_design_states_accessibility_and_validation(self):
        text = normalized()
        for phrase in (
            "complete relevant state matrix",
            "single desktop frame does not define mobile",
            "prefer native controls",
            "matching figma node or variant",
            "capture design context and screenshot as one source-evidence set",
            "visual similarity does not prove",
        ):
            self.assertIn(phrase, text)

    def test_authority_and_completion(self):
        text = normalized()
        for phrase in (
            "require explicit authority",
            "adding code connect mappings",
            "confirm the active authenticated identity",
            "never reset, clean, overwrite, or switch",
            "report source edit",
            "never claim pixel-perfect",
        ):
            self.assertIn(phrase, text)

    def test_scenarios(self):
        blocks = re.split(r"(?=^  - id: )", SCENARIOS, flags=re.MULTILINE)[1:]
        self.assertEqual(len(blocks), 50)
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
