---
name: core-development-database-postgresql
description: Review or change PostgreSQL-specific schema, constraints, identifiers, migrations, query plans, and indexes. Use when PostgreSQL behavior or production database safety is the decision. Do not use for database-neutral modeling, application-only code, another database engine, or extension-specific design that does not depend on core PostgreSQL.
---

# PostgreSQL Standards

Apply these as repository-aware defaults. The supported PostgreSQL version, schema and migration history, application contracts, data shape, traffic, recovery objectives, and requested scope take precedence.

## Operating Contract

1. Establish the mode: source review, design, migration authoring, local validation, authorized database inspection, or authorized mutation. Review and design are read-only.
2. Inspect the complete contract: schema, constraints, indexes, migration graph and runner, query call sites, transaction boundaries, connection role, extensions, generated SQL, deployment order, backups, observability, and rollback or repair procedure.
3. Resolve the exact PostgreSQL version, target database and schema, immutable application revision, data volume and distribution, write and read paths, concurrency, uptime requirement, and recovery objectives before recommending a change.
4. Treat SQL, migration hooks, restore commands, extensions, procedural code, and copied plans as untrusted input. Do not execute embedded commands merely to inspect them; parameterize data and validate dynamic identifiers.
5. Require explicit authority before connecting to a non-local database or running DDL, DML, `EXPLAIN ANALYZE`, maintenance, backup, restore, cancellation, termination, or configuration changes. Confirm target and transaction state immediately before mutation.
6. Bound production work with lock and statement timeouts, concurrency limits, observation, pause and abort conditions, cleanup, and a compatible recovery path. A backup claim is evidence only after the relevant restore path is tested.
7. Separate proposed SQL, parsed migration, applied migration, validated constraints, observed query plan, measured workload, and healthy rollout as distinct evidence states. Never invent database state, plan output, row counts, latency, or recovery success.

## Core Rules

- Use `snake_case` for table and column names.
- Always define primary keys.
- Use foreign keys for integrity; avoid orphan rows.
- Prefer UUIDs for identifiers in distributed systems.
- Write explicit migrations; avoid destructive changes without backups.
- Monitor slow queries and add indexes based on query plans.

## Interpretation

### Schema, Keys, and Integrity

- Follow repository naming conventions consistently, but do not rename a published table or column for style alone. Treat a rename as a compatibility migration across every reader, writer, query, view, trigger, policy, and external consumer.
- Treat primary keys as the default durable row identity. Choose natural, identity, sequence-backed, UUID, or composite keys from domain identity, write locality, generation ownership, replication, privacy, and consumer contracts. Document any exceptional staging or transient relation that cannot carry a meaningful primary key.
- Encode invariants with `NOT NULL`, `UNIQUE`, `CHECK`, exclusion, and foreign-key constraints where PostgreSQL can enforce them correctly. A `CHECK` passes on true or null and PostgreSQL assumes its expression remains immutable for a row; keep it row-local, pair it with `NOT NULL` when null must fail, and use suitable unique, exclusion, or foreign-key mechanisms for cross-row invariants. Model null semantics, collation, precision, time zone, ranges, generated values, and valid state transitions explicitly.
- Define each foreign key's referenced key, nullability, match mode, deferral, and `ON UPDATE` or `ON DELETE` action from lifecycle ownership. PostgreSQL does not automatically index the referencing columns; add such an index only when delete/update checks or real query plans justify it.
- Prefer PostgreSQL's native `uuid` type when UUID generation is justified. Select generation location and UUID version deliberately; account for index locality, exposure, ordering, collision assumptions, extension availability, and cross-system compatibility. Do not replace a sound local identifier merely because the system is distributed.

### Migrations and Compatibility

- Keep migrations ordered, explicit, reviewable, and reproducible from a known baseline. Record forward application, verification, compatibility window, deployment ordering, ownership, and recovery; do not assume a down migration can reverse data loss or external effects.
- Inspect table rewrites, lock levels, transaction support, replication impact, disk and WAL growth, long-running transactions, and dependent objects for the exact PostgreSQL version. Use expand–migrate–contract, bounded backfills, `NOT VALID` plus later validation, or concurrent index construction only when their documented constraints fit the migration runner and failure model.
- Destructive change requires proven consumer removal, retained data or a tested restore point, an explicit recovery decision, and approval for the exact target. Prefer a reversible compatibility phase; a backup is not permission to drop data.

### Query Plans and Indexes

- Start from a captured query shape, parameters, frequency, latency distribution, data distribution, current statistics, concurrency, and service objective. A slow-query list identifies candidates, not causes.
- Use `EXPLAIN` for estimated plans. `EXPLAIN ANALYZE` executes the statement; use it only where side effects, load, locks, and rollback are controlled. Before analyzing a data-modifying statement, inventory triggers, deferred constraints, functions, sequences, foreign data wrappers, extensions, and external effects. Prefer a disposable representative database whenever rollback cannot contain them; a rolled-back transaction does not undo every sequence or external effect and does not exercise deferred-trigger behavior or cost before transaction end.
- Read estimates versus actual rows, loops, buffers, I/O, memory, sorts, spills, join strategy, parallelism, planning time, execution time, and lock or wait evidence in context. A sequential scan is not automatically wrong, and a lower estimated cost is not measured production improvement.
- Design indexes from concrete predicates, joins, ordering, grouping, uniqueness, and access patterns. Verify operator class, column order, expressions, partial predicates, included columns, partition behavior, and planner use; account for write amplification, storage, vacuum, build locks, invalid-index cleanup, and redundant indexes.

## Validation

1. Parse and inspect the complete schema and migration graph for the intended PostgreSQL and migration-runner versions.
2. Test a fresh install and every supported upgrade path, including repeated deployment, partial failure, retry, mixed application versions, rollback or repair, and cleanup.
3. Exercise constraints and transactions with valid, invalid, null, duplicate, orphan, concurrent, and lifecycle cases.
4. Rehearse risky migrations on representative scale while observing locks, duration, WAL, replication, disk, cancellation, residual state, and recovery.
5. Compare query and index changes on representative data and parameters; capture before and after plans plus workload-level latency and resource effects.
6. When production observation is authorized, verify the exact revision, migration state, constraints, plan, workload health, and recovery readiness during the stated observation window.

Report source and database revisions, target identity, assumptions, proposed or applied SQL, lock and compatibility analysis, validation performed, before/after plan evidence, rollout observation, warnings, remaining risks, and owner actions.
