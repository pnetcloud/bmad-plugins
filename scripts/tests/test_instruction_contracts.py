"""Regression tests for the repository's Markdown format parser, not skill prose."""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "check_instruction_contracts.py"
SPEC = importlib.util.spec_from_file_location("instruction_contracts", SCRIPT)
assert SPEC and SPEC.loader
contracts = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(contracts)


def entry() -> str:
    return "---\nname: example-skill\ndescription: An example.\n---\n\n# Example\n\n" + "\n\n".join(
        f"## {heading}\n\nGuidance for {heading}." for heading in contracts.REQUIRED_SECTIONS
    ) + "\n"


class InstructionContractTests(unittest.TestCase):
    def test_valid_contract(self):
        self.assertEqual(contracts.inspect_contract(entry()), [])

    def test_crlf(self):
        self.assertEqual(contracts.inspect_contract(entry().replace("\n", "\r\n")), [])

    def test_fenced_template_headings_are_not_instructions(self):
        text = entry().replace("Guidance for Focus.", "```markdown\n# Template\n## Not a contract section\n```\nDomain guidance.")
        self.assertEqual(contracts.inspect_contract(text), [])

    def test_long_outer_fence_is_not_closed_by_shorter_inner_fence(self):
        text = entry().replace("Guidance for Focus.", "````markdown\n```\n## Template heading\n```\n````\nDomain guidance.")
        self.assertEqual(contracts.inspect_contract(text), [])

    def test_tilde_fence(self):
        text = entry().replace("Guidance for Focus.", "~~~markdown\n## Template\n~~~\nDomain guidance.")
        self.assertEqual(contracts.inspect_contract(text), [])

    def test_unclosed_fence_rejected(self):
        self.assertTrue(any("unclosed fenced" in e for e in contracts.inspect_contract(entry() + "```sh\ncommand\n")))

    def test_missing_frontmatter(self):
        self.assertTrue(contracts.inspect_contract(entry().split("---", 2)[-1]))

    def test_unclosed_frontmatter(self):
        self.assertTrue(contracts.inspect_contract("---\nname: demo\n"))

    def test_missing_section(self):
        self.assertTrue(contracts.inspect_contract(entry().replace("## Focus\n\nGuidance for Focus.\n\n", "")))

    def test_wrong_order(self):
        text = entry().replace("## Focus", "## Return", 1)
        self.assertTrue(contracts.inspect_contract(text))

    def test_extra_section(self):
        self.assertTrue(contracts.inspect_contract(entry() + "\n## Extra\n\nOther guidance.\n"))

    def test_empty_section(self):
        self.assertTrue(any("empty section: Return" == e for e in contracts.inspect_contract(entry().replace("Guidance for Return.", ""))))

    def test_attached_hashes_are_literal_not_closing_delimiters(self):
        for heading in ("## Focus#", "## Focus###", "## Focus# ###", "## Focus\\#"):
            with self.subTest(heading=heading):
                self.assertTrue(contracts.inspect_contract(entry().replace("## Focus", heading)))

    def test_whitespace_separated_closing_hashes_are_valid(self):
        for heading in ("## Focus ###", "## Focus\t###\t", "## Focus ##   "):
            with self.subTest(heading=heading):
                self.assertEqual(contracts.inspect_contract(entry().replace("## Focus", heading)), [])

    def test_thematic_break_alone_is_not_section_content(self):
        for marker in ("* * *", "- - -", "_ _ _", "***", "---", "___", "  *\t*  *  ", "   - - - -"):
            with self.subTest(marker=marker):
                text = entry().replace("Guidance for Return.", marker)
                self.assertIn("empty section: Return", contracts.inspect_contract(text))

    def test_non_thematic_literal_text_is_content(self):
        for literal in ("--", "* _ *", "___label", "    * * *"):
            with self.subTest(literal=literal):
                self.assertEqual(contracts.inspect_contract(entry().replace("Guidance for Return.", literal)), [])

    def test_thematic_looking_fenced_code_is_preserved_content(self):
        text = entry().replace("Guidance for Return.", "```text\n* * *\n```")
        self.assertEqual(contracts.inspect_contract(text), [])

    def test_empty_atx_title_rejected(self):
        self.assertTrue(contracts.inspect_contract(entry().replace("# Example", "# ###")))

    def test_cli_rejects_both_false_acceptance_cases(self):
        import json
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            for text in (entry().replace("## Focus", "## Focus#"), entry().replace("Guidance for Return.", "* * *")):
                with self.subTest(text=text):
                    path.write_text(text)
                    result = subprocess.run([sys.executable, str(SCRIPT), str(path), "--json"], capture_output=True, text=True)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertEqual(json.loads(result.stdout)["failed"], 1)

    def test_subheading_alone_is_not_section_content(self):
        self.assertTrue(any("empty section: Return" == e for e in contracts.inspect_contract(entry().replace("Guidance for Return.", "### A subheading"))))

    def test_html_comment_headings_are_not_instructions(self):
        text = entry().replace("Guidance for Focus.", "<!--\n# Ignored title\n## Ignored section\n-->\nDomain guidance.")
        self.assertEqual(contracts.inspect_contract(text), [])

    def test_inline_html_comment(self):
        text = entry().replace("## Focus", "<!-- ignored -->## Focus")
        self.assertEqual(contracts.inspect_contract(text), [])

    def test_unclosed_html_comment(self):
        self.assertTrue(any("unclosed HTML comment" == e for e in contracts.inspect_contract(entry() + "<!-- hidden")))

    def test_blockquote_headings_are_not_instructions(self):
        text = entry().replace("Guidance for Focus.", "> # Example\n> ## Example\nDomain guidance.")
        self.assertEqual(contracts.inspect_contract(text), [])

    def test_missing_title(self):
        self.assertTrue(contracts.inspect_contract(entry().replace("# Example\n", "")))

    def test_duplicate_title(self):
        self.assertTrue(contracts.inspect_contract(entry() + "\n# Another title\n"))

    def test_missing_file_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            rows = contracts.validate_paths([Path(directory) / "missing.md"])
            self.assertTrue(rows[0]["errors"])

    def test_symlink_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "SKILL.md"
            target.write_text(entry())
            linked = root / "linked.md"
            linked.symlink_to(target)
            self.assertTrue(contracts.validate_paths([linked])[0]["errors"])

    def test_cli_explicit_path_and_nonzero_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text(entry())
            good = subprocess.run([sys.executable, str(SCRIPT), str(path), "--json"], capture_output=True, text=True)
            self.assertEqual(good.returncode, 0, good.stderr)
            path.write_text("invalid")
            bad = subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertNotEqual(bad.returncode, 0)


if __name__ == "__main__":
    unittest.main()
