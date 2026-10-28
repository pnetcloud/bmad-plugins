#!/usr/bin/env python3
"""Lint the collection's explicit entry schema, not semantic skill quality.

Only Markdown structure is checked. Domain accuracy, authority, preservation
and runtime behavior require separate review and evidence.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED_SECTIONS = (
    "Purpose and selection",
    "Working mode",
    "Focus",
    "Quality checks",
    "Return",
    "Boundaries",
)
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING = re.compile(r"^ {0,3}(#{1,6})[ \t]+(.*?)[ \t]*$")
CLOSING_HASHES = re.compile(r"(?:^|[ \t]+)#+[ \t]*$")
THEMATIC_BREAK = re.compile(r"^ {0,3}(?:\*(?:[ \t]*\*){2,}|-(?:[ \t]*-){2,}|_(?:[ \t]*_){2,})[ \t]*$")
SOURCE_ROOT = Path(__file__).resolve().parent.parent


def inspect_contract(text: str) -> list[str]:
    """Return format errors; ignore YAML, HTML comments and fenced examples."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return ["missing frontmatter opening delimiter"]
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return ["unclosed frontmatter"]
    errors: list[str] = []
    sections: list[tuple[str, list[str]]] = []
    titles: list[int] = []
    fence_char = ""
    fence_length = 0
    fence_line = 0
    in_comment = False
    for number, source in enumerate(lines[end + 1 :], start=end + 2):
        # HTML comments are not entry instructions. Remove inline comments too.
        line = source
        if not fence_char:
            visible = ""
            while line:
                if in_comment:
                    close = line.find("-->")
                    if close < 0:
                        line = ""
                        break
                    line = line[close + 3 :]
                    in_comment = False
                else:
                    opening = line.find("<!--")
                    if opening < 0:
                        visible += line
                        line = ""
                    else:
                        visible += line[:opening]
                        line = line[opening + 4 :]
                        in_comment = True
            line = visible
        match = FENCE.match(line)
        if fence_char:
            if match and match[1][0] == fence_char and len(match[1]) >= fence_length and not match[2].strip():
                fence_char = ""
            elif sections and line.strip():
                sections[-1][1].append(line)
            continue
        if match:
            # Backticks in a backtick info string do not open a CommonMark fence.
            if match[1][0] == "`" and "`" in match[2]:
                if sections:
                    sections[-1][1].append(line)
                continue
            fence_char, fence_length, fence_line = match[1][0], len(match[1]), number
            continue
        heading = HEADING.match(line)
        if heading:
            # ATX closing hashes require whitespace separation. In Focus# the
            # hash is literal title text, not an optional closing delimiter.
            level = len(heading[1])
            title = CLOSING_HASHES.sub("", heading[2]).strip()
            if level == 1:
                titles.append(number)
                if not title:
                    errors.append(f"line {number}: empty skill title")
                if sections:
                    errors.append(f"line {number}: skill title must precede contract sections")
            elif level == 2:
                sections.append((title, []))
            continue
        if sections and line.strip() and not THEMATIC_BREAK.fullmatch(line):
            sections[-1][1].append(line)
    if fence_char:
        errors.append(f"line {fence_line}: unclosed fenced block")
    if in_comment:
        errors.append("unclosed HTML comment")
    if len(titles) != 1:
        errors.append(f"expected one skill title, found {len(titles)}")
    actual = tuple(title for title, _ in sections)
    if actual != REQUIRED_SECTIONS:
        errors.append("expected section order: " + ", ".join(REQUIRED_SECTIONS) + "; found: " + ", ".join(actual))
    for title, body in sections:
        if not body:
            errors.append(f"empty section: {title}")
    return errors


def validate_paths(paths: list[Path]) -> list[dict]:
    results = []
    for path in paths:
        try:
            if path.is_symlink():
                raise ValueError("entry must not be a symlink")
            errors = inspect_contract(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError) as exc:
            errors = [f"cannot read entry: {exc}"]
        results.append({"path": str(path), "errors": errors})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", type=Path, nargs="*", help="explicit SKILL.md paths; default: this checkout's complete catalog")
    parser.add_argument("--json", action="store_true", help="emit every checked entry and its errors")
    args = parser.parse_args()
    paths = args.paths or sorted(SOURCE_ROOT.glob("plugins/*/skills/*/SKILL.md"))
    if not paths:
        parser.error("no skill entries discovered")
    results = validate_paths(paths)
    bad = [row for row in results if row["errors"]]
    if args.json:
        print(json.dumps({"checked": len(results), "failed": len(bad), "results": results}, indent=2))
    else:
        for row in bad:
            for error in row["errors"]:
                print(f"{row['path']}: {error}")
        print(f"Instruction entry format: {len(results)} checked, {len(bad)} failed. Semantic quality is not assessed.")
    return bool(bad)


if __name__ == "__main__":
    raise SystemExit(main())
