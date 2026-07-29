#!/usr/bin/env python3
"""
Project Document Generator
Generates structured requirements, design, and task documents for new projects
"""

import argparse
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
import os
import re
import sys
import tempfile

MAX_INPUT_LENGTH = 240
OUTPUT_FILES = ("requirements.md", "design.md", "tasks.md")
DEFAULT_PROMPTS = {
    "web-app": {
        "features": [
            "to complete the primary browser-based outcome",
            "to understand and recover from invalid input",
            "to observe the status of the primary workflow",
        ],
        "components": [
            "User Interaction Boundary",
            "Application Core",
            "External or State Adapter",
        ],
    },
    "cli-tool": {
        "features": [
            "to invoke the primary command and receive a documented result",
            "to understand invalid arguments and corrective action",
            "to use configuration through an approved precedence model",
        ],
        "components": [
            "Command Interface",
            "Application Core",
            "Configuration or I/O Adapter",
        ],
    },
    "api-service": {
        "features": [
            "to call the primary interface and receive a documented result",
            "to distinguish retryable and terminal failures",
            "to use a compatible versioned contract",
        ],
        "components": [
            "API Interface",
            "Application Core",
            "External or State Adapter",
        ],
    },
    "generic": {
        "features": [
            "to complete the primary supported outcome",
            "to receive an observable failure result",
            "to verify the outcome against accepted evidence",
        ],
        "components": [
            "Primary Interface",
            "Application Core",
            "External Adapter",
        ],
    },
}


def validate_single_line(value: str, label: str) -> str:
    """Reject values that can break the generated Markdown structure."""
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text")
    cleaned = value.strip()
    if not cleaned or len(cleaned) > MAX_INPUT_LENGTH:
        raise ValueError(f"{label} must contain 1-{MAX_INPUT_LENGTH} characters")
    if any(ord(character) < 32 for character in cleaned):
        raise ValueError(f"{label} must be a single printable line")
    return cleaned


def markdown_inline(value: str) -> str:
    """Escape data that is inserted into Markdown headings, tables, or lists."""
    return (
        value.replace("\\", "\\\\")
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("|", "\\|")
    )


def python_identifier(value: str) -> str:
    """Create an illustrative identifier without changing the display name."""
    words = re.findall(r"[A-Za-z0-9]+", value)
    identifier = "".join(word[:1].upper() + word[1:] for word in words)
    if not identifier:
        return "PlannedComponent"
    if identifier[0].isdigit():
        identifier = f"Component{identifier}"
    return identifier


def reject_symlink_components(path: Path) -> None:
    """Reject an output path that traverses an existing symlink."""
    absolute = path.absolute()
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current = current / part
        if current.is_symlink():
            raise ValueError(f"Output path traverses a symlink: {current}")

class ProjectDocumentGenerator:
    def __init__(self, project_name: str, project_type: str = "web-app"):
        self.project_name = validate_single_line(project_name, "project name")
        if project_type not in DEFAULT_PROMPTS:
            raise ValueError(
                "project type must be one of: " + ", ".join(DEFAULT_PROMPTS)
            )
        self.project_type = project_type
        self.timestamp = datetime.now().strftime("%Y-%m-%d")
        
    def generate_requirements_template(self, features: List[str]) -> str:
        """Generate requirements document template"""
        if not features:
            raise ValueError("at least one feature prompt is required")
        features = [
            markdown_inline(validate_single_line(feature, f"feature {index}"))
            for index, feature in enumerate(features, 1)
        ]
        project_name = markdown_inline(self.project_name)
        
        template = f"""# Requirements Document

## Introduction

{project_name} is a [DESCRIPTION OF SYSTEM PURPOSE]. The system is designed
for [TARGET USERS] and will be deployed as [DEPLOYMENT MODEL].

- Status: Draft
- Scope owner: [ROLE OR OWNER]
- Authoritative inputs: [SOURCES]

## Glossary

- **[Term]**: [Definition specific to this system]
- **User**: [Define user types]
- **System**: The {project_name} platform

## Requirements
"""
        
        for i, feature in enumerate(features, 1):
            template += f"""
### REQ-{i}: {feature}

**User Story:** As a [USER TYPE], I want {feature}, so that [BENEFIT]
**Source/Owner:** [EVIDENCE OR DECISION OWNER]
**Priority/Status:** [PRIORITY] / Proposed

#### Acceptance Criteria

1. WHEN [trigger/condition], THE system SHALL [behavior]
2. WHERE [context applies], THE system SHALL [behavior]
3. THE system SHALL [capability] within [time limit]
4. IF [error condition], THEN THE system SHALL [handle gracefully]
5. THE system SHALL persist [data] with [attributes]
"""
        template += """
## Quality and Operational Requirements

- Performance: [APPROVED TARGET, WORKLOAD, ENVIRONMENT, AND MEASUREMENT]
- Reliability: [APPROVED AVAILABILITY AND RECOVERY OBJECTIVES]
- Security and privacy: [DATA CLASSIFICATION, THREATS, AND CONTROLS]
- Operability: [OBSERVABILITY, SUPPORT, AND MAINTENANCE OUTCOMES]

## Constraints, Risks, and Open Questions

- Constraint: [SOURCED CONSTRAINT]
- Risk: [RISK, OWNER, AND RESPONSE]
- Open question: [QUESTION, OWNER, AND DUE POINT]

## Traceability

| Requirement | Design coverage | Delivery tasks | Verification | Status |
|---|---|---|---|---|
"""
        for index in range(1, len(features) + 1):
            template += (
                f"| REQ-{index} | [DESIGN IDS] | [TASK IDS] "
                "| [EVIDENCE] | Gap |\n"
            )
        return template
    
    def generate_design_template(self, components: List[str]) -> str:
        """Generate design document template with comprehensive architecture"""
        if not components:
            raise ValueError("at least one component prompt is required")
        components = [
            markdown_inline(validate_single_line(component, f"component {index}"))
            for index, component in enumerate(components, 1)
        ]
        project_name = markdown_inline(self.project_name)
        
        template = f"""# Design Document

## Overview

The architecture for {project_name} remains a decision until the
requirements, constraints, and alternatives below are reviewed.

- Status: Draft
- Decision owner: [ROLE OR OWNER]
- Authoritative inputs: [REQUIREMENTS, CONSTRAINTS, AND EVIDENCE]

## System Architecture

### Component Map

| Component ID | Name | Type or role | Responsibility | Interfaces With |
|---|---|---|---|---|
"""
        
        for i, component in enumerate(components, 1):
            template += f"""
| COMP-{i} | {component} | [DECIDE TYPE OR ROLE] | [Responsibility] | [Components] |"""
        
        template += """

### High-Level Architecture Diagram

```
[Actor or upstream system]
            |
            | [Approved interaction and contract]
            v
[COMP-N: primary boundary]
            |
            | [Approved dependency or state transition]
            v
[External system or state owner, only if required]
```

Replace this placeholder with the accepted components and normal, degraded,
and recovery paths. Do not add a layer, protocol, or state store by convention.

## Data Flow Specifications

### Primary Data Flows

#### 1. [Primary Flow]

```
1. [Actor] → [Component]: [Input and precondition]
2. [Component] → [Component]: [Validation or transformation]
3. [Component] → [System of record]: [State transition]
4. [Component] → [Actor]: [Observable outcome]
```

**Data Transformations:**
- Step 2: [Transformation and validation]
- Step 3: [State, consistency, and failure behavior]
- Failure path: [Rejection, timeout, duplicate, or partial completion]

[Add other critical data flows]

## Integration Points

### Internal Integration Points

| Source | Target | Protocol | Data Format | Purpose |
|--------|--------|----------|-------------|---------|
| [COMP-N] | [COMP-N] | [APPROVED PROTOCOL] | [APPROVED FORMAT] | [OUTCOME] |

### External Integration Points

#### [External Service Name]

**Type:** REST API / Database / Message Queue
**Purpose:** [What this integration provides]
**Endpoint:** [URL pattern or connection details]
**Authentication:** [OAuth2, API Key, etc.]
**Rate Limits:** [Any constraints]

**Interface Contract:**
```
[METHOD] /[PATH]
Headers: { "[NON-SENSITIVE HEADER]": "[SYNTHETIC VALUE]" }
Body: { "[field]": "[type]" }
Response: { "[result]": "[type]" }
```

**Failure Contract:**
- Retryability: [WHICH FAILURES MAY BE RETRIED, BY WHOM, AND WHY]
- Limits and backpressure: [APPROVED BEHAVIOR]
- Degraded behavior: [OBSERVABLE OUTCOME]
- Recovery evidence: [TEST, TRACE, METRIC, OR REVIEW]

## System Boundaries

### In Scope
- [Core functionality included]
- [Features to be implemented]

### Out of Scope  
- [Features not included]
- [Delegated to external systems]

### Assumptions
- [External services available]
- [Infrastructure provided]

## Components and Interfaces
"""
        
        for component in components:
            identifier = python_identifier(component)
            template += f"""
### {component}

**Responsibility:** [Single sentence description of what this component does]

**Key Classes:**
- `{identifier}Boundary`: Illustrative boundary; replace with the approved form
- `{identifier}Interface`: Illustrative interface boundary
- `{identifier}Store`: Include only if this component owns persisted state

**Interfaces:**
```python
class {identifier}Interface:
    async def execute(self, request: "[APPROVED INPUT]") -> "[APPROVED RESULT]":
        ...
```

**Data Flow:**
- Receives [INPUT] from [SOURCE] under [PRECONDITION]
- Validates [RULES] and performs [APPROVED RESPONSIBILITY]
- Changes [STATE], if this component owns it
- Emits or returns [OBSERVABLE RESULT] to [DESTINATION]

**Performance:**
- Baseline: [MEASURED CURRENT BEHAVIOR]
- Target: [APPROVED METRIC, WORKLOAD, AND ENVIRONMENT]
- Verification: [MEASUREMENT METHOD]
"""
        
        template += """
## Data Models

### [Entity]
```python
@dataclass
class PlannedEntity:
    id: str
    created_at: datetime
    updated_at: datetime
```

[Add other data models]

## Error Handling

### [Failure Category]

- Trigger and scope: [CONDITION]
- Observable result: [ERROR OR DEGRADED CONTRACT]
- Retryability and idempotency: [DECISION]
- Recovery and rollback: [DECISION]
- Evidence: [TEST, TRACE, METRIC, OR REVIEW]

## Testing Strategy

### Unit Tests
- Component contract: [BEHAVIOR AND BOUNDARY]
- Decision logic: [RULES AND FAILURE CASES]
- Coverage and test scope: [APPROVED RISK-BASED TARGET]

### Integration Tests
- Interface compatibility: [INT-N]
- State or external integration: [ONLY IF REQUIRED]
- Degraded and recovery flow: [FLOW-N]

### Performance Tests
- Workload: [APPROVED CONCURRENCY AND DATA PROFILE]
- Response target: [APPROVED PERCENTILE AND THRESHOLD]
- Throughput: [APPROVED RATE AND ENVIRONMENT]

## Deployment

### Docker Configuration
```yaml
# Include only when container deployment is an accepted decision.
services:
  planned-component:
    image: "[PINNED IMAGE REFERENCE]"
    environment:
      - "[RUNTIME CONFIGURATION REFERENCE]"
```

### Environment Variables
```
[PUBLIC CONFIGURATION NAME]=[DESCRIPTION]
[SECRET REFERENCE NAME]=[EXTERNAL SECRET SOURCE]
```

## Performance Targets

- [Operation]: [APPROVED PERCENTILE AND THRESHOLD]
- [Data access]: [APPROVED DATASET AND QUERY TARGET]
- [User experience]: [APPROVED MEASURE AND ENVIRONMENT]
- [Resource]: [APPROVED LIMIT AND WORKLOAD]

## Security Considerations

- Identity and trust boundaries: [IF REQUIRED]
- Authorization model and denied behavior: [APPROVED DECISION]
- Data classification and protection: [SOURCED REQUIREMENT]
- Abuse, input, and resource controls: [THREAT-DRIVEN DECISION]
- Sensitive observability and retention: [APPROVED POLICY]
"""
        
        return template
    
    def generate_tasks_template(self, phases: List[Dict]) -> str:
        """Generate implementation plan template with boundaries and deliverables"""
        if not phases:
            raise ValueError("at least one candidate phase is required")
        
        template = f"""# Implementation Plan

Generated: {self.timestamp}
Project: {markdown_inline(self.project_name)}
Type: {self.project_type}

## Project Boundaries

### Must Have (MVP)
- [Core feature 1]
- [Core feature 2]
- [Core feature 3]

### Nice to Have (Enhancements)
- [Enhancement feature 1]
- [Enhancement feature 2]

### Out of Scope
- [Explicitly excluded feature 1]
- [Deferred to future phase]

### Technical Constraints
- [Framework limitations]
- [Resource constraints]

## Deliverables by Phase

The following phases and tasks are candidate planning prompts. Keep only those
justified by accepted requirements and design decisions; unchecked scaffolds
are not approved work.

| Phase | Deliverables | Success Criteria |
|---|---|---|
"""

        for phase_num, phase in enumerate(phases, 1):
            template += (
                f"| {phase_num}. Candidate: {phase['name']} "
                "| [REVIEWABLE DELIVERABLE] | [ACCEPTANCE EVIDENCE] |\n"
            )

        template += """

## Task Breakdown
"""
        
        for phase_num, phase in enumerate(phases, 1):
            template += f"- [ ] {phase_num}. Candidate: {phase['name']}\n\n"
            
            for task_num, task in enumerate(phase.get('tasks', []), 1):
                template += f"  - [ ] {phase_num}.{task_num} {task['name']}\n"
                
                if 'subtasks' in task:
                    for subtask in task['subtasks']:
                        template += f"    - {subtask}\n"
                
                if 'requirements' in task:
                    template += f"    - _Requirements: {', '.join(task['requirements'])}_\n"
                    
                if 'dependencies' in task and task['dependencies']:
                    template += f"    - _Dependencies: {', '.join(task['dependencies'])}_\n"
                
                template += "\n"
            
        return template
    
    def get_default_phases(self) -> List[Dict]:
        """Return neutral planning prompts for the selected project shape.

        These prompts preserve the useful project-type distinction without
        inventing a framework, datastore, authentication scheme, packaging
        channel, deployment target, or release decision.
        """

        phase_names = {
            "web-app": (
                "Interaction Contract",
                "Primary Outcome Slice",
                "Verification and Release Readiness",
            ),
            "cli-tool": (
                "Command Contract",
                "Primary Outcome Slice",
                "Packaging and Compatibility",
            ),
            "api-service": (
                "Interface Contract",
                "Primary Outcome Slice",
                "Compatibility and Operations",
            ),
            "generic": (
                "Scope and Contract",
                "Primary Outcome Slice",
                "Verification and Handoff",
            ),
        }
        contract_phase, delivery_phase, readiness_phase = phase_names[
            self.project_type
        ]

        return [
            {
                "name": contract_phase,
                "tasks": [
                    {
                        "name": "Resolve the accepted boundary and contracts",
                        "subtasks": [
                            "Map confirmed requirements to observable outcomes",
                            "Record approved interfaces, constraints, and owners",
                            "Keep unresolved choices visible as open decisions",
                        ],
                    }
                ],
            },
            {
                "name": delivery_phase,
                "tasks": [
                    {
                        "name": "Deliver one accepted vertical slice",
                        "subtasks": [
                            "Implement only approved behavior and interfaces",
                            "Preserve existing compatibility unless change is approved",
                            "Verify normal, failure, and boundary behavior",
                        ],
                        "dependencies": ["1.1"],
                    }
                ],
            },
            {
                "name": readiness_phase,
                "tasks": [
                    {
                        "name": "Prepare approved verification and handoff",
                        "subtasks": [
                            "Collect evidence for each acceptance condition",
                            "Resolve or explicitly defer remaining risks",
                            "Define rollout and rollback only when applicable",
                        ],
                        "dependencies": ["2.1"],
                    }
                ],
            },
        ]
    
    def generate_all_documents(
        self,
        features: Optional[List[str]] = None,
        components: Optional[List[str]] = None,
        output_dir: str = ".",
        force: bool = False,
    ) -> Dict[str, str]:
        """Generate all three documents"""
        
        # Use neutral, project-type-specific prompts if explicit values were not provided.
        if not features:
            features = list(DEFAULT_PROMPTS[self.project_type]["features"])
        
        if not components:
            components = list(DEFAULT_PROMPTS[self.project_type]["components"])
        
        features = [
            validate_single_line(feature, f"feature {index}")
            for index, feature in enumerate(features, 1)
        ]
        components = [
            validate_single_line(component, f"component {index}")
            for index, component in enumerate(components, 1)
        ]

        phases = self.get_default_phases()
        for phase in phases:
            for task in phase.get("tasks", []):
                # Historical defaults contained unrelated, dangling IDs. Keep
                # the task families but never claim unsupported traceability.
                task.pop("requirements", None)
        phases.append(
            {
                "name": "Requirement Delivery",
                "tasks": [
                    {
                        "name": f"Deliver requirement REQ-{index}",
                        "subtasks": [
                            f"Refine and implement: {markdown_inline(feature)}",
                            "Verify every accepted criterion",
                        ],
                        "requirements": [f"REQ-{index}"],
                    }
                    for index, feature in enumerate(features, 1)
                ],
            },
        )

        # Generate documents
        docs = {
            "requirements.md": self.generate_requirements_template(features),
            "design.md": self.generate_design_template(components),
            "tasks.md": self.generate_tasks_template(phases),
        }
        
        output_path = Path(output_dir).absolute()
        reject_symlink_components(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        if not output_path.is_dir():
            raise ValueError(f"Output path is not a directory: {output_path}")

        destinations = {name: output_path / name for name in OUTPUT_FILES}
        existing = [
            str(path)
            for path in destinations.values()
            if path.exists() or path.is_symlink()
        ]
        if existing and not force:
            raise FileExistsError(
                "Refusing to replace existing documents without --force: "
                + ", ".join(existing)
            )
        if any(path.is_symlink() for path in destinations.values()):
            raise ValueError("Refusing to replace a symlinked document")

        # Write each document to the same directory, flush it, then replace the
        # destination. Preflight above prevents a partial no-force overwrite.
        for filename, content in docs.items():
            destination = destinations[filename]
            descriptor, temporary_name = tempfile.mkstemp(
                dir=output_path,
                prefix=f".{filename}.",
                suffix=".tmp",
                text=True,
            )
            try:
                with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
                    stream.write(content)
                    stream.flush()
                    os.fsync(stream.fileno())
                os.replace(temporary_name, destination)
            except Exception:
                if os.path.exists(temporary_name):
                    os.unlink(temporary_name)
                raise
            print(f"Generated: {destination}")
        
        return docs


def main():
    parser = argparse.ArgumentParser(description="Generate project planning documents")
    parser.add_argument("project_name", help="Name of the project")
    parser.add_argument("--type", default="web-app", 
                      choices=["web-app", "cli-tool", "api-service", "generic"],
                      help="Type of project")
    parser.add_argument("--features", nargs="+", 
                      help="List of features for requirements")
    parser.add_argument("--components", nargs="+",
                      help="List of components for design")
    parser.add_argument("--output", default=".", 
                      help="Output directory for documents")
    parser.add_argument(
        "--force",
        action="store_true",
        help="replace existing generated documents after explicit review",
    )
    
    args = parser.parse_args()
    
    try:
        generator = ProjectDocumentGenerator(args.project_name, args.type)
        generator.generate_all_documents(
            features=args.features,
            components=args.components,
            output_dir=args.output,
            force=args.force,
        )
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    
    print(f"\n✅ Successfully generated project documents for '{args.project_name}'")
    print(f"   Type: {args.type}")
    print(f"   Location: {args.output}/")
    print("\nNext steps:")
    print("1. Review and customize the generated documents")
    print("2. Fill in the [PLACEHOLDER] sections")
    print("3. Add project-specific requirements and design details")
    print("4. Use these documents as input for AI-assisted implementation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
