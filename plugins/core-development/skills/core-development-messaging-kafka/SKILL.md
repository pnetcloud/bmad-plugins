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
- Consumer groups must commit offsets explicitly.
- Monitor lag and rebalance events.
