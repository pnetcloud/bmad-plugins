# Project-Type Planning Patterns

Use this reference when project shape changes the questions, document emphasis,
or delivery slices. These are investigation prompts, not prescribed
architectures, technologies, phases, or quality targets.

## Contents

- Shared selection rules
- Web applications
- Service APIs
- Command-line tools and libraries
- Service-decomposed systems
- Data pipelines
- Generic or uncertain projects
- Shared delivery families

## Shared Selection Rules

Choose a pattern from evidence about actors, interfaces, ownership, state,
deployment, and failure isolation. A product label alone is insufficient.

Before applying a pattern, establish:

- who or what initiates the primary workflow;
- which observable result defines success;
- where trust, ownership, and lifecycle boundaries exist;
- whether state is owned, delegated, derived, or absent;
- which interfaces are public, internal, interactive, batch, or event-driven;
- which failure modes change the requirements or delivery order;
- which deployment and operational decisions remain unresolved.

Combine patterns when the scope genuinely contains multiple shapes. Do not force
one document set per technology layer; keep one traceable planning contract for
the approved scope.

## Web Applications

Requirements may need to examine:

- primary user journeys and denied, empty, loading, and recovery states;
- accessibility, device, locale, session, and navigation expectations;
- identity and authorization only when the workflow requires them;
- client/server validation ownership and observable error behavior;
- freshness, offline, concurrency, and history behavior;
- browser support and measurable user-experience objectives.

Design questions include:

- whether rendering and state transitions occur locally, remotely, or both;
- interface contracts and compatibility between interaction and capability
  boundaries;
- ownership of validation, authorization, caching, and sensitive state;
- navigation, deep-link, refresh, and failure recovery;
- observability without exposing user or credential data.

Delivery slices should demonstrate complete user-observable behavior. A slice
may include interface, application logic, state, and tests when the accepted
design requires them; it need not mirror a frontend/backend/database stack.

## Service APIs

Requirements may need to examine:

- consumers, use cases, version and compatibility expectations;
- authentication, authorization, quotas, pagination, and limits;
- input, output, error, idempotency, ordering, and retry semantics;
- synchronous, asynchronous, streaming, or callback behavior;
- latency and availability objectives only when approved and measurable.

Design questions include:

- protocol and schema ownership;
- lifecycle, deprecation, negotiation, and migration;
- trust boundaries and credential handling;
- failure classification, backpressure, partial completion, and recovery;
- observability, auditability, and sensitive-field treatment.

Delivery slices should connect an accepted requirement to a versioned contract,
implementation behavior, compatibility evidence, and operational verification.
Generate an OpenAPI or other machine-readable description only when the
interface and project standards require one.

## Command-Line Tools and Libraries

Requirements may need to examine:

- commands or callable surfaces, inputs, outputs, and exit or error behavior;
- configuration sources, precedence, defaults, and invalid configuration;
- interactive versus non-interactive use;
- stdout, stderr, structured output, logging, and machine consumption;
- portability, installation, upgrade, and compatibility.

Design questions include:

- parsing or call boundary versus application logic;
- filesystem, process, network, and credential authority;
- deterministic behavior and reproducibility;
- cancellation, interruption, partial writes, and cleanup;
- plugin or extension contracts only when they are an accepted requirement.

Delivery slices should produce a usable command or callable behavior with help,
errors, tests, and packaging evidence. Publication or external distribution is
a separate authorized action, not an automatic final task.

## Service-Decomposed Systems

Use this pattern only after ownership, scaling, deployment, isolation, or
organizational evidence justifies multiple independently operated components.
Do not infer decomposition from the word "platform" or from a template.

Requirements may need to examine:

- independently owned capabilities and data;
- cross-boundary consistency, ordering, and failure behavior;
- compatibility and coordinated or independent change;
- isolation, capacity, and operational ownership;
- audit and recovery across partial completion.

Design questions include:

- why each boundary exists and what it must not own;
- communication and state contracts;
- discovery, routing, retries, deduplication, and backpressure when applicable;
- end-to-end observability and incident ownership;
- migration from or to another boundary model.

Delivery should prefer end-to-end capability slices and contract evidence over
creating empty component scaffolds. Shared libraries, brokers, orchestration,
or gateways are decisions, not mandatory infrastructure.

## Data Pipelines

Requirements may need to examine:

- source authority, format, volume, cadence, and schema evolution;
- transformations, quality rules, lineage, and reproducibility;
- event time, processing time, ordering, duplication, and late data;
- retention, replay, correction, deletion, and privacy;
- delivery objective and consumer-visible completeness.

Design questions include:

- stage boundaries and ownership;
- batch, streaming, or hybrid execution;
- checkpoints, idempotency, replay, and recovery;
- schema and contract evolution;
- observability for freshness, quality, backlog, and failed records.

Delivery slices should prove a representative source-to-consumer path with
quality and recovery evidence. Connectors, storage, schedulers, queues, and
catalogs are included only when the accepted design calls for them.

## Generic or Uncertain Projects

When project shape is unclear, do not select a detailed template prematurely.
Start with:

1. the primary actor and outcome;
2. the input, observable result, and failure boundary;
3. the minimum capability boundary;
4. external authority and state ownership;
5. verification evidence;
6. open decisions that would select another pattern.

Keep components and phases abstract until evidence supports specialization.

## Shared Delivery Families

These families remain useful prompts when supported by the design:

- project and development environment;
- data or state model and migration;
- core decision or transformation logic;
- public or internal interface;
- user interaction;
- external integration;
- security and privacy controls;
- testing and acceptance evidence;
- observability and operational readiness;
- deployment, rollout, rollback, and cleanup;
- documentation, compatibility, and decommissioning.

Order work by dependency and risk. Prefer reviewable vertical slices; use a
family as a standalone phase only when it produces an independently verifiable
outcome.
