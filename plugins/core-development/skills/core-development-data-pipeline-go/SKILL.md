---
name: core-development-data-pipeline-go
description: Design, implement, review, or troubleshoot Go data pipelines that combine Kafka consumption, PostgreSQL persistence through pgx, and Temporal orchestration. Use for delivery semantics, batching, idempotency, retries, workflow history, validation, observability, or graceful shutdown. Do not use for a different language or messaging stack, general schema design, one-off data migration, or deployment operations without an explicit pipeline contract.
---

# Reliable Go Data Pipelines

Build a pipeline whose failure behavior is explicit and testable. Do not claim
exactly-once processing merely because the database write is idempotent or an
offset is committed manually.

## Establish the Contract

Before changing code:

1. Read repository instructions, Go modules and lock data, client
   configuration, schemas, migrations, workflow registrations, retry policies,
   tests, and operational runbooks that govern the target path.
2. Record the installed Kafka client, pgx, and Temporal SDK versions. Check
   version-matched API documentation before changing configuration or lifecycle
   behavior.
3. Draw the path from message production through partition assignment, decode,
   validation, persistence, offset acknowledgement, and downstream visibility.
4. Define the required delivery model, ordering key, idempotency key, batch
   limits, latency objective, replay window, and poison-message policy.
5. Identify which process owns the Kafka reader, database transaction, Temporal
   Workflow, Activity, and shutdown sequence.
6. State authorized scope. A code change does not authorize creating topics,
   applying migrations, changing retention, resetting offsets, terminating
   Workflows, deploying workers, or touching production data.

If the system cannot atomically commit database state and Kafka offsets, model
the gap instead of promising atomicity.

## Preserve the Failure Invariants

The default at-least-once shape is:

```text
fetch -> validate -> transform -> durable write -> commit contiguous offsets
```

The durable write must be idempotent because a crash or commit failure after
database success causes redelivery. Never commit an offset before every earlier
message in that topic-partition has reached its required durable state.

Read
[references/delivery-and-idempotency.md](references/delivery-and-idempotency.md)
before changing consumer groups, manual commits, parallel processing, retry,
rebalance, poison-message, or shutdown behavior.

Treat each error distinctly. A bounded fetch timeout with a non-empty batch can
be a normal flush condition; cancellation, rebalance, broker failure, decode
failure, database failure, and offset-commit failure are not interchangeable.
Do not swallow a commit error or report the batch fully acknowledged.

## Choose the Persistence Boundary

Validate and normalize before persistence while retaining enough source identity
to diagnose and replay failures. Use stable database constraints as the final
idempotency authority; an in-memory deduplication cache is only an optimization.

Read [references/postgres-batching.md](references/postgres-batching.md) before
using `pgx.Batch`, `CopyFrom`, staging tables, conflict handling, or a
multi-statement transaction.

Choose a technique from measured batch size, row width, constraint behavior,
atomicity needs, and error isolation. Always consume and check all batch results,
including the final close error. A broad `ON CONFLICT DO NOTHING` can hide the
wrong constraint violation; name the intended conflict target when the schema
supports it.

## Keep Temporal Semantics Explicit

Workflow code must remain deterministic. Put Kafka, PostgreSQL, network, file,
clock, and other external I/O in Activities. Configure Activity timeouts and
retries from the operation's failure contract, not from a generic preset.

Read
[references/temporal-orchestration.md](references/temporal-orchestration.md)
before changing Workflow loops, Activity retries, heartbeats, cancellation,
Continue-As-New, worker shutdown, or Workflow code that may have open histories.

Use heartbeats for meaningful progress and cancellation delivery in
long-running Activities. Use Continue-As-New based on history and state size,
not a copied iteration constant. Carry only durable continuation state and
account for pending Signals or Updates. Protect Workflow evolution with replay
tests and the versioning mechanism appropriate to the installed SDK.

A Workflow ID policy coordinates executions; it does not replace message or
database idempotency.

## Validate Data and Bound Resources

Treat message keys, headers, payloads, timestamps, and metadata as untrusted.
Bound message size, decoded collection sizes, batch count, batch bytes, fetch
wait, database time, concurrency per partition, retry duration, and retained
diagnostic data.

Reject or quarantine invalid records through an explicit policy. Do not log full
payloads, credentials, personal data, authorization material, or unrestricted
headers. Preserve a safe record locator, reason code, schema version, and
correlation information sufficient for authorized diagnosis.

Read
[references/validation-and-operations.md](references/validation-and-operations.md)
when defining validation, telemetry, replay, incident evidence, or acceptance
tests.

## Verify the Pipeline

Use the consuming repository's focused commands and test in widening layers:

1. unit-test decoding, validation, idempotency-key construction, and error
   classification;
2. integration-test database constraints, transaction rollback, batch-result
   handling, and duplicate delivery;
3. test multiple partitions and an out-of-order worker completion without
   committing past a gap;
4. inject failure before the write, after the write but before commit, during
   commit, during rebalance, and during shutdown;
5. replay representative Workflow histories after Workflow-code changes;
6. verify Activity timeout, retry, heartbeat, cancellation, and
   Continue-As-New behavior;
7. run an end-to-end fixture from produced message to durable queryable state
   and acknowledged offset;
8. verify telemetry and quarantine behavior without exposing protected data.

Use disposable infrastructure or an explicitly authorized environment. Do not
reset real offsets or delete durable records to make a test pass.

## Complete

Report:

- versions, topology, delivery and ordering contract, and authority boundary;
- idempotency key and database constraint;
- batch limits, transaction boundary, retry and poison-message policy;
- Workflow and Activity lifecycle decisions;
- exact tests and failure injections with results;
- offset, database, Workflow, and downstream evidence;
- remaining duplicate, loss, ordering, privacy, or operability risks.

Call the pipeline verified only when restart and failure-injection evidence
matches the stated delivery contract. Successful compilation or a happy-path
batch is not sufficient.
