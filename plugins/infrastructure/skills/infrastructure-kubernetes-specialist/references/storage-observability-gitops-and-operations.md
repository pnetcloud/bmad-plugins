# Storage, Observability, GitOps, and Operations

Use this reference for persistent data, telemetry, GitOps, troubleshooting, cost, recovery, or operational handoff.

## Contents

- [Storage and data lifecycle](#storage-and-data-lifecycle)
- [Backup, restore, and migration](#backup-restore-and-migration)
- [Observability and troubleshooting](#observability-and-troubleshooting)
- [GitOps and configuration delivery](#gitops-and-configuration-delivery)
- [Cost and capacity](#cost-and-capacity)
- [Operational receipt](#operational-receipt)

## Storage and data lifecycle

Resolve the CSI driver and version, StorageClass parameters and binding mode, topology, access modes, reclaim policy, expansion, snapshots, encryption, identity, quotas, performance limits, and provider lifecycle. Distinguish namespaced PersistentVolumeClaims from cluster-scoped PersistentVolumes and external storage assets.

For each workload, establish:

- application consistency, writer, flush, fencing, quorum, and shutdown behavior;
- volume attachment and topology constraints;
- expected capacity, latency, throughput, IOPS, burst, and failure behavior;
- retention, deletion protection, reclaim, orphan, and cleanup semantics;
- encryption key ownership and rotation;
- monitoring, alert, backup, restore, migration, and recovery ownership.

Dynamic provisioning simplifies allocation; it does not prove tenant isolation, backup, performance, or safe deletion. Snapshot capability depends on the driver and storage system. A VolumeSnapshot is not automatically an application-consistent backup or a tested restore.

Storage tuning starts with a representative baseline across application, filesystem, node, CSI, network, and backend evidence. Change one bottleneck at a time and remeasure using the same method.

## Backup, restore, and migration

1. Define protected objects and data, consistency point, retention, immutability, encryption, region or failure-domain placement, access, and recovery objectives.
2. Bind backup artifacts to source volumes, application version, schemas, keys, cluster objects, and external dependencies.
3. Verify completion and integrity without exposing data or credentials.
4. Restore into an authorized isolated target; validate application startup, data semantics, identities, networking, dependencies, and user-visible behavior.
5. Reconcile restored objects with GitOps and active controllers while preventing overwrite, duplicate writers, and external side effects.
6. Measure recovery and data loss against objectives and record untested dependencies and residual risk.

For migration, define source of truth, writer quiescence or replication, cutover, compatibility, validation queries, lag, client routing, abort conditions, fallback limits, and post-cutover cleanup. Deleting old volumes or snapshots is a separate destructive action requiring explicit authority.

## Observability and troubleshooting

Collect the smallest evidence needed to discriminate hypotheses:

- API and controller conditions, events, generation and observed generation;
- Pod phase, container state, prior termination, readiness, restarts, scheduling, and placement;
- logs with exact time window, container, instance, and correlation identifiers;
- workload and dependency metrics, traces, user journeys, resource pressure, and saturation;
- node, DNS, network, storage, admission, identity, and external-service evidence;
- change events, image and configuration identity, and GitOps reconciliation.

Metrics, logs, traces, events, and audit records are complementary. Bound label cardinality, payload collection, tenant data, privacy, retention, and access. Never copy Secret values, tokens, full environment dumps, or unrelated tenant logs into a report.

Troubleshoot from current state:

1. state impact and affected scope;
2. preserve time-bounded evidence before disruptive action;
3. separate observations from hypotheses;
4. test the cheapest discriminating hypothesis;
5. choose reversible containment within authority;
6. observe workload and user-facing recovery;
7. reconcile declared source and runtime;
8. report residual risk and follow-up ownership.

For Pod failures, network issues, storage problems, bottlenecks, security violations, resource constraints, upgrades, and application errors, resist symptom-only changes such as increasing limits, restarting, widening policy, or disabling probes without causal evidence.

## GitOps and configuration delivery

Call a workflow GitOps only when desired state is:

- declarative;
- versioned with immutable history;
- pulled by software agents;
- continuously observed and reconciled.

Argo CD, Flux, or another controller requires exact source revision, artifact identity, target selection, controller identity, project or tenant boundary, diff and health semantics, ordering, concurrency, approval, audit, failure, recovery, and upgrade ownership. A repository plus push-based deployment is ordinary CI/CD, not automatically GitOps.

For Helm:

- inspect charts, dependencies, plugins, hooks, lookups, value precedence, generated names, CRDs, ownership, and release history;
- render deterministically with the intended chart and dependency identity;
- keep secret values outside committed value files and command output;
- treat rollback as conditional on application, schema, storage, hook, and API compatibility.

For Kustomize, inspect bases, components, remote resources, plugins, generators, transformers, patch targeting, name changes, and overlay composition. Review the complete rendered output and preserve an immutable mapping from source to deployed artifact.

Promotion should move a reviewed identity across environments while keeping environment-owned configuration explicit. Multi-cluster sync needs target inventory, tenancy, waves, capacity, version compatibility, pause, abort, and recovery. Secret management requires source-of-truth, encryption, access, rotation, revocation, propagation, and unavailable-provider behavior; encrypted text in Git is not by itself safe end-to-end handling.

Manual emergency changes require exact authority, evidence preservation, reversible containment, source reconciliation, and protection against unsafe controller overwrite. Emergency language does not authorize disabling reconciliation fleet-wide.

## Cost and capacity

Attribute cost with dated resource, usage, storage, network, license, and shared-platform evidence. Separate:

- observed bill or usage;
- estimated change and assumptions;
- realized comparable result;
- attribution limits and service-level tradeoffs.

Right-size from representative demand and failure headroom. Spot or interruptible nodes require workload tolerance, capacity alternatives, eviction behavior, topology, and recovery. Idle-resource cleanup, storage deletion, and autoscaler changes can be destructive or availability-affecting and require ownership and recovery.

Do not optimize for a universal utilization percentage. Capacity planning includes growth, bursts, rescheduling, upgrades, zone loss, DaemonSet overhead, system reservations, quotas, provider limits, and dependency ceilings. Monitoring overhead is part of the measured workload, not an excuse to remove decision-critical signals blindly.

## Operational receipt

Report:

- **Target:** repository revision, rendered artifact identity, cluster/context, namespace, objects, and identity used.
- **Mode and authority:** review, design, local execution, live read, or mutation; approvals and bounds.
- **Changed:** source and live objects, field manager, controller, and observed side effects.
- **Validation:** exact commands, versions, policy revisions, dry-run kind, isolated tests, and live observation window.
- **Runtime:** controller reconciliation, Pod and dependency state, user-facing signals, or `not observed`.
- **Data and recovery:** protected assets, backup/restore evidence, rollback or forward-repair limits.
- **Security:** identity, admission, policy, image, Secret handling, exceptions, and residual risks.
- **Cost:** estimate versus observed result and assumptions.
- **Remaining:** unresolved drift, deprecation, risk, owner, and next action.

Never claim completion from generated YAML, a successful command, accepted API request, healthy Pod condition, passing scanner, successful backup, or proposed saving alone. State exactly what each piece of evidence proves.
