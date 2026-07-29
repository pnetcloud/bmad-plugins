# Distributed Systems and Messaging

Read this reference when backend work crosses a process boundary or introduces
asynchronous delivery. Distribution adds failure modes; it is not a default
scalability improvement.

## Contents

- Service boundaries and communication
- Message contract
- Producer and consumer behavior
- Replay and batch processing
- Scaling and resilience
- Observability across boundaries

## Service Boundaries and Communication

- Preserve the existing deployment boundary unless independent ownership,
  scaling, isolation, compliance, or release needs justify a split.
- Define the owner of each invariant and write. Avoid shared-table coupling
  disguised as independent services.
- Select synchronous calls when the caller needs an immediate result and can
  tolerate temporal coupling. Select asynchronous delivery when decoupling,
  buffering, fanout, or durable work is required and eventual outcomes are
  acceptable.
- For every remote call define deadline, cancellation, retry eligibility,
  idempotency, concurrency bound, load-shedding behavior, response-size limit,
  authentication, authorization, and telemetry.
- Add a circuit breaker only with a measured failure mode, meaningful fallback,
  bounded half-open probes, and observable state. A breaker cannot replace
  timeouts, capacity, or dependency repair.
- Use service discovery, a gateway, load balancer, or service mesh only when supplied
  by the operating environment or justified by the target architecture. Keep
  policy ownership and failure behavior explicit.

For cross-service workflows, choose deliberately among:

- a single owner and synchronous call;
- an outbox/inbox or change-capture flow for durable publication;
- orchestration when one component must track the workflow;
- choreography when event ownership and emergent coupling remain manageable;
- compensation when a completed side effect has a valid inverse;
- reconciliation when reality may diverge and no atomic transaction exists.

Do not call a sequence a saga unless steps, durable state, compensation or
forward recovery, timeouts, duplicates, and operator intervention are defined.

## Message Contract

Define:

- message or event purpose and authoritative producer;
- stable identity and correlation/causation fields;
- schema, compatibility, defaults, unknown-field behavior, and size bound;
- partition or routing key and its ordering scope;
- acknowledgement point and durability expectation;
- delivery semantics as observed by the application;
- consumer idempotency and side-effect deduplication;
- retry schedule, attempt budget, poison-message disposition, and alerting;
- retention, privacy, encryption, access, and deletion requirements;
- replay selection, version compatibility, rate control, and reconciliation.

“Exactly once” at one broker boundary does not make external effects exactly
once. Design consumers for duplicates unless an end-to-end proof says
otherwise.

## Producer and Consumer Behavior

- Publish after durable state using a transactional outbox or another proven
  protocol when losing the event would violate an invariant.
- Do not acknowledge before required effects are durable. If work has several
  effects, define which state records progress and how it resumes.
- Bound in-flight messages, workers, batches, and memory. Pause intake or apply
  backpressure when dependencies or storage cannot keep up.
- Preserve ordering only where the domain requires it; document what happens
  during retries, repartitioning, failover, and parallel consumption.
- Make handlers cancellation-aware without abandoning work after it was
  acknowledged or leaving an ambiguous side effect.
- Quarantine poison messages with enough non-sensitive diagnostics to
  investigate. A dead-letter destination needs ownership, retention, access,
  alerting, redrive rules, and a terminal disposition.
- Use priority queues only when starvation, fairness, capacity reservation,
  and retry priority have defined behavior.

## Replay and Batch Processing

Replay is a privileged write operation. Before execution:

1. Identify the exact immutable source range and target consumers.
2. Prove schema and code compatibility or provide a translator.
3. Disable or deduplicate unsafe external effects.
4. Bound rate and concurrency against downstream capacity.
5. Define checkpoints, pause, resume, abort, and reconciliation.
6. Observe lag, error classes, duplicates, and side effects.
7. Obtain explicit authority for the target environment.

For batches, define item-level versus batch-level atomicity, partial failure,
ordering, retry granularity, maximum size/time, checkpointing, and reporting.

## Scaling and Resilience

- Scale only after measuring the bottleneck. Horizontal replicas may amplify
  database connections, hot partitions, cache misses, downstream load, and
  duplicate work.
- Keep stateless request handling where practical, but name durable state and
  session ownership rather than hiding it.
- Test dependency timeout, slow response, malformed response, refusal,
  partition, stale data, overload, restart, duplicate delivery, and recovery.
- Use graceful degradation only when it remains correct and does not bypass
  authorization, return cross-tenant or dangerously stale data, or falsely
  report success.
- Define service-level indicators and objectives only from user-visible
  behavior and operational needs. Do not invent an availability target.

## Observability Across Boundaries

Use distributed tracing only where cross-process request paths need it.
Propagate a bounded correlation or trace context only across trusted fields.
Do not accept arbitrary baggage into logs, storage, or downstream headers.

Measure request and message rate, duration, error class, saturation, queue lag,
age of oldest work, retries, dead-letter volume, and reconciliation outcomes as
applicable. Keep labels bounded; raw object, user, request, or message
identifiers generally belong in access-controlled diagnostics, not metric
dimensions.
