---
name: business-product-project-planner
description: Create or update an evidence-backed software project planning package that connects requirements, design decisions, and implementation tasks. Use when the user asks to plan a new project, turn an idea or existing system into actionable specifications, reconcile planning documents, or break approved scope into traceable work. Do not use for a single isolated requirement, architecture-only work, sprint tracking, or implementation when a narrower skill fits.
---

# Project Planning Package

Produce the smallest coherent planning package that makes downstream decisions
and implementation safer. Do not generate three large documents merely because
the templates exist.

## Establish the Planning Contract

Before writing:

1. Read applicable project instructions, existing plans, source documentation,
   and current system evidence. Preserve authoritative terminology and IDs.
2. Identify the decision this planning work must enable, its audience, requested
   artifacts, output location, and whether files may be created or updated.
3. Separate confirmed facts, user decisions, assumptions, constraints, and open
   questions. Never turn an unknown into an invented architecture or metric.
4. Define scope boundaries and success outcomes. Distinguish the first usable
   increment from later possibilities.
5. Select only the needed artifacts:
   - requirements when behavior and acceptance are unclear;
   - design when cross-cutting decisions or interfaces need consistency;
   - implementation plan when approved scope must become executable work.

For a complete package, adapt the templates in `assets/`. Do not overwrite
existing files before reading them and confirming the destination.

## Build Requirements

Give each requirement a stable `REQ-*` identifier and include:

- actor or affected stakeholder;
- desired outcome and business or operational reason;
- observable acceptance scenarios covering success, failure, and a boundary;
- priority or release slice when known;
- source, owner, and unresolved decisions when relevant.

Keep requirements solution-neutral unless a constraint or prior decision fixes
the implementation. Add performance, security, privacy, availability, scale, or
compliance targets only when supported by evidence or explicitly marked as
`TBD` with an owner and resolution step.

Do not require user-story wording when another form communicates the behavior
more precisely.

## Build the Design

Start from invariants and consequential decisions, not a catalog of fashionable
components. For each decision record the context, chosen option, rejected
alternative, tradeoff, and affected requirements.

Cover only relevant surfaces:

- system boundary and external actors;
- responsibilities and ownership;
- primary and failure flows;
- interfaces, data contracts, and compatibility;
- state, consistency, lifecycle, and migration;
- security and authority boundaries;
- observability, operations, recovery, and cost constraints;
- validation strategy and unresolved risks.

Reference `REQ-*` identifiers from decisions, flows, and interfaces. Label
conceptual components as proposals until supported by existing source or an
approved decision.

For domain-specific discovery, read
[references/domain-discovery.md](references/domain-discovery.md) and select only
questions relevant to the project. Never copy a domain checklist wholesale.

## Build the Implementation Plan

Organize work as verifiable vertical slices where practical. Give every task a
stable `TASK-*` identifier and include:

- outcome and explicitly excluded work;
- requirement and design references;
- dependencies and enabling decisions;
- expected artifacts or changed surfaces;
- validation evidence and completion condition;
- risks or approvals that can stop execution.

Keep the dependency graph acyclic. Separate discovery, migration, rollout, and
verification when they have different evidence or authority. Avoid hour or date
estimates unless the user requests them and inputs justify them.

Do not mark generated tasks complete. A planning document describes intended
work; it is not runtime or implementation evidence.

## Reconcile the Package

Before completion:

1. Trace every in-scope requirement to at least one design decision or explicit
   reason that no design decision is needed.
2. Trace every in-scope requirement to implementation and validation work.
3. Confirm every task references existing requirements and dependencies.
4. Check that boundaries, terminology, actors, states, and interfaces agree
   across artifacts.
5. Identify orphan requirements, speculative components, circular dependencies,
   unsupported metrics, placeholders, and hidden out-of-scope work.
6. Walk at least one success flow, one failure flow, one boundary case, and one
   operational or recovery scenario end to end.

For documents using the bundled ID conventions, run the read-only validator:

```bash
python3 scripts/validate_documents.py \
  --requirements <requirements-file> \
  --design <design-file> \
  --tasks <tasks-file>
```

Read the script before first use. Treat its result as structural evidence, not
proof that the plan is correct or complete.

## Completion

Return the artifacts created or updated, the planning decision they enable,
confirmed facts, assumptions, unresolved questions, traceability gaps, and
validation performed.

Call the package implementation-ready only when no blocking decision is hidden,
critical requirements have executable acceptance evidence, dependencies are
feasible, and the user-requested readiness checks pass.
