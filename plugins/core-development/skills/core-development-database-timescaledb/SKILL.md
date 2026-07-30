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
- Always index the time column and foreign keys.
