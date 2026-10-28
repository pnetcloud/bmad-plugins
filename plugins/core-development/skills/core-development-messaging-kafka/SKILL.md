---
name: core-development-messaging-kafka
description: Kafka messaging standards for topic design, reliability, and observability.
---

# Kafka Standards

## Purpose and selection

Apply to Kafka topic, producer, consumer, or event-contract design and review. Do not use it to impose Kafka on a system that has not selected it or to claim delivery guarantees for unrelated external systems.

## Working mode

Inspect the topic configuration, schema compatibility baseline, client versions, offset strategy, and required failure semantics. Ask for missing owners or delivery requirements before selecting settings; distinguish proposed configuration from the live cluster.

## Focus

- Design topics carefully: `domain.entity.event`.

- Treat every topic as a versioned contract: document owner, event key, ordering
  scope, retention or compaction policy, schema subject, and compatibility mode
  before producers write to it. Add a new topic or version for incompatible
  semantics instead of silently changing an existing stream.

- Always specify partitions and replication factor.

- Use a schema registry (Avro/JSON/Protobuf) for compatibility.

- Use idempotent producers for retry safety. Claim Kafka exactly-once processing
  only when output records and consumed offsets commit in the same Kafka
  transaction and downstream consumers use `read_committed`. Do not extend that
  claim to external side effects; specify their separate idempotency or atomicity
  mechanism and actual delivery guarantee.

- Choose automatic, manual, or transactional offset commits from the failure
  contract. Do not advance offsets before required effects complete unless the
  contract explicitly accepts loss; test crash and rebalance replay or duplicates.

## Quality checks

Validate schemas and compatibility, then test retries, crashes, rebalances, and duplicate handling in an approved environment. Verify lag and rebalance visibility and show the transaction and consumer isolation evidence for any exactly-once claim.

- Monitor lag and rebalance events.

## Return

Return topic and schema decisions or the focused producer/consumer change, actual delivery guarantees, observed checks, and unresolved failure cases or ownership decisions.

## Boundaries

Topic creation, partition changes, retention changes, schema registration, offset resets, replay, and cluster writes require explicit target authority. Do not infer permission to mutate a broker from a design or review request.
