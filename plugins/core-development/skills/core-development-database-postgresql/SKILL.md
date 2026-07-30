---
name: core-development-database-postgresql
description: PostgreSQL standards for schema design, migrations, and performance. Use when working with SQL/PostgreSQL.
---

# PostgreSQL Standards

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
  existing key type requires a staged compatibility migration for referencing
  data and clients.
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
- Monitor slow queries and add indexes based on query plans.
