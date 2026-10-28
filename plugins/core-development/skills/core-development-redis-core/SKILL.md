---
name: core-development-redis-core
description: Core Redis modeling guidance — choose the right data structure (String, Hash, List, Set, Sorted Set, JSON, Stream, Vector Set) and use consistent colon-separated key names. Use when designing a Redis data model, caching objects, deciding between Hash and JSON, building counters, leaderboards, membership sets, or session stores, or when reviewing/cleaning up Redis key naming.
metadata:
  author: Redis, Inc.
  version: 0.1.0
---

# Redis Core

Modified distribution: headings, public ID and operating contract adapted; see [ORIGIN.md](ORIGIN.md).

## Purpose and selection

Model Redis data structures and key names for objects, sessions, counters, queues, leaderboards, membership, streams and similarity. Use for modeling and naming decisions, not server installation, cluster operations or an implicit production-key migration.


Foundational guidance for modeling data in Redis. Covers data-type selection and key-name conventions — the two decisions that most directly drive memory, performance, and maintainability.

### When to apply

- Caching objects, sessions, or per-user state.
- Counters, leaderboards, recent-items lists, unique-membership sets.
- Reviewing or refactoring Redis key names.
- Deciding between a Redis Hash and a JSON document for an entity.

## Working mode

Identify access patterns, update granularity, TTL/lifecycle, tenancy and memory requirements. Confirm Redis version/features and client library (redis-py or Jedis for the examples); JSON, Vector Set and field expiration availability must be checked rather than assumed. If these inputs are absent, state assumptions and give a conditional design.

## Focus

### 1. Choose the right data structure

Pick the type that matches the *access pattern*, not just the shape of the data.

| Use case | Recommended type | Why |
|---|---|---|
| Simple values, counters | String | Atomic `INCR`/`DECR`, `SET`/`GET` |
| Object with independently updated fields | Hash | Per-field reads/writes, no whole-object rewrite |
| Queue, recent-N items | List | O(1) push/pop at ends |
| Unique items, membership checks | Set | O(1) `SADD`/`SISMEMBER`/`SCARD` |
| Rankings, score-based ranges | Sorted Set | Score-ordered; `ZADD`/`ZRANGE`/`ZRANK` |
| Nested / hierarchical data | JSON | Path-level updates, nested arrays, RQE indexing |
| Event log, fan-out messaging | Stream | Persistent, consumer groups |
| Vector similarity | Vector Set | Native vector storage with HNSW |

**Common anti-pattern:** stuffing a flat object into a serialized string. Updating one field means fetch + parse + mutate + rewrite. Use a Hash instead.

See [references/choose-data-structure.md](references/choose-data-structure.md) for full rationale and Python/Java examples.

### 2. Use consistent key names

Use `colon-separated` segments with a stable hierarchy:

```
{entity}:{id}:{attribute}
user:1001:profile
user:1001:settings
order:2024:items
session:abc123
article:987:likes
game:space-invaders:leaderboard
```

Rules of thumb:

- **Lowercase, colon-separated.** No spaces, no mixed casing (`User_1001_Profile` is bad).
- **Keep keys short but readable** — keys live in memory and appear in every command.
- **Don't use full URLs or long strings as keys.** Extract a short identifier, or use a hash digest of the URL.
- **Prefix for multi-tenancy** (`tenant:42:user:7:cart`) so scans and ACLs can target a tenant cleanly.
- **Be consistent.** Pick one convention per service and apply it across all keys.

See [references/key-naming.md](references/key-naming.md) for cleanup examples and edge cases.

### References

- [Redis: Choosing the right data type](https://redis.io/docs/latest/develop/data-types/compare-data-types/)
- [Redis: Keys](https://redis.io/docs/latest/develop/use/keyspace/)

## Quality checks

Check that the chosen type supports required atomic updates and reads, key hierarchy remains consistent and tenant-scoped, and optional Redis features exist on the target. The Python/Java snippets illustrate client calls, not a provisioned connection or an executed benchmark.

## Return

Return the recommended type and key hierarchy with rationale, relevant example or focused code change, version/client assumptions and checks performed.

## Boundaries

Do not rename/delete production keys, overwrite cached state, scan tenants or change server/ACL configuration without explicit authorization. Use credential references provided by the host; never embed credentials or infer connectivity from these examples.
