---
name: core-development-database-timescaledb
description: TimescaleDB best practices for hypertables, retention, and performance. Use when working with time-series data.
---

# TimescaleDB Standards

- Use hypertables for time-series data.
- Set chunk interval based on data rate (for example, 1 day).
- Create continuous aggregates for rollups.
- Use compression for older chunks to save space.
- Monitor chunk sizes and adjust retention policies.
- Always index the time column and foreign keys.
