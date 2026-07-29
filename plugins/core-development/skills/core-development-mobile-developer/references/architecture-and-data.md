# Architecture, State, and Offline Data

Use this reference to choose boundaries and data semantics for React Native,
Flutter, or another repository-selected mobile stack.

## Contents

- Preserve the existing stack
- Place shared and native behavior
- Choose state and architecture patterns
- Design native boundaries
- Define offline and synchronization semantics
- Review networking, caching, and persistence

## Preserve the Existing Stack

Start from repository evidence:

- framework and plugin/package versions in manifests and lockfiles;
- native iOS and Android projects, deployment targets, build tools, and enabled
  architectures;
- current navigation, state, persistence, dependency injection, code
  generation, and native-module conventions;
- public API and data contracts;
- migration history and supported upgrade path.

Do not select React Native, Flutter, Kotlin Multiplatform, Compose
Multiplatform, or fully native development from trend or preference alone.
Compare them only when the task authorizes a platform or framework decision.
Account for existing skills, native feature depth, accessibility, platform
release cadence, dependency health, build/release ownership, and migration
cost.

Treat framework version labels such as "latest" as time-sensitive. Use the
version declared by the repository and consult that version's official
documentation. Do not copy APIs from a newer release into an older project.

## Place Shared and Native Behavior

Share behavior when it has the same invariant and failure semantics on every
supported platform:

- domain models and validation;
- serialization and API contracts;
- deterministic business rules;
- synchronization protocol and conflict decisions;
- feature-policy evaluation;
- portable tests for shared rules.

Keep behavior platform-specific when the operating system owns its semantics:

- permissions, entitlements, and capabilities;
- application and scene/activity lifecycle;
- background execution;
- navigation conventions and system surfaces;
- authentication prompts and protected storage;
- deep-link and notification delivery;
- accessibility semantics, input, haptics, and system settings;
- camera, media, location, sensors, Bluetooth, health, automotive, and
  wearable integrations.

Optimize for one coherent contract, not a code-sharing percentage. Duplicating
a small native adapter can be safer than a generic abstraction that obscures
different lifecycles or failures.

Use a typed capability boundary:

```text
Capability:
  availability: supported | unavailable | permission-required | degraded
  operation: typed request -> typed result
  failures: denied | unavailable | interrupted | invalid-input | platform-error
  lifecycle: start, suspend, restore, cancel, dispose
```

Ensure a missing capability has an intentional fallback or an explicitly
unsupported state.

## Choose State and Architecture Patterns

Follow the repository's established separation first. Consider these as
options, not a mandatory stack:

- layered or Clean Architecture when independent policy and infrastructure
  boundaries already justify it;
- repository abstractions when multiple data sources or test substitutes need a
  stable consumer contract;
- MVVM or MVI when the UI framework and existing state flow support them;
- unidirectional data flow for predictable state transitions;
- dependency injection when dependencies require lifecycle control or
  substitution;
- immutable models when they reduce shared-state ambiguity;
- reactive streams or hooks for actual asynchronous state, with explicit
  cancellation;
- code generation when the generated contract is checked in or reproducible,
  reviewable, and version-pinned.

Do not add layers merely to match a diagram. State the problem each boundary
solves and the ownership it establishes.

For React Native, follow the project's TypeScript/JavaScript, navigation, and
state conventions. Redux Toolkit, Zustand, another store, Context, or local
component state can each be appropriate at different scopes.

For Flutter, follow the project's Dart architecture and state convention.
Provider, Riverpod, BLoC, another state mechanism, or framework primitives are
choices governed by current code and lifecycle needs.

Keep API clients, validation, and errors consistent across screens. Do not
collapse transport errors, authorization failures, offline state, cancellation,
and validation failures into one generic message.

## Design Native Boundaries

Use the framework-supported native boundary for the repository version:

- React Native native modules/components and code generation where applicable;
- Flutter platform channels for message-oriented platform APIs;
- Dart FFI for suitable C-compatible libraries when ownership, memory safety,
  threading, and packaging are understood;
- Pigeon or another repository-approved typed generator when it materially
  reduces schema drift.

Before adding a boundary:

1. Define supported platforms and availability.
2. Define serialization, threading, reentrancy, and callback ordering.
3. Define ownership of native resources and listener cleanup.
4. Propagate cancellation and lifecycle transitions.
5. Map native failures to stable typed failures without leaking sensitive
   details.
6. Test both sides and the unsupported path.
7. Measure the boundary only if it is a demonstrated bottleneck.

Do not select TurboModules, FFI, or another lower-level mechanism solely as a
performance label. Confirm compatibility with the repository's active
architecture and build pipeline.

## Define Offline and Synchronization Semantics

Do not equate a local cache with offline support. Define:

- **Source of truth:** local, remote, or hybrid for each entity and field.
- **Read policy:** cached, stale-while-refresh, remote-required, or unavailable.
- **Durable operations:** which user intents survive process death and how they
  are serialized.
- **Identity:** stable operation and entity identifiers used for idempotency and
  deduplication.
- **Ordering:** whether operations commute, require causal order, or require a
  server sequence.
- **Conflict policy:** field merge, domain-specific merge, server authority,
  explicit user resolution, last-write-wins with defined clocks, or a
  version/vector strategy.
- **Delta synchronization:** change token, cursor, version range, deletion
  representation, and full-resync fallback.
- **Retry policy:** retryable failures, cap, backoff with jitter, connectivity
  wake-up, cancellation, and dead-letter/user recovery.
- **Deletion:** tombstones, retention, resurrection prevention, and
  cross-device behavior.
- **Schema migration:** compatibility across installed app versions and queued
  operations.
- **Observability:** queue depth, age, conflict count, failure class, and
  user-visible state without sensitive payloads.

SQLite, Realm, WatermelonDB, framework storage, or another local store are
implementation choices. Select by transaction needs, query model, migrations,
encryption/support characteristics, binary size, native maintenance, and
existing project use.

Test at least:

- create/update/delete offline, then reconnect;
- duplicate and reordered delivery;
- concurrent edits from multiple clients;
- process termination between enqueue and acknowledgement;
- authentication expiry and account change;
- partial page/cache state and schema upgrade;
- permanently invalid operations and user recovery.

## Review Networking, Caching, and Persistence

- Use explicit timeouts, cancellation, idempotency, and retry classification.
- Batch only when it improves the measured workload without delaying important
  interactions or increasing failure scope.
- Use supported transport capabilities negotiated by the platform and server;
  do not require a protocol version without end-to-end evidence.
- Compress payloads when content and measured cost justify it. Avoid
  recompressing already compressed media.
- Define cache key, freshness, invalidation, capacity, eviction, and ownership.
  TTL and LRU are mechanisms, not complete consistency policies.
- Paginate with stable ordering and duplicate/missing-item behavior across
  refreshes.
- Protect sensitive stored data according to its threat model and retention
  need. Minimize persistence before choosing encryption.
- Treat logs, backups, snapshots, notifications, clipboard, screenshots, and
  analytics as possible data-exposure surfaces.
