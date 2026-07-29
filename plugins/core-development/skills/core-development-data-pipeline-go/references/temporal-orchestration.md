# Temporal Orchestration for Pipelines

Use this reference for the Temporal Go SDK. Inspect the installed SDK and server
compatibility before selecting APIs or versioning behavior.

## Contents

- Workflow and Activity boundary
- Timeouts, retries, and heartbeats
- Continue-As-New
- Cancellation and shutdown
- Workflow evolution and replay

## Workflow and Activity Boundary

Workflow code must be deterministic under history replay. Use Temporal Workflow
APIs for time, timers, concurrency, channels, and controlled side effects. Do
not perform Kafka, PostgreSQL, network, filesystem, environment, or native
goroutine work directly in Workflow code.

Activities own external I/O. Keep their inputs and results bounded and
serializable. Avoid returning complete message batches or payloads through
Workflow history when a durable locator or compact summary is sufficient.

Separate orchestration idempotency from business idempotency:

- Workflow ID and reuse policies coordinate executions.
- Activity retries can repeat an external call.
- The database or destination still needs a durable idempotency key.

## Timeouts, Retries, and Heartbeats

Define timeouts from the operation:

- Schedule-to-Start bounds queue wait when that distinction matters.
- Start-to-Close bounds one Activity attempt.
- Schedule-to-Close bounds the complete retry window.
- Heartbeat timeout detects missing progress for a heartbeating Activity.

Classify non-retryable validation or contract errors explicitly. Bound retry
attempts or elapsed time when indefinite retry would block a partition,
retention window, or operational objective.

Heartbeat long-running Activities at meaningful checkpoints. Include only
compact, non-sensitive progress needed to resume safely. Heartbeats also deliver
cancellation to the Activity; they are not a substitute for a correct
Start-to-Close timeout.

On retry, read heartbeat details only when the checkpoint is durable and
compatible with the current input. Re-validate any external state before
resuming.

## Continue-As-New

Continue-As-New starts a new run with fresh history. Use it when current SDK
history guidance, event count, state size, or a deliberate processing boundary
justifies rotation. Do not copy a universal loop count.

Before continuing:

1. complete or cancel owned child work according to policy;
2. preserve durable progress and compact continuation state;
3. drain buffered Signal channels into durable or bounded continuation state
   according to the message contract;
4. wait for in-progress Update handlers with the installed SDK's
   `AllHandlersFinished` mechanism unless an explicit unfinished-handler policy
   permits abandonment;
5. return the Continue-As-New error from the main Workflow path, not from a
   Signal or Update handler;
6. carry identifiers and schema versions needed by the next run;
7. avoid carrying secrets, full payloads, or unbounded collections.

Test Signals arriving immediately before and during rollover, accepted Updates
whose handlers are still running, and a new run that restores the carried
state. Draining is not permission to accumulate an unbounded message list.

Use the version-matched SDK recommendation or server suggestion API when
available, plus a conservative project-specific guard.

## Cancellation and Shutdown

Propagate cancellation intentionally. Decide whether an Activity should abandon
work, finish a transaction, or complete a compensating durable step. Do not
detach work merely to make shutdown quick.

Worker shutdown and Activity cancellation are related but distinct:

- stop polling for new tasks;
- allow the configured graceful-stop interval for in-flight work;
- keep heartbeating progress when appropriate;
- close Kafka and database resources owned by the worker after work has stopped;
- let unacknowledged work retry rather than fabricating success.

No cleanup callback should commit an offset whose durable state is uncertain.

## Workflow Evolution and Replay

Changing Workflow control flow can make open histories non-deterministic.
Before deployment:

1. collect representative histories without protected payloads;
2. replay them against the new worker code;
3. use the SDK's supported versioning or worker-deployment mechanism for
   incompatible transitions;
4. test old and new continuation-state schemas;
5. document rollback compatibility.

Activity implementation changes still require contract compatibility even
though Activity code itself is not replayed.

## Primary References

- [Temporal Go SDK](https://pkg.go.dev/go.temporal.io/sdk)
- [Temporal Continue-As-New](https://docs.temporal.io/develop/go/continue-as-new)
- [Temporal Activity heartbeats](https://docs.temporal.io/encyclopedia/detecting-activity-failures#heartbeat-timeout)
