#!/usr/bin/env python3
"""Validate skill directory naming across plugin manifests."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


SOURCE_ROOT = Path(__file__).resolve().parent.parent
SKILL_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CANONICAL_EXCEPTIONS = {("qa", "agent-browser")}


def plugin_manifest_paths() -> list[Path]:
    return sorted(SOURCE_ROOT.glob("plugins/*/.claude-plugin/plugin.json"))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_skill_name(skill_md_path: Path) -> str | None:
    lines = skill_md_path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None

    for line in lines[1:40]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return None


def validate() -> list[str]:
    errors: list[str] = []
    referenced_dirs: set[Path] = set()

    for manifest_path in plugin_manifest_paths():
        plugin_dir = manifest_path.parents[1]
        plugin_slug = plugin_dir.name
        manifest = read_json(manifest_path)

        for skill_entry in manifest.get("skills", []):
            skill_dir = plugin_dir / skill_entry.replace("./skills/", "skills/")
            skill_slug = skill_dir.name
            referenced_dirs.add(skill_dir.resolve())

            if not skill_dir.exists():
                errors.append(f"missing skill directory: {skill_dir}")
                continue

            if not SKILL_SLUG_RE.match(skill_slug):
                errors.append(
                    f"invalid skill slug '{skill_slug}' in {skill_dir}; use lowercase kebab-case"
                )

            skill_md_path = skill_dir / "SKILL.md"
            if not skill_md_path.exists():
                errors.append(f"missing SKILL.md: {skill_md_path}")
                continue

            frontmatter_name = read_skill_name(skill_md_path)
            if frontmatter_name is None:
                errors.append(f"missing frontmatter name in {skill_md_path}")
            elif frontmatter_name != skill_slug:
                errors.append(
                    f"frontmatter name mismatch in {skill_md_path}: expected '{skill_slug}', got '{frontmatter_name}'"
                )

            if skill_slug.startswith(f"{plugin_slug}-"):
                continue

            if (plugin_slug, skill_slug) in CANONICAL_EXCEPTIONS:
                continue

            errors.append(
                f"non-canonical skill name: {plugin_slug}/{skill_slug}; expected prefix '{plugin_slug}-'"
            )

    for skill_md_path in sorted(SOURCE_ROOT.glob("plugins/*/skills/*/SKILL.md")):
        skill_dir = skill_md_path.parent.resolve()
        if skill_dir not in referenced_dirs:
            errors.append(f"unreferenced skill directory: {skill_dir}")

    return errors


def main() -> int:
    errors = validate()

    if errors:
        print("Errors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("Skill naming is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
