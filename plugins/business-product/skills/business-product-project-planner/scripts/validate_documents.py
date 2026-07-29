#!/usr/bin/env python3
"""
Document Validator
Validates project planning documents for completeness and consistency
"""

import re
import argparse
import sys
from typing import List, Dict, Tuple
from pathlib import Path

max_document_bytes = 2 * 1024 * 1024


def read_document(file_name: str) -> str:
    """Read a bounded regular UTF-8 document without following its final link."""
    path = Path(file_name)
    metadata = path.lstat()
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Document must be a regular non-symlink file: {path}")
    if path.absolute() != path.resolve():
        raise ValueError(f"Document path must not traverse symlinks: {path}")
    if metadata.st_size > max_document_bytes:
        raise ValueError(
            f"Document exceeds {max_document_bytes} bytes: {path}"
        )
    return path.read_text(encoding="utf-8")


def requirement_ids(content: str) -> List[str]:
    """Return normalized requirement IDs in document order."""
    return [
        f"REQ-{match.group(1)}"
        for match in re.finditer(
            r"^###\s+(?:REQ-|Requirement\s+)(\d+)(?:\b|:)",
            content,
            re.MULTILINE,
        )
    ]


def referenced_requirement_ids(content: str) -> List[str]:
    """Return requirement IDs used in explicit task traceability fields."""
    ids = []
    for line in content.splitlines():
        if "_Requirements:" in line or "Requirements:" in line:
            ids.extend(re.findall(r"(?<![A-Za-z0-9])REQ-\d+(?!\d)", line))
    return ids


def component_ids(content: str) -> List[str]:
    """Return component IDs declared in Markdown table rows."""
    return [
        match.group(1)
        for match in re.finditer(
            r"^\|\s*(COMP-\d+)\s*\|",
            content,
            re.MULTILINE,
        )
    ]


def referenced_component_ids(content: str) -> List[str]:
    """Return component IDs used in explicit task traceability fields."""
    ids = []
    for line in content.splitlines():
        if any(
            field in line
            for field in ("_Components:", "Components:", "_Design:", "Design:")
        ):
            ids.extend(re.findall(r"(?<![A-Za-z0-9])COMP-\d+(?!\d)", line))
    return ids


def design_ids(content: str) -> List[str]:
    """Return design IDs declared by component/decision rows or interface/flow headings."""
    ids = []
    ids.extend(
        match.group(1)
        for match in re.finditer(
            r"^\|\s*((?:COMP|DEC)-\d+)\s*\|",
            content,
            re.MULTILINE,
        )
    )
    ids.extend(
        match.group(1)
        for match in re.finditer(
            r"^###\s+((?:INT|FLOW)-\d+)(?:\b|:)",
            content,
            re.MULTILINE,
        )
    )
    return ids


def referenced_design_ids(content: str) -> List[str]:
    """Return design IDs from explicit task design or component fields."""
    ids = []
    for line in content.splitlines():
        if any(
            field in line
            for field in ("_Components:", "Components:", "_Design:", "Design:")
        ):
            ids.extend(
                re.findall(
                    r"(?<![A-Za-z0-9])(?:DEC|INT|FLOW)-\d+(?!\d)",
                    line,
                )
            )
    return ids


def task_records(content: str) -> List[Tuple[str, str]]:
    """Return task IDs and checkbox states from actual task records."""
    return [
        (match.group(2), match.group(1).lower())
        for match in re.finditer(
            r"^\s*-\s*\[([ xX~])\]\s+(TASK-\d+|\d+\.\d+)\b",
            content,
            re.MULTILINE,
        )
    ]


def task_ids(content: str) -> List[str]:
    """Return stable task IDs from checked or unchecked task records."""
    return [task_id for task_id, _ in task_records(content)]


def traceability_references(content: str) -> Dict[str, List[str]]:
    """Extract IDs from rows in the canonical requirements traceability table."""
    references: Dict[str, List[str]] = {
        "requirements": [],
        "design": [],
        "tasks": [],
    }
    in_traceability = False

    for line in content.splitlines():
        if re.match(r"^##\s+Traceability\s*$", line, re.IGNORECASE):
            in_traceability = True
            continue
        if in_traceability and re.match(r"^##\s+", line):
            break
        if not in_traceability or not re.match(r"^\s*\|", line):
            continue

        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not re.fullmatch(r"REQ-\d+", cells[0]):
            continue
        references["requirements"].append(cells[0])
        references["design"].extend(
            re.findall(r"(?<![A-Za-z0-9])(?:COMP|DEC|INT|FLOW)-\d+(?!\d)", cells[1])
        )
        references["tasks"].extend(
            re.findall(r"(?<![A-Za-z0-9])(?:TASK-\d+|\d+\.\d+)(?!\d)", cells[2])
        )

    return references


def task_dependency_graph(content: str) -> Dict[str, List[str]]:
    """Map task IDs to task IDs named in their dependency fields."""
    graph: Dict[str, List[str]] = {}
    current_task = None
    task_pattern = re.compile(
        r"^\s*-\s*\[[ xX~]\]\s+(TASK-\d+|\d+\.\d+)\b"
    )
    for line in content.splitlines():
        task_match = task_pattern.match(line)
        if task_match:
            current_task = task_match.group(1)
            graph.setdefault(current_task, [])
            continue
        if current_task and ("_Dependencies:" in line or "Dependencies:" in line):
            graph[current_task].extend(
                re.findall(r"(?<![A-Za-z0-9])(?:TASK-\d+|\d+\.\d+)(?!\d)", line)
            )
    return graph


def dependency_cycles(graph: Dict[str, List[str]]) -> List[List[str]]:
    """Return deterministic task dependency cycles."""
    cycles = []
    state = {}
    stack = []

    def visit(node):
        state[node] = "active"
        stack.append(node)
        for dependency in graph.get(node, []):
            if dependency not in graph:
                continue
            if state.get(dependency) == "active":
                start = stack.index(dependency)
                cycle = stack[start:] + [dependency]
                if cycle not in cycles:
                    cycles.append(cycle)
            elif state.get(dependency) is None:
                visit(dependency)
        stack.pop()
        state[node] = "done"

    for task_id in graph:
        if state.get(task_id) is None:
            visit(task_id)
    return cycles


class DocumentValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        
    def validate_requirements(self, content: str) -> Tuple[List[str], List[str]]:
        """Validate requirements document structure and content"""
        errors = []
        warnings = []
        
        # Check required sections
        required_section_groups = [
            ("Introduction or Purpose and Outcomes", ("## Introduction", "## Purpose and Outcomes")),
            ("Glossary", ("## Glossary",)),
            ("Requirements", ("## Requirements", "## Functional Requirements")),
        ]

        for label, alternatives in required_section_groups:
            if not any(section in content for section in alternatives):
                errors.append(f"Missing required section: {label}")
        
        # Check for user stories
        user_story_pattern = (
            r"^\*\*User Story:\*\*[^\n]*\bAs an?\b[^\n]*\bI want\b"
            r"[^\n]*\bso that\b"
        )
        has_user_story = re.search(
            user_story_pattern,
            content,
            re.MULTILINE | re.IGNORECASE,
        )
        if not has_user_story and "**Outcome:**" not in content:
            warnings.append("No user stories found in requirements")
        
        # Check for acceptance criteria
        if (
            "Acceptance Criteria" not in content
            and "Acceptance evidence" not in content
        ):
            errors.append("No acceptance criteria or evidence found")
        
        # Check for SHALL statements
        observable_pattern = (
            r"\b(?:SHALL|MUST)\b"
            r"|\bGIVEN\b[^\n]*\bWHEN\b[^\n]*\bTHEN\b"
        )
        if not re.search(observable_pattern, content, re.IGNORECASE):
            warnings.append("No observable normative or scenario criteria found")
        
        # Check for requirement numbering
        req_matches = requirement_ids(content)
        if not req_matches:
            errors.append("No numbered requirements found")
        duplicates = sorted(
            req_id for req_id in set(req_matches) if req_matches.count(req_id) > 1
        )
        if duplicates:
            errors.append("Duplicate requirement IDs: " + ", ".join(duplicates))
        
        # Check for placeholders
        placeholder_pattern = r"\[[A-Z][A-Z0-9 _/.-]{2,}\]"
        placeholders = re.findall(placeholder_pattern, content)
        if placeholders:
            warnings.append(
                f"Found {len(placeholders)} unresolved planning placeholders"
            )
        
        return errors, warnings
    
    def validate_design(self, content: str) -> Tuple[List[str], List[str]]:
        """Validate design document structure and content"""
        errors = []
        warnings = []
        
        # Check required sections
        required_section_groups = [
            ("Overview or Context and Goals", ("## Overview", "## Context and Goals")),
            ("Architecture or System Boundary", ("## System Architecture", "## System Boundary")),
            ("Data Flow", ("## Data Flow", "## End-to-End Flows")),
            ("Interfaces", ("## Integration Points", "## Interfaces and Integration Points")),
            ("Components", ("## Components", "## Component Responsibilities")),
            ("Data", ("## Data Models", "## Data and State")),
            ("Deployment", ("## Deployment", "## Deployment and Environments")),
        ]

        for label, alternatives in required_section_groups:
            if not any(section in content for section in alternatives):
                errors.append(f"Missing required section: {label}")
        
        # Check for component map
        if "Component Map" not in content and "| Component ID |" not in content:
            errors.append("Missing Component Map table")
        design_component_ids = component_ids(content)
        if not design_component_ids:
            errors.append("No numbered components found")
        duplicate_components = sorted(
            component_id
            for component_id in set(design_component_ids)
            if design_component_ids.count(component_id) > 1
        )
        if duplicate_components:
            errors.append(
                "Duplicate component IDs: " + ", ".join(duplicate_components)
            )
        declared_design_ids = design_ids(content)
        duplicate_design_ids = sorted(
            design_id
            for design_id in set(declared_design_ids)
            if declared_design_ids.count(design_id) > 1
        )
        if duplicate_design_ids:
            errors.append(
                "Duplicate design IDs: " + ", ".join(duplicate_design_ids)
            )
        
        # Check for system boundaries
        if "System Boundaries" not in content and "In Scope" not in content:
            warnings.append("Missing System Boundaries definition")
        
        # Check for architecture diagram
        if "```" not in content and "┌" not in content:
            warnings.append("No architecture diagram found")
        
        # Check for interfaces
        if (
            "class" not in content
            and "interface" not in content.lower()
            and not re.search(r"\bINT-\d+\b", content)
        ):
            warnings.append("No interface definitions found")
        
        # Check for error handling
        if "Error Handling" not in content and "error handling" not in content.lower():
            warnings.append("No error handling section found")
        
        # Check for performance targets
        if "Performance" not in content and "performance" not in content.lower():
            warnings.append("No performance targets specified")
        
        return errors, warnings
    
    def validate_tasks(self, content: str) -> Tuple[List[str], List[str]]:
        """Validate implementation plan structure and content"""
        errors = []
        warnings = []
        
        # Check for project boundaries
        if (
            "## Project Boundaries" not in content
            and "## Boundaries and Non-Goals" not in content
        ):
            errors.append("Missing Project Boundaries section")
        
        if "Must Have" not in content and "In scope:" not in content:
            warnings.append("Missing 'Must Have' scope definition")
        
        if "Out of Scope" not in content and "Out of scope:" not in content:
            warnings.append("Missing 'Out of Scope' definition")
        
        # Check for deliverables
        if not any(
            section in content
            for section in (
                "## Deliverables",
                "Deliverables by Phase",
                "## Milestones or Vertical Slices",
                "## Tasks",
            )
        ):
            warnings.append("Missing Deliverables section")
        
        # Check for success criteria
        if "Success Criteria" not in content and "Completion:" not in content:
            warnings.append("Missing Success Criteria for deliverables")

        tasks = task_ids(content)
        if not tasks:
            errors.append("No tasks found in implementation plan")
        duplicate_tasks = sorted(
            task_id for task_id in set(tasks) if tasks.count(task_id) > 1
        )
        if duplicate_tasks:
            errors.append("Duplicate task IDs: " + ", ".join(duplicate_tasks))
        
        # Check for requirement tracing
        req_traces = [
            line for line in content.splitlines()
            if referenced_requirement_ids(line)
        ]
        
        if len(req_traces) == 0:
            warnings.append("No requirement tracing found in tasks")
        elif len(req_traces) < len(tasks):
            warnings.append(
                f"{len(req_traces)} of {len(tasks)} tasks have requirement tracing"
            )
        
        # Check for component involvement
        comp_pattern = r"_Components:.*COMP-\d+"
        comp_traces = re.findall(comp_pattern, content)
        
        if len(comp_traces) == 0:
            warnings.append("No component mapping found in tasks")
        
        # Check for dependencies
        graph = task_dependency_graph(content)
        dependencies = [
            dependency
            for task_dependencies in graph.values()
            for dependency in task_dependencies
        ]
        if not dependencies:
            warnings.append("No task dependencies defined")
        dangling_dependencies = sorted(set(dependencies) - set(tasks))
        if dangling_dependencies:
            errors.append(
                "Tasks reference unknown dependencies: "
                + ", ".join(dangling_dependencies)
            )
        cycles = dependency_cycles(graph)
        if cycles:
            errors.extend(
                "Task dependency cycle: " + " -> ".join(cycle)
                for cycle in cycles
            )

        # Report completion only for parsed task records, never arbitrary
        # checklists or phase headings.
        records = task_records(content)
        completed = sum(state == "x" for _, state in records)
        if records:
            completion_rate = (completed / len(records)) * 100
            print(
                f"Task completion: {completed}/{len(records)} "
                f"({completion_rate:.1f}%)"
            )
        
        return errors, warnings
    
    def validate_consistency(self, req_content: str, design_content: str, 
                           task_content: str) -> Tuple[List[str], List[str]]:
        """Check consistency across documents"""
        errors = []
        warnings = []
        
        # Extract requirement IDs from requirements and task documents.
        req_ids = set(requirement_ids(req_content))
        task_req_ids = set(referenced_requirement_ids(task_content))
        dangling = sorted(task_req_ids - req_ids)
        if dangling:
            errors.append(
                "Tasks reference unknown requirements: " + ", ".join(dangling)
            )
        
        # Check if requirements are referenced in tasks
        for req_id in sorted(req_ids):
            if req_id not in task_req_ids:
                warnings.append(f"{req_id} not referenced in any tasks")
        
        design_component_ids = set(component_ids(design_content))
        task_component_ids = set(referenced_component_ids(task_content))
        dangling_components = sorted(task_component_ids - design_component_ids)
        if dangling_components:
            errors.append(
                "Tasks reference unknown components: "
                + ", ".join(dangling_components)
            )
        if task_component_ids:
            for component_id in sorted(design_component_ids - task_component_ids):
                warnings.append(f"{component_id} not referenced in any tasks")

        declared_design_ids = set(design_ids(design_content))
        task_design_ids = set(referenced_design_ids(task_content))
        dangling_design_ids = sorted(task_design_ids - declared_design_ids)
        if dangling_design_ids:
            errors.append(
                "Tasks reference unknown design IDs: "
                + ", ".join(dangling_design_ids)
            )

        traceability = traceability_references(req_content)
        duplicate_trace_rows = sorted(
            req_id
            for req_id in set(traceability["requirements"])
            if traceability["requirements"].count(req_id) > 1
        )
        if duplicate_trace_rows:
            errors.append(
                "Duplicate traceability rows: " + ", ".join(duplicate_trace_rows)
            )

        dangling_trace_requirements = sorted(
            set(traceability["requirements"]) - req_ids
        )
        if dangling_trace_requirements:
            errors.append(
                "Traceability references unknown requirements: "
                + ", ".join(dangling_trace_requirements)
            )

        dangling_trace_design = sorted(
            set(traceability["design"]) - declared_design_ids
        )
        if dangling_trace_design:
            errors.append(
                "Traceability references unknown design IDs: "
                + ", ".join(dangling_trace_design)
            )

        declared_task_ids = set(task_ids(task_content))
        dangling_trace_tasks = sorted(
            set(traceability["tasks"]) - declared_task_ids
        )
        if dangling_trace_tasks:
            errors.append(
                "Traceability references unknown tasks: "
                + ", ".join(dangling_trace_tasks)
            )
        
        return errors, warnings
    
    def validate_all(self, req_file: str, design_file: str, 
                     task_file: str) -> Dict[str, Tuple[List[str], List[str]]]:
        """Validate all three documents"""
        results = {}
        
        # Read files
        req_content = read_document(req_file)
        design_content = read_document(design_file)
        task_content = read_document(task_file)
        
        # Validate individual documents
        results['requirements'] = self.validate_requirements(req_content)
        results['design'] = self.validate_design(design_content)
        results['tasks'] = self.validate_tasks(task_content)
        
        # Validate consistency
        results['consistency'] = self.validate_consistency(
            req_content, design_content, task_content
        )
        
        return results

def print_validation_results(results: Dict[str, Tuple[List[str], List[str]]]):
    """Print validation results in a formatted way"""
    
    total_errors = 0
    total_warnings = 0
    
    for doc_name, (errors, warnings) in results.items():
        print(f"\n{'='*50}")
        print(f"Validation Results: {doc_name.upper()}")
        print('='*50)
        
        if errors:
            print(f"\n❌ Errors ({len(errors)}):")
            for error in errors:
                print(f"  - {error}")
            total_errors += len(errors)
        else:
            print("\n✅ No errors found")
        
        if warnings:
            print(f"\n⚠️  Warnings ({len(warnings)}):")
            for warning in warnings:
                print(f"  - {warning}")
            total_warnings += len(warnings)
        else:
            print("\n✅ No warnings found")
    
    # Summary
    print(f"\n{'='*50}")
    print("SUMMARY")
    print('='*50)
    
    if total_errors == 0 and total_warnings == 0:
        print("✅ No structural findings; semantic review is still required")
    else:
        print(f"Total Errors: {total_errors}")
        print(f"Total Warnings: {total_warnings}")
        
        if total_errors > 0:
            print("\n⚠️  Please fix errors before using these documents")
        else:
            print("\n📝 Review warnings to improve document quality")

def main():
    parser = argparse.ArgumentParser(description="Validate project planning documents")
    parser.add_argument("--requirements", "-r", default="requirements.md",
                      help="Path to requirements document")
    parser.add_argument("--design", "-d", default="design.md",
                      help="Path to design document")
    parser.add_argument("--tasks", "-t", default="tasks.md",
                      help="Path to tasks/implementation plan")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return non-zero when warnings remain",
    )
    
    args = parser.parse_args()
    
    # Check if files exist
    for filepath, name in [(args.requirements, "Requirements"),
                          (args.design, "Design"),
                          (args.tasks, "Tasks")]:
        if not Path(filepath).exists():
            print(f"❌ {name} file not found: {filepath}")
            return 1
    
    # Validate documents
    validator = DocumentValidator()
    try:
        results = validator.validate_all(
            args.requirements,
            args.design,
            args.tasks,
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    
    # Print results
    print_validation_results(results)
    
    # Return exit code based on errors
    total_errors = sum(len(errors) for errors, _ in results.values())
    total_warnings = sum(len(warnings) for _, warnings in results.values())
    return 1 if total_errors > 0 or (args.strict and total_warnings > 0) else 0

if __name__ == "__main__":
    raise SystemExit(main())
