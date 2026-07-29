# Data, Cost, Observability, and Delivery

Use for data platforms, storage, analytics, ML infrastructure, cost and sustainability, observability, or architecture implementation handoff.

## Contents

- [Data architecture](#data-architecture)
- [Storage and lifecycle](#storage-and-lifecycle)
- [Cost and sustainability](#cost-and-sustainability)
- [Observability and operations](#observability-and-operations)
- [Delivery and evidence](#delivery-and-evidence)

## Data architecture

Start with data products, owners, consumers, contracts, classification, sovereignty, lineage, quality, retention, deletion, latency, consistency, volume, and failure behavior.

For lakes, warehouses, ETL/ELT, streaming, and real-time analytics, define:

- source of truth, schema ownership and compatibility;
- ingestion identity, ordering, duplicates, late data, replay, backfill, and poison disposition;
- raw, curated, serving, and archive zones with access and lifecycle;
- catalog, lineage, quality checks, reconciliation, privacy, and deletion propagation;
- batch and streaming correctness, checkpoints, state, capacity, and recovery;
- query isolation, concurrency, caching, cost attribution, and consumer objectives.

ML and AI infrastructure also needs training and serving data provenance, feature consistency, model and artifact identity, evaluation, privacy, drift, rollback, capacity, accelerator supply, and human accountability. Do not select managed AI services merely because they appear in a provider catalog.

## Storage and lifecycle

Choose object, block, file, database, cache, archive, or distributed storage from access, consistency, durability, latency, throughput, concurrency, topology, retention, recovery, and cost needs.

Lifecycle and tiering policies require access-distribution evidence, transition and retrieval fees, minimum duration, restore latency, legal hold, replication, deletion, and application compatibility. Backup success is not restore proof. Exercise application-consistent restore with keys, identity, dependencies, schemas, and business validation.

Database selection belongs jointly to application and data owners. Evaluate transactions, consistency, query shape, indexes, scale, operations, portability, replication, backup, migration, and failure rather than choosing from workload labels alone.

## Cost and sustainability

FinOps is collaborative: engineering, finance, product, procurement, and leaders connect usage and cost to business value. Establish owner, unit economics, allocation quality, forecast horizon, currency, discounts, commitments, shared costs, support, licenses, data transfer, operations, and migration or exit costs.

Distinguish:

- current observed usage and billed cost;
- modelled baseline with dated prices and assumptions;
- potential saving before implementation;
- purchased commitment and utilization risk;
- realized comparable outcome with workload and quality controls.

Right-sizing, autoscaling, reserved capacity, savings plans, spot/preemptible compute, storage tiering, license changes, and idle cleanup all carry performance, availability, lock-in, commitment, or deletion risk. Interruptible compute also needs scheduler behavior, checkpoint or restart semantics, work duplication, interruption notice handling, capacity alternatives, and bounded retry. Automated cost actions need protected exceptions, exact authority, observation, and recovery.

Sustainability decisions use measured work accomplished per resource and consider location, energy/carbon data quality, hardware lifecycle, data movement, utilization, reliability, and business constraints. Never invent precise environmental benefits from service labels.

## Observability and operations

Design signals from business journeys and architectural decisions: user outcomes, SLI/SLO risk, dependencies, saturation, control-plane changes, security, cost, capacity, and recovery. Metrics, logs, traces, audit records, events, and synthetic journeys are complementary.

Bound telemetry schemas, cardinality, sensitive data, aggregation, sampling, retention, access, and cost. Pages should be actionable and tied to user-impact risk; infrastructure utilization is often diagnostic rather than a universal paging condition.

Runbooks identify signal, context, safe queries, authority, containment, escalation, recovery, and evidence capture. Incident work separates observation from hypothesis, preserves time-bounded evidence, uses reversible containment, verifies user recovery, and reconciles declared source.

## Delivery and evidence

Architecture implementation proceeds through owned repositories and delivery systems. Preserve immutable source and artifact identity, dependency and provider provenance, IaC state and locks, generated configuration, approval, environment boundaries, concurrency, and recovery.

Before any plan, test, or tool execution, inspect repository-controlled plugins, hooks, child processes, network, credential, state, and cost effects. Plans can become stale and may omit runtime or external behavior; review immediately before authorized apply and observe the actual workload afterward.

Handoffs are direction-specific:

- DevOps and platform owners receive source, artifact, state, bootstrap, deployment, observability, and recovery contracts.
- SRE owners receive journeys, objectives, failure modes, capacity, signals, runbooks, and exercise evidence.
- Security owners receive threat model, identities, data classes, controls, exceptions, evidence, and residual risk.
- Network owners receive flows, addressing, routes, DNS, certificates, connectivity, failure, and change sequence.
- Kubernetes and Terraform owners receive provider/version, ownership, state, target, compatibility, policy, and validation boundaries.
- Database owners receive data contracts, consistency, topology, backup, restore, migration, and performance assumptions.

Do not borrow recipient approval. Report proposed, source-validated, planned, applied, observed, recovered, estimated, and realized states separately.
