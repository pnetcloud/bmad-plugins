---
name: core-development-database-postgresql
description: PostgreSQL standards for schema design, migrations, and performance. Use when working with SQL/PostgreSQL.
---

# PostgreSQL Standards

- Use `snake_case` for table and column names.
- Always define primary keys.
- Use foreign keys for integrity; avoid orphan rows.
- Prefer UUIDs for identifiers in distributed systems.
- Write explicit migrations; avoid destructive changes without backups.
- Monitor slow queries and add indexes based on query plans.
