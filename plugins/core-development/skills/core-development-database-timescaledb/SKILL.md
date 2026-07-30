---
name: core-development-database-timescaledb
description: TimescaleDB best practices for hypertables, retention, and performance. Use when working with time-series data.
---

# TimescaleDB Standards

- Use hypertables for time-series data.
- Choose chunk interval from measured ingest rate, typical query windows, and
  the data-plus-index memory footprint of concurrently active chunks, including
  late writes. Validate chunk count and query plans under representative load;
  treat 1 day as an example, not a default. Interval changes affect only future
  chunks, so inspect existing chunks separately.
- Create continuous aggregates for rollups.
- Use compression for older chunks to save space.
- Monitor chunk sizes and adjust retention policies.
- Account for TimescaleDB's default time indexes; add composite or
  foreign-key-side indexes when representative plans or documented workload
  and integrity behavior justify them, then validate with representative data
  when available. Include every partitioning column in unique constraints, and
  do not design hypertable-to-hypertable foreign keys.
