# Origin and modifications

- Original skill name: `design-postgres-tables`.
- Original repository: https://github.com/timescale/pg-aiguide
- Immutable source: https://github.com/timescale/pg-aiguide/tree/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/design-postgres-tables
- Matched upstream revision: `5d3b76b5c986693b30753828b404aa66ba34c31a`.
- Original SKILL.md SHA-256: `05208140f1929a1935b1d9fa426200ac08e844e5d6b231bbcc00fa60753ea633`.
- Distributed public ID: `core-development-design-postgres-tables`.
- License: Apache-2.0; full upstream text is in LICENSE; attribution is in NOTICE.

SKILL.md was modified: its original topic blocks were placed into the six-section operating contract and their headings demoted outside fenced examples. Added selection, prerequisites, observable checks, output and authority gates; no example was removed. Relative resource paths and resource bytes are unchanged. Only the distribution skill ID changes; commands, public source URLs and data identifiers retain their original names. No local sibling-path remapping was necessary.

Added explicit qualification gates for version-dependent SQL and source ambiguities; retained examples must be checked against the actual server before execution. No database behavior was verified by this textual redistribution.

Correctness modification to SKILL.md: replaced the inherited partitioned-table FK prohibition with PG11+ referencing / PG12+ referenced-table support and a preference for supported declarative FKs. Replaced the blanket partial-index prohibition for ON CONFLICT with unique-index inference and predicate requirements; distinguished DO UPDATE unique arbiters from DO NOTHING exclusion-constraint support. Sources: [PostgreSQL 11 release notes](https://www.postgresql.org/docs/11/release-11.html), [PostgreSQL 12 release notes](https://www.postgresql.org/docs/12/release-12.html), and [PostgreSQL 18 INSERT](https://www.postgresql.org/docs/18/sql-insert.html). All other instruction content and packaged resources, including LICENSE and NOTICE, remain unchanged by this correction. Verification is static documentation review, not SQL execution.
