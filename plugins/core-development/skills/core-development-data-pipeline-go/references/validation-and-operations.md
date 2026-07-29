# Validation and Operations

Use this reference to define ingest validation, observability, replay, and
acceptance evidence.

## Validate at Trust Boundaries

Validate before transformation and again before persistence where types or
invariants change. Cover:

- message and decompressed size;
- supported schema version and encoding;
- required identifiers and partitioning key;
- timestamp range and clock assumptions;
- collection lengths and nesting depth;
- numeric precision and narrowing conversions;
- referential and cross-field invariants;
- tenant or authorization scope when applicable.

Do not silently drop invalid input. Select one declared outcome:

- retry because the dependency or schema registry is temporarily unavailable;
- quarantine a durable safe representation for authorized review;
- reject and acknowledge only when loss is explicitly allowed by the contract;
- stop the partition or pipeline when ordering or compliance requires it.

Quarantine is an external write. Define access control, encryption, retention,
replay ownership, and duplication behavior before enabling it.

## Observability Model

Prefer bounded labels and identifiers. Useful signals include:

- consumer lag and safe offset frontier by topic-partition;
- fetched, validated, persisted, duplicated, retried, quarantined, and
  acknowledged counts;
- batch rows, bytes, fill time, and database duration;
- commit latency and commit failures;
- transaction rollback and constraint-error classes;
- Activity queue wait, attempt duration, retry, timeout, heartbeat age, and
  cancellation;
- Workflow history growth, Continue-As-New count, and last durable progress;
- end-to-end freshness from source timestamp to queryable state.

Do not put payload content, raw headers, credentials, personal data, full error
objects, or unbounded identifiers into metrics. Logs should identify a record
through a safe locator and correlation value, not reproduce the record.

## Failure-Injection Matrix

Exercise at least:

| Injection | Expected invariant |
| --- | --- |
| process stops before database commit | offset does not advance |
| process stops after database commit | replay creates one logical result |
| Kafka commit fails | error is visible and replay remains safe |
| database connection drops mid-batch | transaction and offset outcome are known |
| one partition completes out of order | commit does not cross the gap |
| consumer group rebalances | revoked work is not acknowledged unsafely |
| Activity times out after heartbeat | retry resumes or replays safely |
| cancellation arrives during I/O | ownership and durable state remain consistent |
| invalid record repeats | retry or quarantine policy remains bounded |
| Continue-As-New occurs with pending input | pending Signals or Updates follow policy |
| worker restarts with an old Workflow history | replay remains deterministic |

Test both a duplicate with identical content and a key collision with different
content. They are not the same condition.

## Acceptance Evidence

Record:

- exact fixture topology and library versions;
- produced message identifiers and partitions using synthetic data;
- database rows or queryable results after processing;
- committed offsets after the durable result;
- results after crash, restart, rebalance, and duplicate replay;
- Workflow run transition and replay-test output;
- quarantine result for one invalid fixture;
- telemetry that distinguishes every injected failure.

Compilation, mocked method calls, a low consumer lag, or a successful
Continue-As-New alone cannot prove end-to-end delivery.

## Operational Stop Conditions

Stop rollout or replay when:

- offsets advance without matching durable state;
- duplicates create additional logical effects;
- a commit gap is crossed;
- retry or quarantine grows without a bound;
- Workflow replay becomes non-deterministic;
- protected data appears in logs, metrics, history, or artifacts;
- the observed topology differs from the reviewed contract.

Preserve evidence before cleanup. Cleanup must target only disposable fixtures
or explicitly authorized test resources.
