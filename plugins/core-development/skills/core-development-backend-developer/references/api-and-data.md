# API and Data Decisions

Read this reference only when the task changes an API or persistent-data
contract. Repository conventions and the task's compatibility requirements
take precedence over generic preferences.

## Contents

- HTTP and RPC contracts
- Relational data
- Migrations and data evolution
- Non-relational stores and caches
- Backup and recovery

## HTTP and RPC Contracts

- Model resources and operations around domain behavior rather than mirroring
  tables. Use the protocol's actual method, status, metadata, cancellation, and
  streaming semantics.
- Distinguish safe, idempotent, and non-idempotent operations. Do not
  automatically retry a write merely because its transport method is commonly
  idempotent; verify the complete side effect and any downstream calls.
- Validate path, query, header, body, metadata, and decoded values at the trust
  boundary. Reject ambiguous duplicates, unsupported media types, oversized
  inputs, invalid encodings, and unknown fields when the contract requires it.
- Define one stable error contract. Keep client errors actionable while
  excluding stack traces, queries, credentials, internal hosts, and dependency
  details.
- Choose pagination from data and consistency needs:
  - offset pagination is simple but can drift under concurrent writes and may
    become expensive at high offsets;
  - cursor or keyset pagination needs a deterministic total order, tie-breaker,
    direction, scope, expiry/version strategy, and opaque validated cursor;
  - document whether totals are exact, approximate, unavailable, or bounded.
- Configure CORS only for browser callers and only for required origins,
  methods, headers, and credential behavior. CORS is not authorization.
- Apply rate limiting or resource limits by the protected resource and abuse model, not
  only by network address. Define scope, burst, sustained rate, response,
  retry guidance, distributed consistency, and fail-open/fail-closed behavior.
- Version only when compatibility requires it. Prefer compatible additive
  evolution; document deprecation, observability, migration, and removal
  criteria for a breaking change.
- Keep an API description such as OpenAPI aligned with implemented behavior
  when the repository uses one. Validate examples, authentication, errors,
  pagination, limits, callbacks/webhooks, and compatibility in CI where
  supported. Do not upgrade the specification version incidentally.

For GraphQL, also bound query depth or cost, pagination, batching, error
visibility, field-level authorization, and subscription lifecycle. For gRPC,
preserve generated contracts, deadlines, cancellation, status details,
streaming flow control, half-close behavior, metadata trust, and transport
identity.

## Relational Data

- Start from invariants, access patterns, cardinality, write rate, retention,
  isolation, and consistency. Normalize or denormalize deliberately; neither is
  a universal target.
- Make constraints enforce durable invariants when the datastore supports
  them. Treat application validation as complementary, not a concurrency-safe
  replacement.
- Use parameterized queries or safe query builders. Dynamic identifiers and
  sort expressions require an explicit allowlist rather than value
  parameterization.
- Add an index only after inspecting representative query plans and data
  distribution. Account for write amplification, storage, lock/build behavior,
  selectivity, ordering, partial predicates, covering columns, and redundant
  indexes. Re-measure after the change.
- Size connection pools against total process/replica concurrency, database
  capacity, transaction duration, and proxy behavior. Bound acquisition time
  and expose saturation without logging connection strings.
- Define transaction isolation from anomalies the workflow must prevent.
  Keep external calls outside a database transaction unless a deliberate
  protocol proves otherwise.
- Define rollback behavior for each transaction path, including errors raised
  after partial in-memory work and cleanup that can itself fail.
- Handle uncertain commit outcomes: do not blindly retry a transaction if the
  client cannot know whether commit succeeded. Use a stable operation identity,
  reconciliation, or domain-specific recovery.
- For replicas, specify which reads may be stale, how read-after-write is
  preserved, what happens during lag/failover, and whether routing is
  transaction-aware.

## Migrations and Data Evolution

Use expand/migrate/contract when mixed application versions or large data make
an atomic breaking change unsafe:

1. Add backward-compatible schema and code.
2. Backfill in bounded, resumable, observable batches.
3. Switch reads/writes with compatibility evidence.
4. Remove legacy behavior only after usage and rollback-window evidence.

Before execution, inspect lock behavior, table size, defaults, constraints,
index build mode, replication, timeout, backup/restore, and interruption
semantics. Test clean installation and upgrade from every supported version.
Prefer a forward-fix when a down migration would destroy or misinterpret data.

Do not conflate “migration file generated,” “migration test passed,”
“migration applied,” and “production data verified.”

## Non-Relational Stores and Caches

- Choose a store from consistency, query, update, retention, partition, and
  failure requirements rather than popularity.
- Define keys, partitioning, hot-key behavior, conditional writes, conflict
  resolution, TTL, compaction, and schema evolution.
- Treat a cache as derived state unless the design explicitly makes it
  authoritative. Define source of truth, key namespace, tenant and
  authorization scope, negative caching, invalidation, stampede controls,
  serialization version, size limits, and behavior when unavailable.
- Never place a shared cache ahead of object-level authorization in a way that
  can return one caller's data to another.

## Backup and Recovery

When recovery is in scope, verify rather than merely configure:

- recovery point and recovery time objectives;
- what stores, schemas, keys, and encryption material are included;
- retention, immutability, access control, and regional/tenant boundaries;
- restore procedure, integrity checks, application compatibility, and test
  cadence.

A successful backup job is not evidence that a usable restore exists.
