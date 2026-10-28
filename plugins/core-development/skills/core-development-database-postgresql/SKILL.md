---
name: core-development-database-postgresql
description: PostgreSQL standards for schema design, migrations, and performance. Use when working with SQL/PostgreSQL.
---

# PostgreSQL Standards

## Purpose and selection

Apply these standards to PostgreSQL schema, SQL, migration, and query-performance work; not to a different database engine without checking its contract.

## Working mode

Inspect the deployed PostgreSQL version, schema, data volume, workload, and migration tooling. Ask for missing downtime, compatibility, or recovery constraints before selecting a migration path.

- Write explicit, version-aware migrations. Before applying one, assess its
  lock level and wait, table or index rewrite, scan, disk/WAL, replication, and
  transaction-block behavior against current data and traffic. When retained
  data value, live traffic, downtime budget, scale, independently deployed
  consumers, or recovery risk warrants it, use a staged expand, bounded
  resumable backfill, validation, cutover, and contract sequence with old/new
  application compatibility, monitoring, stop conditions, and forward or
  rollback recovery. Otherwise document why a simpler transactional or
  scheduled-offline migration is safe, including measured lock/runtime limits
  and authorized recovery.
  Use version-supported online index or constraint techniques where warranted
  and handle failed/invalid artifacts explicitly. A backup must have a tested
  restore path, but is not by itself a safe migration plan.

## Focus

- Use `snake_case` for table and column names.
- Always define primary keys.
- Use foreign keys for integrity; avoid orphan rows.
- Choose identifier types from generation scope, merge/offline needs, exposure,
  index locality, storage, and client contracts. Preserve suitable natural or
  composite keys and established identifier contracts. For a new surrogate
  key, prefer identity or sequence allocation when database-local generation is
  sufficient; use UUIDs when independent generators need collision-resistant
  IDs. If time-ordered UUIDs are useful, require a PostgreSQL version or
  application generator that supports the selected UUID version and document
  the tradeoff. Benchmark the actual index and write workload when locality,
  throughput, or cost is a decision driver or identified risk. Changing an
  existing key type requires staged compatibility when live references,
  independently deployed clients, availability, or recovery risk warrants it;
  otherwise use the measured simpler-migration path in Working mode.

## Quality checks

Record the affected schema or migration revision, query plans, migration checks, and observed lock/runtime evidence; mark checks not run.

- Monitor slow queries and add indexes based on query plans.

## Return

Return the requested SQL, migration proposal, patch, or review with rationale, validation evidence, and unresolved compatibility or recovery risks.

## Boundaries

Preparing SQL does not authorize applying it. Obtain task authority for data/schema changes, destructive operations, downtime, and recovery actions; stop when safe execution cannot be established.
