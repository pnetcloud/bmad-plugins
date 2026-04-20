#!/usr/bin/env python3
"""Sync BMAD agent customizations into an installed project's _bmad folder."""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path

import yaml


SOURCE_ROOT = Path(__file__).resolve().parent.parent
CUSTOMIZATION_DIR = SOURCE_ROOT / "customizations" / "agents"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=".", help="Installed BMAD project root.")
    parser.add_argument("--check", action="store_true", help="Show planned actions without writing.")
    return parser.parse_args()


def load_agent_manifest(project_root: Path) -> list[dict[str, str]]:
    manifest_path = project_root / "_bmad" / "_config" / "agent-manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"Missing agent manifest: {manifest_path}")
    with manifest_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_target(name: str) -> tuple[str, str]:
    suffix = ".customize.yaml"
    if not name.endswith(suffix):
        raise ValueError(f"Unsupported file name: {name}")
    stem = name[: -len(suffix)]
    if "-" not in stem:
        raise ValueError(f"Customization file must look like <module>-<agent>.customize.yaml: {name}")
    return stem.split("-", 1)


def agent_exists(rows: list[dict[str, str]], module: str, short_name: str) -> bool:
    for row in rows:
        if row["module"] != module:
            continue
        skill_name = row["name"]
        canonical = row.get("canonicalId", "") or ""
        if skill_name == short_name or skill_name.endswith(f"-{short_name}"):
            return True
        if canonical and (canonical == short_name or canonical.endswith(f"-{short_name}")):
            return True
    return False


def validate_yaml(path: Path) -> None:
    yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    target_dir = project_root / "_bmad" / "_config" / "agents"

    if not CUSTOMIZATION_DIR.exists():
        print(f"Missing customization directory: {CUSTOMIZATION_DIR}", file=sys.stderr)
        return 1

    rows = load_agent_manifest(project_root)
    files = sorted(CUSTOMIZATION_DIR.glob("*.customize.yaml"))
    if not files:
        print(f"No customization files found in {CUSTOMIZATION_DIR}", file=sys.stderr)
        return 1

    print(f"[source] {CUSTOMIZATION_DIR}")
    print(f"[target] {target_dir}")

    for source in files:
        validate_yaml(source)
        module, short_name = parse_target(source.name)
        if not agent_exists(rows, module, short_name):
            print(f"[skip] {source.name}: matching installed agent not found", file=sys.stderr)
            continue

        destination = target_dir / source.name
        if args.check:
            print(f"[check] would copy {source} -> {destination}")
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        print(f"[sync] {source.name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
