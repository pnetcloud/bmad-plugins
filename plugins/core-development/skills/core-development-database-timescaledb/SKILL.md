---
name: core-development-database-timescaledb
description: TimescaleDB best practices for hypertables, retention, and performance. Use when working with time-series data.
---

# TimescaleDB Standards

## Purpose and selection

Apply to TimescaleDB time-series schema, hypertables, rollups, compression, and retention; not to non-time-series PostgreSQL work that needs no extension-specific decision.

## Working mode

Inspect the installed TimescaleDB/PostgreSQL versions, existing chunks, ingest pattern, query windows, and retention contract. Ask for missing workload or data-lifetime requirements.

- Choose chunk interval from measured ingest rate, typical query windows, and
  the data-plus-index memory footprint of concurrently active chunks, including
  late writes. Validate chunk count and query plans under representative load;
  treat 1 day as an example, not a default. Interval changes affect only future
  chunks, so inspect existing chunks separately.

## Focus

- Use hypertables for time-series data.

- Create continuous aggregates for rollups.
- Use compression for older chunks to save space.

- Account for TimescaleDB's default time indexes; add composite or
  foreign-key-side indexes when representative plans or documented workload
  and integrity behavior justify them, then validate with representative data
  when available. Include every partitioning column in unique constraints, and
  do not design hypertable-to-hypertable foreign keys.

## Quality checks

Check the affected plans, chunk behavior, aggregate results, and policy effects under representative data; report version, workload, observed evidence, and unrun checks.

- Monitor chunk sizes and adjust retention policies.

## Return

Return the requested schema/policy proposal, patch, or review with chunk/index rationale, evidence, and unresolved data-lifetime tradeoffs.

## Boundaries

A recommendation does not authorize dropping chunks, changing retention, scheduling policies, or modifying production hypertables. Stop for explicit authority before irreversible data loss.
