#!/usr/bin/env python3
"""Read-only structural, suspicious-content, and public-release scan for a skill."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import re
import stat
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote, urlsplit


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
DESCRIPTION_REVIEW_CHARS = 500
SKILL_REVIEW_LINES = 250
SKILL_MAX_LINES = 500
SKILL_REVIEW_WORDS = 2_000
PUBLIC_POLICY_VERSION = 1
PUBLIC_POLICY_KEYS = {
    "version",
    "forbidden_literals",
    "forbidden_regexes",
    "forbidden_domains",
    "allowed_environment_variables",
    "allowed_email_domains",
}
ENVIRONMENT_REFERENCE_RE = re.compile(
    r"\$\{(?P<braced>[A-Z][A-Z0-9_]{1,})[^}]*}|\$(?P<plain>[A-Z][A-Z0-9_]{1,})\b|"
    r"^\s*(?:export|ENV)\s+(?P<declared>[A-Z][A-Z0-9_]{1,})\s*=",
    re.MULTILINE,
)
BARE_ENVIRONMENT_ASSIGNMENT_RE = re.compile(
    r"(?m)^\s*(?:-\s+)?(?P<assigned>[A-Z][A-Z0-9_]{1,})\s*="
)
ENVIRONMENT_ASSIGNMENT_SUFFIXES = {
    ".bash",
    ".env",
    ".md",
    ".mk",
    ".sh",
    ".yaml",
    ".yml",
    ".zsh",
}
ABSOLUTE_PRIVATE_PATH_RE = re.compile(
    r"(?:/home|/Users)/[A-Za-z0-9._-]+(?:/|$)|"
    r"\b[A-Za-z]:\\Users\\[^\\\s]+(?:\\|$)"
)
PRIVATE_HOST_RE = re.compile(
    r"\b(?:[A-Za-z0-9-]+\.)+(?:internal|corp|lan|local)\b",
    re.IGNORECASE,
)
PRIVATE_CONTEXT_RE = re.compile(
    r"\bour\s+(?:internal\s+)?(?:production|staging|cluster|namespace|service|"
    r"database|repository|repo|architecture|topic|workflow|tenant)\b|"
    r"\b(?:internal|private)\s+(?:hostname|domain|cluster|namespace|service|"
    r"database|repository|repo|topic|workflow)(?:\s+(?:name|url|id))?\s*[:=]",
    re.IGNORECASE,
)
URL_RE = re.compile(
    r"\b[a-z][a-z0-9+.-]{1,20}://[^\s<>()\"']+",
    re.IGNORECASE,
)
EMAIL_RE = re.compile(
    r"(?<![A-Za-z0-9._%+-])"
    r"(?P<local>[A-Za-z0-9._%+-]{1,64})@"
    r"(?P<domain>[A-Za-z0-9.-]+\.[A-Za-z]{2,})"
)
IPV4_RE = re.compile(r"(?<![0-9])(?:[0-9]{1,3}\.){3}[0-9]{1,3}(?![0-9])")
SENSITIVE_PACKAGE_PATH_RE = re.compile(
    r"(?:^|/)(?:\.env(?:\.[^/]+)?|id_(?:rsa|dsa|ecdsa|ed25519)|"
    r"credentials?(?:\.[^/]+)?|[^/]+\.(?:key|p12|pfx|jks|keystore))$",
    re.IGNORECASE,
)
SECRET_VALUE_PATTERNS = (
    (
        "public-private-key",
        re.compile(
            r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----"
        ),
        "private key material detected",
    ),
    (
        "public-provider-token",
        re.compile(
            r"\b(?:AKIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9]{30,255}|"
            r"xox[baprs]-[A-Za-z0-9-]{20,255}|sk_live_[A-Za-z0-9]{16,255})\b"
        ),
        "provider credential pattern detected",
    ),
    (
        "public-jwt",
        re.compile(
            r"\beyJ[A-Za-z0-9_-]{8,}\.eyJ[A-Za-z0-9_-]{8,}\."
            r"[A-Za-z0-9_-]{8,}\b"
        ),
        "JWT-like credential detected",
    ),
)
GENERIC_SECRET_ASSIGNMENT_RE = re.compile(
    r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|"
    r"password|passwd|secret)\b\s*[:=]\s*[\"']?"
    r"(?P<value>[^\s,\"';}{]{8,})"
)
PLACEHOLDER_VALUE_RE = re.compile(
    r"(?i)^(?:<[^>]+>|\$\{?[^}]+\}?|your[-_].*|example.*|sample.*|dummy.*|"
    r"test.*|fake.*|redacted|masked|changeme|replace[-_].*|x{4,}|"
    r"\*{4,}|user(?:name)?|pass(?:word)?|"
    r"(?:input|button|select|textarea)\[.*)$"
)

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


@dataclass(frozen=True)
class PublicPolicy:
    forbidden_literals: tuple[str, ...]
    forbidden_regexes: tuple[re.Pattern[str], ...]
    forbidden_domains: frozenset[str]
    allowed_environment_variables: frozenset[str]
    allowed_email_domains: frozenset[str]


def add(
    findings: list[Finding],
    severity: str,
    code: str,
    path: Path | str,
    message: str,
    line: int | None = None,
) -> None:
    findings.append(Finding(severity, code, str(path), line, message))


def policy_string_list(
    data: dict[str, object],
    key: str,
    findings: list[Finding],
) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not all(
        isinstance(item, str) and item.strip() for item in value
    ):
        add(
            findings,
            "blocking",
            "public-policy-invalid",
            "PUBLIC_POLICY",
            f"{key} must be a list of non-empty strings",
        )
        return []
    return [item.strip() for item in value]


def load_public_policy(
    path: Path,
    findings: list[Finding],
) -> PublicPolicy | None:
    text, error = read_text(path)
    if text is None:
        add(
            findings,
            "blocking",
            "public-policy-unreadable",
            "PUBLIC_POLICY",
            error or "public policy must be readable UTF-8 JSON",
        )
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        add(
            findings,
            "blocking",
            "public-policy-invalid",
            "PUBLIC_POLICY",
            f"invalid JSON at line {error.lineno}",
        )
        return None
    if not isinstance(data, dict):
        add(
            findings,
            "blocking",
            "public-policy-invalid",
            "PUBLIC_POLICY",
            "policy root must be an object",
        )
        return None

    unknown = sorted(set(data) - PUBLIC_POLICY_KEYS)
    if unknown:
        add(
            findings,
            "blocking",
            "public-policy-invalid",
            "PUBLIC_POLICY",
            f"unknown policy fields: {', '.join(unknown)}",
        )
    if data.get("version") != PUBLIC_POLICY_VERSION:
        add(
            findings,
            "blocking",
            "public-policy-invalid",
            "PUBLIC_POLICY",
            f"version must be {PUBLIC_POLICY_VERSION}",
        )

    literal_values = policy_string_list(data, "forbidden_literals", findings)
    regex_values = policy_string_list(data, "forbidden_regexes", findings)
    domain_values = policy_string_list(data, "forbidden_domains", findings)
    environment_values = policy_string_list(
        data,
        "allowed_environment_variables",
        findings,
    )
    email_domain_values = policy_string_list(
        data,
        "allowed_email_domains",
        findings,
    )

    if not literal_values and not regex_values:
        add(
            findings,
            "blocking",
            "public-policy-empty",
            "PUBLIC_POLICY",
            "policy must contain private product or architecture terms",
        )

    compiled_regexes: list[re.Pattern[str]] = []
    for index, value in enumerate(regex_values, start=1):
        try:
            compiled_regexes.append(re.compile(value, re.IGNORECASE))
        except re.error:
            add(
                findings,
                "blocking",
                "public-policy-invalid",
                "PUBLIC_POLICY",
                f"forbidden_regexes entry {index} is invalid",
            )

    invalid_environment_values = [
        value
        for value in environment_values
        if not re.fullmatch(r"[A-Z][A-Z0-9_]{1,}", value)
    ]
    if invalid_environment_values:
        add(
            findings,
            "blocking",
            "public-policy-invalid",
            "PUBLIC_POLICY",
            "allowed_environment_variables contains an invalid name",
        )

    if any(item.severity == "blocking" for item in findings):
        return None

    return PublicPolicy(
        forbidden_literals=tuple(literal_values),
        forbidden_regexes=tuple(compiled_regexes),
        forbidden_domains=frozenset(value.casefold().rstrip(".") for value in domain_values),
        allowed_environment_variables=frozenset(environment_values),
        allowed_email_domains=frozenset(
            value.casefold().rstrip(".") for value in email_domain_values
        ),
    )


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
    elif len(description) > DESCRIPTION_REVIEW_CHARS:
        add(
            findings,
            "warning",
            "description-long",
            relative,
            f"description exceeds the {DESCRIPTION_REVIEW_CHARS}-character review goal",
            3,
        )

    if not text[closing + 5 :].strip():
        add(findings, "blocking", "body-empty", relative, "skill body is empty")

    line_count = len(text.splitlines())
    word_count = len(re.findall(r"\S+", text))
    if line_count > SKILL_MAX_LINES:
        add(
            findings,
            "blocking",
            "skill-entrypoint-over-limit",
            relative,
            f"SKILL.md has {line_count} lines; completion limit is {SKILL_MAX_LINES}",
        )
    elif line_count > SKILL_REVIEW_LINES:
        add(
            findings,
            "warning",
            "skill-entrypoint-large",
            relative,
            f"SKILL.md has {line_count} lines; structural review begins above {SKILL_REVIEW_LINES}",
        )
    if word_count > SKILL_REVIEW_WORDS:
        add(
            findings,
            "warning",
            "skill-entrypoint-wordy",
            relative,
            f"SKILL.md has {word_count} words; review goal is {SKILL_REVIEW_WORDS}",
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


def mask_fenced_code(text: str) -> str:
    """Replace fenced-code content with spaces while preserving offsets and lines."""
    masked: list[str] = []
    fence_character: str | None = None
    fence_length = 0

    for line in text.splitlines(keepends=True):
        content = line.rstrip("\r\n")
        opening = re.match(r"^ {0,3}(`{3,}|~{3,})", content)

        if fence_character is None:
            if opening is None:
                masked.append(line)
                continue
            fence_character = opening.group(1)[0]
            fence_length = len(opening.group(1))
        else:
            closing = re.match(
                rf"^ {{0,3}}{re.escape(fence_character)}{{{fence_length},}}[ \t]*$",
                content,
            )
            if closing is not None:
                fence_character = None
                fence_length = 0

        masked.append("".join(char if char in "\r\n" else " " for char in line))

    return "".join(masked)


def scan_links(
    root: Path,
    markdown_path: Path,
    text: str,
    findings: list[Finding],
) -> None:
    link_text = mask_fenced_code(text)
    for match in INLINE_LINK_RE.finditer(link_text):
        target = match.group("angle") or match.group("plain")
        line = text.count("\n", 0, match.start()) + 1
        check_local_target(root, markdown_path, target, line, findings)

    definitions: dict[str, str] = {}
    for match in REFERENCE_DEF_RE.finditer(link_text):
        identifier = match.group("id").strip().casefold()
        target = match.group("angle") or match.group("plain")
        definitions[identifier] = target
        line = text.count("\n", 0, match.start()) + 1
        check_local_target(root, markdown_path, target, line, findings)

    for match in REFERENCE_USE_RE.finditer(link_text):
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


def domain_matches(domain: str, candidates: frozenset[str]) -> bool:
    normalized = domain.casefold().rstrip(".")
    return any(
        normalized == candidate or normalized.endswith(f".{candidate}")
        for candidate in candidates
    )


def is_reserved_example_domain(domain: str) -> bool:
    normalized = domain.casefold().rstrip(".")
    return (
        normalized in {"example.com", "example.net", "example.org"}
        or normalized.endswith(".example")
        or normalized.endswith(".invalid")
        or normalized.endswith(".test")
    )


def is_private_ip(host: str) -> bool:
    try:
        address = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        return False
    return address.is_private and not address.is_loopback


def is_reserved_example_ip(host: str) -> bool:
    try:
        address = ipaddress.ip_address(host.strip("[]"))
    except ValueError:
        return False
    if address.version != 4:
        return False
    return any(
        address in network
        for network in (
            ipaddress.ip_network("192.0.2.0/24"),
            ipaddress.ip_network("198.51.100.0/24"),
            ipaddress.ip_network("203.0.113.0/24"),
        )
    )


def add_public_match(
    findings: list[Finding],
    code: str,
    relative: Path,
    message: str,
    text: str,
    start: int,
) -> None:
    add(
        findings,
        "blocking",
        code,
        relative,
        message,
        text.count("\n", 0, start) + 1,
    )


def scan_public_policy_terms(
    relative: Path,
    text: str,
    policy: PublicPolicy,
    findings: list[Finding],
) -> None:
    folded = text.casefold()
    for index, literal in enumerate(policy.forbidden_literals, start=1):
        needle = literal.casefold()
        start = 0
        while True:
            match_at = folded.find(needle, start)
            if match_at < 0:
                break
            add_public_match(
                findings,
                "public-private-term",
                relative,
                f"content matches private literal policy entry {index}",
                text,
                match_at,
            )
            start = match_at + max(len(needle), 1)

    for index, pattern in enumerate(policy.forbidden_regexes, start=1):
        for match in pattern.finditer(text):
            add_public_match(
                findings,
                "public-private-pattern",
                relative,
                f"content matches private regex policy entry {index}",
                text,
                match.start(),
            )


def scan_public_urls(
    relative: Path,
    text: str,
    policy: PublicPolicy,
    findings: list[Finding],
) -> None:
    for match in URL_RE.finditer(text):
        raw_url = match.group(0).rstrip(".,;:`]}")
        parseable_url = re.sub(
            r"\[[A-Za-z][A-Za-z0-9_-]*]",
            "placeholder",
            raw_url,
        )
        try:
            parsed = urlsplit(parseable_url)
        except ValueError:
            add_public_match(
                findings,
                "public-malformed-url",
                relative,
                "URL-like content cannot be safely parsed",
                text,
                match.start(),
            )
            continue
        host = parsed.hostname or ""
        password = unquote(parsed.password or "")
        if password and not PLACEHOLDER_VALUE_RE.fullmatch(password):
            add_public_match(
                findings,
                "public-credential-url",
                relative,
                "URL contains embedded credentials",
                text,
                match.start(),
            )
        if (
            (":" in host and is_private_ip(host))
            or domain_matches(host, policy.forbidden_domains)
        ):
            add_public_match(
                findings,
                "public-private-host",
                relative,
                "URL references a private host or address",
                text,
                match.start(),
            )


def scan_public_text(
    relative: Path,
    text: str,
    policy: PublicPolicy,
    findings: list[Finding],
) -> None:
    scan_public_policy_terms(relative, text, policy, findings)

    for match in ENVIRONMENT_REFERENCE_RE.finditer(text):
        name = next(value for value in match.groupdict().values() if value)
        if name not in policy.allowed_environment_variables:
            add_public_match(
                findings,
                "public-environment-variable",
                relative,
                "environment variable is not allowlisted for publication",
                text,
                match.start(),
            )

    if (
        relative.suffix.casefold() in ENVIRONMENT_ASSIGNMENT_SUFFIXES
        or relative.name.casefold() in {"dockerfile", "makefile"}
    ):
        for match in BARE_ENVIRONMENT_ASSIGNMENT_RE.finditer(text):
            name = match.group("assigned")
            if name not in policy.allowed_environment_variables:
                add_public_match(
                    findings,
                    "public-environment-variable",
                    relative,
                    "environment variable is not allowlisted for publication",
                    text,
                    match.start(),
                )

    for match in ABSOLUTE_PRIVATE_PATH_RE.finditer(text):
        add_public_match(
            findings,
            "public-private-path",
            relative,
            "absolute user or workstation path detected",
            text,
            match.start(),
        )

    for match in PRIVATE_HOST_RE.finditer(text):
        add_public_match(
            findings,
            "public-private-host",
            relative,
            "private hostname detected",
            text,
            match.start(),
        )

    for match in IPV4_RE.finditer(text):
        address = match.group(0)
        if not is_private_ip(address) or is_reserved_example_ip(address):
            continue
        add_public_match(
            findings,
            "public-private-address",
            relative,
            "private address detected",
            text,
            match.start(),
        )

    for match in PRIVATE_CONTEXT_RE.finditer(text):
        add_public_match(
            findings,
            "public-private-context",
            relative,
            "concrete private architecture context requires removal",
            text,
            match.start(),
        )

    for code, pattern, message in SECRET_VALUE_PATTERNS:
        for match in pattern.finditer(text):
            add_public_match(
                findings,
                code,
                relative,
                message,
                text,
                match.start(),
            )

    for match in GENERIC_SECRET_ASSIGNMENT_RE.finditer(text):
        value = match.group("value")
        if "(" in value or PLACEHOLDER_VALUE_RE.fullmatch(value):
            continue
        add_public_match(
            findings,
            "public-secret-assignment",
            relative,
            "non-placeholder secret-like assignment detected",
            text,
            match.start(),
        )

    for match in EMAIL_RE.finditer(text):
        domain = match.group("domain").casefold().rstrip(".")
        if (
            is_reserved_example_domain(domain)
            or domain_matches(domain, policy.allowed_email_domains)
        ):
            continue
        add_public_match(
            findings,
            "public-email",
            relative,
            "email address is not allowlisted for publication",
            text,
            match.start(),
        )

    scan_public_urls(relative, text, policy, findings)


def scan_public_path(
    relative: Path,
    policy: PublicPolicy,
    findings: list[Finding],
) -> None:
    normalized = relative.as_posix()
    if any(ord(character) > 127 for character in normalized):
        add(
            findings,
            "blocking",
            "public-non-ascii-path",
            relative,
            "non-ASCII package path may hide a homoglyph or non-portable filename",
        )
    if SENSITIVE_PACKAGE_PATH_RE.search(normalized):
        add(
            findings,
            "blocking",
            "public-sensitive-file",
            relative,
            "secret-bearing or credential file type is not publishable",
        )
    scan_public_policy_terms(relative, normalized, policy, findings)


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
    public_policy: PublicPolicy | None = None,
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
    if public_policy is not None:
        scan_public_text(relative, text, public_policy, findings)


def scan_tree(
    root: Path,
    findings: list[Finding],
    public_policy: PublicPolicy | None = None,
) -> None:
    for path, skipped in iter_paths(root):
        relative = path.relative_to(root)
        if public_policy is not None:
            scan_public_path(relative, public_policy, findings)
        if skipped:
            add(
                findings,
                "blocking" if public_policy is not None else "warning",
                (
                    "public-unscanned-directory"
                    if public_policy is not None
                    else "skipped-directory"
                ),
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

        scan_text(root, path, text, findings, public_policy)


def scan_skill(
    root: Path,
    public_policy: PublicPolicy | None = None,
) -> list[Finding]:
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
    if public_policy is not None:
        scan_public_policy_terms(
            Path("."),
            root.name,
            public_policy,
            findings,
        )

    skill_md = root / "SKILL.md"
    if not skill_md.is_file():
        add(
            findings,
            "blocking",
            "skill-md-missing",
            Path("SKILL.md"),
            "SKILL.md is missing",
        )
        scan_tree(root, findings, public_policy)
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

    scan_tree(root, findings, public_policy)
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
    parser.add_argument(
        "--public-policy",
        type=Path,
        help=(
            "enable blocking public-release checks using an ignored private JSON policy"
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.skill_dir.expanduser().absolute()
    policy_findings: list[Finding] = []
    public_policy = None
    public_policy_sha256 = None
    if args.public_policy is not None:
        public_policy_path = args.public_policy.expanduser().absolute()
        public_policy = load_public_policy(public_policy_path, policy_findings)
        if public_policy is not None:
            public_policy_sha256 = hashlib.sha256(
                public_policy_path.read_bytes()
            ).hexdigest()
    findings = policy_findings + scan_skill(root, public_policy)
    findings = sorted(
        set(findings),
        key=lambda item: (
            0 if item.severity == "blocking" else 1,
            item.path,
            item.line or 0,
            item.code,
            item.message,
        ),
    )
    blocking = sum(item.severity == "blocking" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)
    displayed_target = root.name if args.public_policy is not None else str(root)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "target": displayed_target,
                    "public_policy_sha256": public_policy_sha256,
                    "blocking": blocking,
                    "warnings": warnings,
                    "findings": [asdict(item) for item in findings],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(f"target: {displayed_target}")
        if public_policy_sha256 is not None:
            print(f"public policy sha256: {public_policy_sha256}")
        print(f"blocking: {blocking}; warnings: {warnings}")
        for item in findings:
            location = item.path
            if item.line is not None:
                location += f":{item.line}"
            print(f"[{item.severity}] {item.code} {location} - {item.message}")

    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
