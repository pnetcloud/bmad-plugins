#!/usr/bin/env python3
"""Validate traceability and unresolved placeholders in planning documents."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


HEADING_ID = re.compile(
    r"^###\s+((?:REQ|DEC|COMP|FLOW|TASK)-[A-Z0-9][A-Z0-9.-]*)\b",
    re.MULTILINE,
)
REFERENCE = re.compile(
    r"\b((?:REQ|DEC|COMP|FLOW|TASK)-[A-Z0-9][A-Z0-9.-]*)\b"
)
PLACEHOLDER = re.compile(r"\{\{[^}\n]+\}\}|\bTBD\b|\[TODO\]", re.IGNORECASE)


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, list[str]]:
        return {"errors": self.errors, "warnings": self.warnings}


def read_text(path: Path, report: Report) -> str:
    if not path.is_file():
        report.errors.append(f"missing file: {path}")
        return ""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        report.errors.append(f"cannot read {path}: {exc}")
        return ""


def ids_with_prefix(text: str, prefix: str) -> list[str]:
    return [
        match.group(1)
        for match in HEADING_ID.finditer(text)
        if match.group(1).startswith(f"{prefix}-")
    ]


def section_bodies(text: str, prefix: str) -> dict[str, str]:
    matches = [
        match
        for match in HEADING_ID.finditer(text)
        if match.group(1).startswith(f"{prefix}-")
    ]
    sections: dict[str, str] = {}
    for match in matches:
        remaining = text[match.end() :]
        next_heading = re.search(r"^#{1,3}\s+", remaining, re.MULTILINE)
        end = match.end() + next_heading.start() if next_heading else len(text)
        sections[match.group(1)] = text[match.end() : end]
    return sections


def check_duplicates(ids: list[str], label: str, report: Report) -> None:
    for identifier, count in sorted(Counter(ids).items()):
        if count > 1:
            report.errors.append(f"duplicate {label} ID: {identifier}")


def find_references(text: str, prefix: str) -> set[str]:
    return {
        match.group(1)
        for match in REFERENCE.finditer(text)
        if match.group(1).startswith(f"{prefix}-")
    }


def check_placeholders(
    documents: dict[str, str], report: Report, allow_placeholders: bool
) -> None:
    if allow_placeholders:
        return
    for name, text in documents.items():
        count = len(PLACEHOLDER.findall(text))
        if count:
            report.errors.append(f"{name}: {count} unresolved placeholder(s)")


def check_requirements(requirements: str, report: Report) -> set[str]:
    req_ids = ids_with_prefix(requirements, "REQ")
    check_duplicates(req_ids, "requirement", report)
    if not req_ids:
        report.errors.append("requirements: no REQ-* headings")
        return set()

    for req_id, body in section_bodies(requirements, "REQ").items():
        if "Acceptance:" not in body:
            report.errors.append(f"{req_id}: missing Acceptance block")
        if not re.search(r"^\d+\.\s+", body, re.MULTILINE):
            report.errors.append(f"{req_id}: no numbered acceptance scenario")
    return set(req_ids)


def check_design(
    design: str, requirement_ids: set[str], report: Report
) -> set[str]:
    design_ids = {
        identifier
        for identifier in HEADING_ID.findall(design)
        if not identifier.startswith(("REQ-", "TASK-"))
    }
    check_duplicates(
        [
            identifier
            for identifier in HEADING_ID.findall(design)
            if not identifier.startswith(("REQ-", "TASK-"))
        ],
        "design",
        report,
    )
    referenced_requirements = find_references(design, "REQ")
    for req_id in sorted(referenced_requirements - requirement_ids):
        report.errors.append(f"design references unknown requirement: {req_id}")
    for req_id in sorted(requirement_ids - referenced_requirements):
        report.errors.append(f"requirement has no design trace: {req_id}")
    if not design_ids:
        report.warnings.append("design: no DEC, COMP, or FLOW headings")
    return design_ids


def dependency_graph(task_sections: dict[str, str]) -> dict[str, set[str]]:
    graph: dict[str, set[str]] = {}
    for task_id, body in task_sections.items():
        dependency_line = re.search(
            r"^- Dependencies:\s*(.*)$", body, re.MULTILINE
        )
        graph[task_id] = (
            find_references(dependency_line.group(1), "TASK")
            if dependency_line
            else set()
        )
    return graph


def cyclic_tasks(graph: dict[str, set[str]]) -> set[str]:
    visiting: set[str] = set()
    visited: set[str] = set()
    cycles: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            cycles.add(node)
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph.get(node, set()):
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)
    return cycles


def check_tasks(
    tasks: str,
    requirement_ids: set[str],
    design_ids: set[str],
    report: Report,
) -> set[str]:
    task_ids = ids_with_prefix(tasks, "TASK")
    check_duplicates(task_ids, "task", report)
    if not task_ids:
        report.errors.append("tasks: no TASK-* headings")
        return set()

    sections = section_bodies(tasks, "TASK")
    covered_requirements: set[str] = set()
    for task_id, body in sections.items():
        req_refs = find_references(body, "REQ")
        covered_requirements.update(req_refs)
        if not req_refs:
            report.errors.append(f"{task_id}: no requirement reference")
        if "- Validation:" not in body:
            report.errors.append(f"{task_id}: missing Validation")
        if "- Status:" not in body:
            report.warnings.append(f"{task_id}: missing Status")
        for req_id in sorted(req_refs - requirement_ids):
            report.errors.append(f"{task_id} references unknown requirement: {req_id}")
        for design_id in sorted(
            {
                ref
                for ref in REFERENCE.findall(body)
                if ref.startswith(("DEC-", "COMP-", "FLOW-"))
            }
            - design_ids
        ):
            report.errors.append(f"{task_id} references unknown design ID: {design_id}")

    for req_id in sorted(requirement_ids - covered_requirements):
        report.errors.append(f"requirement has no implementation task: {req_id}")

    graph = dependency_graph(sections)
    for task_id, dependencies in sorted(graph.items()):
        for dependency in sorted(dependencies - set(task_ids)):
            report.errors.append(f"{task_id} depends on unknown task: {dependency}")
        if task_id in dependencies:
            report.errors.append(f"{task_id} depends on itself")
    for task_id in sorted(cyclic_tasks(graph)):
        report.errors.append(f"task dependency cycle includes: {task_id}")
    return set(task_ids)


def validate(
    requirements_path: Path,
    design_path: Path,
    tasks_path: Path,
    allow_placeholders: bool = False,
) -> Report:
    report = Report()
    documents = {
        "requirements": read_text(requirements_path, report),
        "design": read_text(design_path, report),
        "tasks": read_text(tasks_path, report),
    }
    if report.errors:
        return report

    check_placeholders(documents, report, allow_placeholders)
    requirement_ids = check_requirements(documents["requirements"], report)
    design_ids = check_design(documents["design"], requirement_ids, report)
    check_tasks(documents["tasks"], requirement_ids, design_ids, report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--requirements", type=Path, required=True)
    parser.add_argument("--design", type=Path, required=True)
    parser.add_argument("--tasks", type=Path, required=True)
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="permit template placeholders during an explicitly incomplete draft",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    report = validate(
        args.requirements,
        args.design,
        args.tasks,
        allow_placeholders=args.allow_placeholders,
    )
    if args.format == "json":
        print(json.dumps(report.as_dict(), indent=2))
    else:
        for error in report.errors:
            print(f"ERROR: {error}")
        for warning in report.warnings:
            print(f"WARNING: {warning}")
        print(
            f"validation: {len(report.errors)} error(s), "
            f"{len(report.warnings)} warning(s)"
        )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
