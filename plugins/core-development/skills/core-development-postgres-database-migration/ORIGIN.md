# Origin and modifications

- Original skill name: `postgres-database-migration`.
- Original repository: https://github.com/timescale/pg-aiguide
- Immutable source: https://github.com/timescale/pg-aiguide/tree/5d3b76b5c986693b30753828b404aa66ba34c31a/skills/postgres-database-migration
- Matched upstream revision: `5d3b76b5c986693b30753828b404aa66ba34c31a`.
- Original SKILL.md SHA-256: `927448a05a6d4de518ed159f3627f75a1057d80c6be5cc02850a7680aa811c1a`.
- Distributed public ID: `core-development-postgres-database-migration`.
- License: Apache-2.0; full upstream text is in LICENSE; attribution is in NOTICE.

SKILL.md was modified: its original topic blocks were placed into the six-section operating contract and their headings demoted outside fenced examples. Added selection, prerequisites, observable checks, output and authority gates; no example was removed. Relative resource paths and resource bytes are unchanged. Only the distribution skill ID changes; commands, public source URLs and data identifiers retain their original names. No local sibling-path remapping was necessary.

Full original description exceeds official 1024-character limit; preserved verbatim as selection detail in Purpose and selection; concise trigger description stays in frontmatter.

Added explicit qualification gates for version-dependent SQL and source ambiguities; retained examples must be checked against the actual server before execution. No database behavior was verified by this textual redistribution.

Correctness modification to SKILL.md: replaced the invalid PG18 SET NOT NULL NOT VALID / VALIDATE NOT NULL recipe with ADD CONSTRAINT orders_status_nn NOT NULL order_status NOT VALID followed by VALIDATE CONSTRAINT orders_status_nn. Marked version branches as alternatives and qualified checks, transactions and lock expectations; retained the PG12–17 CHECK/VALIDATE/SET NOT NULL branch unchanged. Source: [PostgreSQL 18 ALTER TABLE](https://www.postgresql.org/docs/18/sql-altertable.html). All other instruction content and packaged resources, including LICENSE and NOTICE, remain unchanged by this correction. Verification is static documentation/grammar review, not SQL execution.
