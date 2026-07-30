---
name: core-development-messaging-kafka
description: Kafka messaging standards for topic design, reliability, and observability.
---

# Kafka Standards

- Design topics carefully: `domain.entity.event`.
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
- Monitor lag and rebalance events.
