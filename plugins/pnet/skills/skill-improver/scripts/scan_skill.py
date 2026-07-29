#!/usr/bin/env python3
"""Read-only structural and suspicious-content scan for an Agent Skill."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
INLINE_LINK_RE = re.compile(
    r"!?\[[^\]]*]\(\s*(?:<(?P<angle>[^>]+)>|(?P<plain>[^\s)]+))"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)"
)
REFERENCE_DEF_RE = re.compile(
    r"^\s*\[(?P<id>[^\]]+)]\s*:\s*(?:<(?P<angle>[^>]+)>|(?P<plain>\S+))",
    re.MULTILINE,
)
REFERENCE_USE_RE = re.compile(r"(?<!!)\[(?P<label>[^\]]+)]\[(?P<id>[^\]]*)]")
HIDDEN_UNICODE_RE = re.compile("[\u200b-\u200f\u202a-\u202e\u2066-\u2069\ufeff]")
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
MAX_TEXT_BYTES = 2_000_000

HEURISTICS = (
    (
        "prompt-override",
        re.compile(
            r"ignore\s+(?:all\s+|any\s+|the\s+)?(?:previous|prior|system)"
            r"\s+instructions|reveal\s+(?:the\s+)?system\s+prompt|jailbreak",
            re.IGNORECASE,
        ),
        "possible prompt-override instruction",
    ),
    (
        "pipe-to-shell",
        re.compile(
            r"(?:curl|wget)(?:(?!\|).){0,1000}\|[\s\\]*(?:sh|bash)\b",
            re.IGNORECASE | re.DOTALL,
        ),
        "remote content piped to a shell",
    ),
    (
        "destructive-command",
        re.compile(
            r"\brm\b"
            r"(?=[^\n;&|]{0,240}(?:-[a-z]*r[a-z]*|--recursive\b))"
            r"(?=[^\n;&|]{0,240}(?:-[a-z]*f[a-z]*|--force\b))"
            r"[^\n;&|]{1,240}|"
            r"\bgit\s+reset\s+--hard\b|"
            r"\b(?:mkfs|shutdown|reboot)\b",
            re.IGNORECASE,
        ),
        "potentially destructive command",
    ),
    (
        "sensitive-path",
        re.compile(
            r"(?:^|[/\\])\.ssh(?:[/\\]|$)|\bid_rsa\b|(?:^|[/\\])\.env\b|"
            r"\bkeychain\b|\bcredentials?\b",
            re.IGNORECASE,
        ),
        "reference to a sensitive path or credential store",
    ),
    (
        "secret-handling",
        re.compile(
            r"\b(?:api[_ -]?key|access[_ -]?token|password|secret)\b",
            re.IGNORECASE,
        ),
        "secret-related content requires review",
    ),
)


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    path: str
    line: int | None
    message: str


def add(
    findings: list[Finding],
    severity: str,
    code: str,
    path: Path | str,
    message: str,
    line: int | None = None,
) -> None:
    findings.append(Finding(severity, code, str(path), line, message))


def parse_frontmatter(skill_md: Path, text: str, findings: list[Finding]) -> None:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    relative = Path("SKILL.md")
    if not text.startswith("---\n"):
        add(
            findings,
            "blocking",
            "frontmatter-missing",
            relative,
            "SKILL.md must begin with YAML frontmatter at byte zero",
            1,
        )
        return

    closing = text.find("\n---\n", 4)
    if closing < 0:
        add(
            findings,
            "blocking",
            "frontmatter-unclosed",
            relative,
            "frontmatter has no closing delimiter",
            1,
        )
        return

    values: dict[str, str] = {}
    for index, line in enumerate(text[4:closing].splitlines(), start=2):
        match = re.match(r"^(name|description):\s*(.+?)\s*$", line)
        if match:
            values[match.group(1)] = match.group(2).strip("'\"")

    name = values.get("name", "")
    description = values.get("description", "")
    if not name:
        add(findings, "blocking", "name-missing", relative, "missing name", 2)
    elif not NAME_RE.fullmatch(name):
        add(
            findings,
            "blocking",
            "name-invalid",
            relative,
            "name must use lowercase kebab-case",
            2,
        )
    elif name != skill_md.parent.name:
        add(
            findings,
            "blocking",
            "name-directory-mismatch",
            relative,
            f"name {name!r} does not match directory {skill_md.parent.name!r}",
            2,
        )

    if not description:
        add(
            findings,
            "blocking",
            "description-missing",
            relative,
            "missing description",
            3,
        )
    elif len(description) > 1024:
        add(
            findings,
            "blocking",
            "description-too-long",
            relative,
            "description exceeds 1024 characters",
            3,
        )

    if not text[closing + 5 :].strip():
        add(findings, "blocking", "body-empty", relative, "skill body is empty")

    line_count = text.count("\n") + 1
    if line_count > 500:
        add(
            findings,
            "warning",
            "skill-too-long",
            relative,
            f"SKILL.md has {line_count} lines; consider progressive disclosure",
        )


def local_link_target(raw_target: str) -> str | None:
    target = raw_target.strip().strip("<>")
    if not target or target.startswith(("#", "http://", "https://", "mailto:")):
        return None
    target = target.split("#", 1)[0].split("?", 1)[0]
    return unquote(target) or None


def check_local_target(
    root: Path,
    markdown_path: Path,
    raw_target: str,
    line: int,
    findings: list[Finding],
) -> None:
    target = local_link_target(raw_target)
    if target is None:
        return
    relative_markdown = markdown_path.relative_to(root)
    resolved = (markdown_path.parent / target).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        add(
            findings,
            "blocking",
            "reference-escapes-skill",
            relative_markdown,
            f"local reference escapes the skill directory: {target}",
            line,
        )
        return
    if not resolved.exists():
        add(
            findings,
            "blocking",
            "reference-missing",
            relative_markdown,
            f"referenced file does not exist: {target}",
            line,
        )


def scan_links(
    root: Path,
    markdown_path: Path,
    text: str,
    findings: list[Finding],
) -> None:
    for match in INLINE_LINK_RE.finditer(text):
        target = match.group("angle") or match.group("plain")
        line = text.count("\n", 0, match.start()) + 1
        check_local_target(root, markdown_path, target, line, findings)

    definitions: dict[str, str] = {}
    for match in REFERENCE_DEF_RE.finditer(text):
        identifier = match.group("id").strip().casefold()
        target = match.group("angle") or match.group("plain")
        definitions[identifier] = target
        line = text.count("\n", 0, match.start()) + 1
        check_local_target(root, markdown_path, target, line, findings)

    for match in REFERENCE_USE_RE.finditer(text):
        identifier = (match.group("id") or match.group("label")).strip().casefold()
        if identifier in definitions:
            continue
        line = text.count("\n", 0, match.start()) + 1
        add(
            findings,
            "blocking",
            "reference-definition-missing",
            markdown_path.relative_to(root),
            f"reference-style link has no definition: {identifier}",
            line,
        )


def iter_paths(root: Path):
    for current, dirs, files in os.walk(root, followlinks=False):
        current_path = Path(current)
        skipped = [name for name in dirs if name in SKIP_DIRS]
        dirs[:] = [name for name in dirs if name not in SKIP_DIRS]
        for name in skipped:
            yield current_path / name, True
        for name in dirs + files:
            yield current_path / name, False


def read_text(path: Path) -> tuple[str | None, str | None]:
    try:
        size = path.stat().st_size
    except OSError as error:
        return None, f"cannot stat file: {error}"
    if size > MAX_TEXT_BYTES:
        return None, f"file exceeds {MAX_TEXT_BYTES} byte scan limit"
    try:
        data = path.read_bytes()
    except OSError as error:
        return None, f"cannot read file: {error}"
    if b"\0" in data:
        return None, "file contains NUL bytes"
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        return None, "file is not valid UTF-8 text"


def scan_text(
    root: Path,
    path: Path,
    text: str,
    findings: list[Finding],
) -> None:
    relative = path.relative_to(root)
    for match in HIDDEN_UNICODE_RE.finditer(text):
        add(
            findings,
            "blocking",
            "hidden-unicode",
            relative,
            "hidden or bidirectional Unicode control character",
            text.count("\n", 0, match.start()) + 1,
        )

    for code, pattern, message in HEURISTICS:
        for match in pattern.finditer(text):
            add(
                findings,
                "warning",
                code,
                relative,
                message,
                text.count("\n", 0, match.start()) + 1,
            )

    if path.suffix.casefold() == ".md":
        scan_links(root, path, text, findings)


def scan_tree(root: Path, findings: list[Finding]) -> None:
    for path, skipped in iter_paths(root):
        relative = path.relative_to(root)
        if skipped:
            add(
                findings,
                "warning",
                "skipped-directory",
                relative,
                "directory was not traversed; inspect or remove it before trusting the skill",
            )
            continue
        if path.is_symlink():
            add(
                findings,
                "blocking",
                "symlink",
                relative,
                f"symlink target requires manual review: {os.readlink(path)}",
            )
            continue
        if not path.is_file():
            continue

        try:
            mode = path.stat().st_mode
        except OSError as error:
            add(findings, "blocking", "stat-failed", relative, str(error))
            continue

        if mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH):
            add(
                findings,
                "warning",
                "executable-file",
                relative,
                "executable file requires manual code review before use",
            )

        text, error = read_text(path)
        if text is None:
            add(
                findings,
                "blocking",
                "opaque-or-oversized-file",
                relative,
                error or "file cannot be inspected safely",
            )
            continue

        scan_text(root, path, text, findings)


def scan_skill(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    if root.is_symlink():
        add(
            findings,
            "blocking",
            "target-symlink",
            root,
            "target skill directory must not be a symlink",
        )
        return findings
    if not root.exists() or not root.is_dir():
        add(
            findings,
            "blocking",
            "target-invalid",
            root,
            "target must be an existing skill directory",
        )
        return findings

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        add(
            findings,
            "blocking",
            "skill-md-missing",
            Path("SKILL.md"),
            "SKILL.md is missing",
        )
        scan_tree(root, findings)
        return findings

    text, error = read_text(skill_md)
    if text is None:
        add(
            findings,
            "blocking",
            "skill-md-unreadable",
            Path("SKILL.md"),
            error or "SKILL.md must be readable UTF-8 text",
        )
    else:
        parse_frontmatter(skill_md, text, findings)

    scan_tree(root, findings)
    return sorted(
        findings,
        key=lambda item: (
            0 if item.severity == "blocking" else 1,
            item.path,
            item.line or 0,
            item.code,
        ),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_dir", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.skill_dir.expanduser().absolute()
    findings = scan_skill(root)
    blocking = sum(item.severity == "blocking" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "target": str(root),
                    "blocking": blocking,
                    "warnings": warnings,
                    "findings": [asdict(item) for item in findings],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(f"target: {root}")
        print(f"blocking: {blocking}; warnings: {warnings}")
        for item in findings:
            location = item.path
            if item.line is not None:
                location += f":{item.line}"
            print(f"[{item.severity}] {item.code} {location} - {item.message}")

    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
