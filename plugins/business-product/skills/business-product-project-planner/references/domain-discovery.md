# Domain Discovery Questions

Read only the sections relevant to the project. Use these as prompts for
evidence gathering, not as requirements or architecture defaults.

## Contents

- Transactional and financial work
- Event-driven and real-time work
- Data and machine-learning work
- Multi-tenant services
- Device and edge systems
- Regulated or safety-sensitive work
- Developer platforms and integrations

## Transactional and Financial Work

- What is the system of record, and which invariants must never be violated?
- Where are authorization, limits, reconciliation, and audit decisions made?
- Which operations require idempotency, ordering, or atomicity?
- What are the states and recovery paths for partial or disputed operations?
- Which latency, availability, retention, or reporting targets are evidenced?

Do not infer an exchange, ledger model, settlement flow, or compliance regime
from the domain label.

## Event-Driven and Real-Time Work

- Which events are facts, requests, notifications, or derived observations?
- What ordering, deduplication, replay, and delivery guarantees are required?
- Where does state live, and how is it rebuilt after failure?
- Which backpressure, lag, and overload behaviors are acceptable?
- What end-to-end latency matters to the user, and where is it measured?

Do not select a broker, partitioning scheme, or consistency model before these
requirements are known.

## Data and Machine-Learning Work

- What are the source contracts, ownership, quality rules, and allowed uses?
- How are schemas, datasets, features, models, and decisions versioned?
- Which offline and online metrics determine acceptance?
- How are leakage, bias, drift, privacy, and human review handled?
- What is the rollback or fallback when data or model quality degrades?

Separate deterministic data processing from probabilistic model behavior and
trace validation for both.

## Multi-Tenant Services

- What constitutes a tenant and where must isolation hold?
- Which identities can cross tenant boundaries, and for what purpose?
- Which configuration, quotas, billing, and lifecycle rules vary per tenant?
- What noisy-neighbor, residency, deletion, and export requirements apply?
- How will operators diagnose problems without leaking another tenant's data?

Do not assume one database, one schema, or one deployment per tenant.

## Device and Edge Systems

- What are device identities, trust roots, ownership states, and provisioning
  flows?
- How do intermittent connectivity, clock drift, duplication, and offline work
  affect correctness?
- What can execute at the edge, and what requires centralized authority?
- How are configuration and software updates staged, verified, and rolled back?
- What physical safety or irreversible effects require human control?

## Regulated or Safety-Sensitive Work

- Which jurisdiction, standard, policy, or accountable role actually applies?
- What evidence, approvals, segregation of duties, and retention are required?
- Which hazards or failure modes can cause material harm?
- What operations require a safe state, manual override, or two-person control?
- How are decisions reproduced and audited without exposing protected data?

Record applicable authority; never manufacture compliance requirements from a
generic template.

## Developer Platforms and Integrations

- Who owns each interface, and what compatibility promise exists?
- How are consumers discovered, migrated, rate-limited, and supported?
- Which extension points execute untrusted code or receive privileged access?
- How are artifacts, dependencies, provenance, and release promotion verified?
- What failure isolation and observability does each integration boundary need?

Prefer contracts and consumer evidence over a predetermined toolchain.
