# Kafka Delivery and Idempotency

Use this reference for `segmentio/kafka-go` consumer-group processing through
either `Reader` or the lower-level `ConsumerGroup` generation API. Confirm the
installed version before relying on exact options or methods.

## Contents

- Delivery boundary
- Offset rules
- Failure matrix
- Idempotency
- Poison messages and retry
- Rebalance and shutdown

## Delivery Boundary

With a consumer group, `FetchMessage` reads without committing. Explicit
acknowledgement uses `CommitMessages`. If commit batching is configured, verify
whether the call is synchronous or only schedules a later commit; do not infer
durability from the method name alone.

Keep the boundary visible:

```text
message fetched
  -> validated and transformed
  -> required durable state committed
  -> safe offset frontier advanced
  -> frontier committed to Kafka
```

Kafka and PostgreSQL normally do not share a transaction. Therefore database
success followed by process failure or Kafka commit failure produces
redelivery. Design the durable write to tolerate it and make the failed commit
observable.

## Offset Rules

Kafka stores one committed offset per topic-partition. `CommitMessages` commits
the highest supplied offset for each partition and therefore also acknowledges
all earlier offsets in that partition.

Consequences:

- Track progress separately per topic-partition.
- Commit only the highest contiguous successfully processed offset.
- Do not commit a later message while an earlier message from that partition is
  failed, pending, or being retried.
- If processing a partition concurrently, use an ordered completion tracker or
  keep acknowledgement serial even when transformation is parallel.
- Preserve partition identity when grouping a multi-partition batch.
- Treat partition reassignment as a generation boundary. `Reader` with
  `GroupID` handles generations internally and does not expose assignment or
  revocation callbacks, so do not claim application-controlled revoke draining
  in that mode. Keep processing and acknowledgement bounded, and treat commit
  errors as possible reassignment or redelivery.
- When the contract requires explicit generation-scoped cancellation or
  per-partition draining, use the version-matched `ConsumerGroup` generation
  API (or another client API that exposes ownership). Run partition work under
  the generation context, stop it when that context ends, and commit only the
  safe frontier through that generation's offset mechanism.

Do not describe a whole fetched batch as committed unless every partition's
safe frontier was acknowledged successfully.

## Failure Matrix

| Failure point | Expected outcome | Required evidence |
| --- | --- | --- |
| Before durable write | No acknowledgement; retry or quarantine by policy | unchanged durable state and offset |
| During transaction | Rollback; no acknowledgement | transaction error and unchanged offset |
| After database commit, before Kafka commit | Redelivery is possible | idempotent replay produces one logical result |
| Kafka commit returns an error | Report failure; do not claim acknowledgement | commit error metric and redelivery-safe state |
| After Kafka commit | Message must not require an uncommitted database effect | durable query and committed offset |
| Decode or validation failure | Retry, skip, or quarantine only by declared policy | reason code and offset decision |

A retry loop must be bounded and cancellation-aware. Classify transient broker
or database errors separately from permanent schema or validation failures.

## Idempotency

Choose an idempotency key from stable source identity and business semantics.
Examples include a producer-assigned event identifier or a composite of source,
partition-independent entity identity, and version. Do not use arrival time,
random values, or mutable payload formatting.

Enforce the key with a database unique constraint or an equivalent durable
mechanism. Decide whether duplicate handling should:

- return the already stored result;
- compare and reject conflicting content;
- update a versioned record under an explicit ordering rule; or
- record a duplicate audit event.

`ON CONFLICT DO NOTHING` is valid only when ignoring that exact conflict is the
declared behavior. It must not hide unrelated constraint failures or payload
disagreement.

An in-memory set, process-local cache, or Temporal Workflow ID is not the final
idempotency boundary: each can be lost, evicted, scoped differently, or reused
under a different lifecycle.

## Poison Messages and Retry

Define:

- retryable error classes and backoff;
- maximum attempts or elapsed time;
- whether a failed record blocks its partition;
- quarantine or dead-letter destination and authorization;
- safe diagnostic fields and retention;
- replay ownership and how replay avoids a second side effect.

Skipping a poison message advances an offset and is a data-loss decision unless
the contract explicitly defines quarantine as the durable outcome. Do not make
that decision inside a generic catch block.

## Rebalance and Shutdown

Use contexts to cancel blocking fetch and commit calls. Stop intake before
closing dependencies, drain or cancel in-flight work according to the delivery
contract, commit only safe frontiers, then close the reader.

`Reader.Close` closes the stream and enables a graceful consumer-group
disconnect. It does not promise to commit arbitrary fetched or processed
messages. Make all required commits explicit and check their errors before
closing.

Give shutdown a deadline. On expiry, prefer redelivery of unacknowledged work to
advancing offsets past uncertain durable state.

## Primary Reference

- [`kafka-go` package documentation](https://pkg.go.dev/github.com/segmentio/kafka-go)
