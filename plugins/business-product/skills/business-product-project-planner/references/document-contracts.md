# Planning Document Contracts

Use this reference for the document surfaces needed by the selected planning
mode. It preserves the package's requirements, design, implementation,
traceability, and quality capabilities without loading every template into
`SKILL.md`.

## Shared Header

Every planning document should identify:

```markdown
# [Document Type]: [Scope Name]

- Status: Draft | In Review | Accepted | Superseded
- Scope owner: [Role or owner]
- Reviewers: [Roles or owners]
- Last reviewed: [Date]
- Authoritative inputs: [Links or identifiers]
- Replaces: [Prior document or none]
- Related documents: [Requirements, design, plan, decisions]
```

Keep a compact evidence ledger:

| ID | Statement | Class | Source or owner | Validation or review |
|---|---|---|---|---|
| E-1 | [Material statement] | confirmed / decision / assumption / constraint / open / derived | [Source] | [Evidence or next action] |

## Requirements Document

### Recommended Structure

```markdown
# Requirements: [Scope]

## Purpose and Outcomes
## Stakeholders and Users
## Context and Current State
## In Scope
## Out of Scope
## Constraints and Assumptions
## Glossary
## Functional Requirements
## Quality and Operational Requirements
## Data, Security, Privacy, and Compliance
## Dependencies and Integrations
## Risks and Open Questions
## Traceability
```

### Requirement Record

```markdown
### REQ-[N]: [Outcome-oriented title]

- Status: proposed / accepted / deferred / rejected
- Priority: [Project-defined scale]
- Source: [Evidence or decision owner]
- Related: [Constraint, risk, design, or prior requirement IDs]

**Outcome:** As a [stakeholder], I need [observable capability], so that
[measurable or reviewable benefit].

**Preconditions:** [Required state]

**Acceptance evidence:**

1. GIVEN [initial state], WHEN [event], THEN [observable result].
2. IF [failure or boundary], THEN [observable handling].
3. Measurement: [method, environment, sample, threshold owner].

**Unknowns:** [Unresolved information or none]
```

User-story form is optional. A system, legal, operational, migration, or
security requirement may be clearer as a direct outcome statement. Do not force
one capability into a story if it hides the actual stakeholder or constraint.

### Acceptance Criteria Patterns

Use criteria that identify state, action, and observable evidence:

```text
GIVEN [precondition], WHEN [event], THEN [result]
IF [boundary or failure], THEN [result and recovery]
FOR [data class or role], THE system MUST [behavior]
UNDER [measured environment], [metric] MUST satisfy [approved target]
```

If using `MUST`, `SHOULD`, or `MAY` normatively, declare BCP 14 interpretation.
Otherwise use ordinary language. Testability comes from observable evidence,
not from capitalization.

### Quality Requirements

For performance, reliability, scale, security, privacy, accessibility, cost, or
operability, record:

- stakeholder and business consequence;
- baseline evidence and date;
- approved target and owner;
- workload, environment, data volume, and measurement method;
- steady state, burst, degraded state, and recovery expectations;
- exclusions and confidence.

Never copy example numbers into a live requirement. A placeholder remains an
open decision until supported by evidence.

## Design Document

### Recommended Structure

```markdown
# Design: [Scope]

## Context and Goals
## Requirements and Constraints
## System Boundary
## Invariants
## Decisions and Alternatives
## Component Responsibilities
## Interfaces and Integration Points
## Data and State
## End-to-End Flows
## Failure and Recovery
## Security and Privacy
## Observability and Operations
## Deployment and Environments
## Migration, Rollout, Rollback, and Decommissioning
## Verification Strategy
## Risks, Assumptions, and Open Questions
## Traceability
```

### Component Map

| ID | Component or external actor | Responsibility | Owns | Interfaces | Does not own |
|---|---|---|---|---|---|
| COMP-1 | [Name] | [Single purpose] | [State or decisions] | [Interface IDs] | [Boundary] |

Component boundaries should follow accepted requirements and invariants. Do not
default to services, queues, gateways, or databases because a domain template
mentions them.

### Interface Contract

```markdown
### INT-[N]: [Interface name]

- Owner and consumers: [Roles/components]
- Purpose: [Outcome]
- Protocol and version: [Decision or open question]
- Authentication and authorization: [Contract]
- Request/input schema: [Reference]
- Response/output schema: [Reference]
- Errors and retryability: [Contract]
- Idempotency and ordering: [Contract]
- Limits, pagination, and backpressure: [Contract]
- Compatibility and deprecation: [Contract]
- Observability: [Signals without sensitive payloads]
```

For HTTP APIs, use the project's approved OpenAPI version when machine-readable
interoperability is required. Keep prose for intent, invariants, and behavior
that the schema cannot express.

### Flow Contract

```markdown
### FLOW-[N]: [Name]

1. [Actor] sends [data/event] to [component] under [precondition].
2. [Component] validates [rules] and records [state transition].
3. [Component] calls or emits [interface/event].
4. [Consumer] produces [observable outcome].

- Failure paths: [Timeout, rejection, duplicate, partial completion]
- Recovery: [Retry, compensation, operator action]
- Data classification and retention: [Contract]
- Evidence: [Trace, metric, log, test, or review]
```

### Decision Record

| ID | Decision | Alternatives | Rationale | Consequences | Owner/status |
|---|---|---|---|---|---|
| DEC-1 | [Choice] | [Options] | [Evidence] | [Tradeoffs] | [Owner] |

## Implementation Plan

### Recommended Structure

```markdown
# Implementation Plan: [Scope]

## Delivery Strategy
## Boundaries and Non-Goals
## Dependency Graph
## Milestones or Vertical Slices
## Tasks
## Migration and Rollout
## Verification and Acceptance
## Risks and Open Questions
## Traceability
```

### Task Record

```markdown
- [ ] TASK-[N]: [Outcome]
  - In scope: [Exact change]
  - Out of scope: [Protected boundary]
  - Requirements: [REQ IDs]
  - Design: [DEC/COMP/INT/FLOW IDs]
  - Dependencies: [Task or external IDs]
  - Implementation notes: [Only accepted design constraints]
  - Verification: [Tests, runtime evidence, document review]
  - Rollout/rollback: [If applicable]
  - Completion: [Observable criteria]
```

Prefer vertical slices that produce reviewable behavior. Infrastructure,
database, backend, frontend, integration, testing, operations, and
documentation remain valid task families when the design actually requires
them; they are not mandatory phases.

Checkboxes reflect verified state only:

- `[ ]` not started or not proven;
- `[~]` active if the project's format supports it;
- `[x]` accepted against the stated evidence.

Do not mark generated tasks complete.

## Traceability

Maintain explicit mappings rather than relying on repeated names:

| Requirement | Design coverage | Delivery tasks | Verification | Status |
|---|---|---|---|---|
| REQ-1 | DEC-1, COMP-1, INT-1 | TASK-1 | TEST-1 / review | covered / deferred / gap |

Check both directions:

- every accepted requirement has design, delivery, and verification coverage
  or an explicit deferral;
- every design component and task has a requirement, constraint, risk, or
  operational justification;
- every referenced ID exists exactly once;
- superseded IDs are not silently reused.

## Update Mode

When changing existing documents:

1. inventory current IDs, decisions, accepted behavior, and consumers;
2. record the requested change and affected surfaces;
3. preserve identifiers where semantics remain compatible;
4. mark replacements and migration paths when semantics change;
5. update forward and reverse traceability;
6. review the diff for accidental information loss;
7. revalidate the full planning set, not only the edited file.

## Validation Mode

Classify findings:

- **blocking** — contradiction, dangling reference, missing authority,
  unverifiable acceptance, unsafe assumption, or absent decision required for
  implementation;
- **warning** — incomplete detail that can be resolved during an owned task;
- **note** — improvement that does not affect readiness.

Structural tools can prove headings, IDs, references, and placeholder presence.
They cannot prove business correctness, architectural fitness, estimates, or
that a metric is attainable.

## Domain Routing

Read [domain-templates.md](domain-templates.md) only for a matching domain. Use
its lists to ask:

- which capabilities and risks apply;
- which suggested components are actually justified;
- which standards, protocols, regulations, and versions are authoritative;
- what workload and operational evidence supports quality targets;
- which domain test and deployment concerns need owners.

The domain families retained by the package include financial, real-time,
commerce, content, IoT, machine learning, developer tools, SaaS, analytics,
agent/orchestration, and enterprise integration systems, plus shared
non-functional, cross-cutting, task, testing, and deployment patterns.

## Completion Checklist

Before handoff:

- [ ] Requested documents and planning mode are clear.
- [ ] Scope, non-goals, outcomes, constraints, and owners agree.
- [ ] Material claims are classified and sourced.
- [ ] Requirements are unique, testable, and measurable where necessary.
- [ ] Design covers interfaces, data, failures, security, operations, and
      lifecycle.
- [ ] Tasks form an explainable dependency order and retain protected
      boundaries.
- [ ] Forward and reverse traceability contain no unresolved references.
- [ ] Metrics, technologies, estimates, and architectures are decisions, not
      template defaults.
- [ ] Structural validation and semantic review are both recorded.
- [ ] Sensitive and private information remains only in its authorized project
      context.
