---
name: core-development-messaging-kafka
description: Kafka messaging standards for topic design, reliability, and observability.
---

# Kafka Standards

- Design topics carefully: `domain.entity.event`.
- Always specify partitions and replication factor.
- Use a schema registry (Avro/JSON/Protobuf) for compatibility.
- Enable idempotent producers and safe configs for exactly-once.
- Consumer groups must commit offsets explicitly.
- Monitor lag and rebalance events.
