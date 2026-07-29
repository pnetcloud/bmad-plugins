# Cluster, Workloads, Resources, and Upgrades

Use this reference for cluster topology, workload controllers, scheduling, autoscaling, disruption, or upgrades. Keep provider-specific actions subordinate to the repository and distribution documentation.

## Contents

- [Cluster and version contract](#cluster-and-version-contract)
- [Choose the controller from semantics](#choose-the-controller-from-semantics)
- [Resources, scheduling, and autoscaling](#resources-scheduling-and-autoscaling)
- [Probes, shutdown, and rollout](#probes-shutdown-and-rollout)
- [Disruption and availability](#disruption-and-availability)
- [Upgrade workflow](#upgrade-workflow)
- [Validation and evidence](#validation-and-evidence)

## Cluster and version contract

Before a cluster-level recommendation, establish:

- Kubernetes distribution and exact control-plane and node versions;
- supported version skew, lifecycle window, and provider restrictions;
- control-plane, etcd, node-pool, availability-zone, network, DNS, and storage failure domains;
- CNI, CSI, ingress or Gateway implementation, admission stack, metrics APIs, and autoscaling components;
- cluster-scoped controllers, CRDs, webhooks, field managers, and upgrade ownership;
- workload criticality, recovery objectives, capacity headroom, maintenance policy, and rollback or forward-repair limits.

Do not infer high availability from replica count, multiple nodes, or multiple zones alone. Trace control-plane, node, network, storage, identity, DNS, and external dependency failures through the required user journey.

## Choose the controller from semantics

- **Deployment:** independently replaceable replicas and declarative rollout. Check surge/unavailable capacity, image identity, readiness, termination, and dependency compatibility.
- **StatefulSet:** stable identity or ordered lifecycle. Verify headless service, persistent-volume behavior, update policy, quorum or leader semantics, and application-level backup and restore.
- **Job:** finite work with explicit success, retry, deadline, idempotence, output, and cleanup contracts. A completed Pod is not proof that business effects are correct.
- **CronJob:** Job semantics plus schedule timezone, concurrency policy, missed-run behavior, deadlines, retention, duplicate execution, and clock assumptions.
- **DaemonSet:** justified per-node placement. Bound privileges, host access, tolerations, update capacity, and blast radius.
- **Bare Pod:** use only when its non-replacement lifecycle is intentional; normally select an owning controller.
- **Init container:** ordered setup that must tolerate Pod restart and avoid writing unsafe shared state.
- **Sidecar:** define startup, readiness, shutdown, resource, failure, and shared-volume behavior rather than assuming auxiliary containers are transparent.

For custom resources and operators, inspect schema, controller ownership, reconciliation, finalizers, external side effects, upgrade conversion, deletion, and recovery. For admission webhooks, include timeout, failure policy, certificate, version compatibility, and API-server availability impact. Custom schedulers, device plugins, runtime classes, and federation or multi-cluster controllers require an evidenced need and explicit operational owner.

## Resources, scheduling, and autoscaling

Base requests and limits on representative measurements and application behavior:

1. Identify startup, steady-state, burst, batch, and failure-recovery demand.
2. Separate compressible CPU behavior from memory, ephemeral storage, device, and external quotas.
3. Check scheduling feasibility, QoS, eviction risk, throttling or OOM behavior, and capacity headroom.
4. Verify ResourceQuota and LimitRange interactions in every target namespace.
5. Reproduce the same workload before and after right-sizing; report range and uncertainty, not false precision.

HPA needs a suitable metric, correct requests where utilization is used, understood stabilization and missing-metric behavior, capacity for new replicas, and dependency limits. VPA may be an add-on and can change Pod resources or require eviction depending on mode and implementation. Cluster autoscaling changes nodes, not application demand; verify node-group bounds, provisioning latency, disruption, topology, storage, DaemonSet overhead, and provider quotas. Evaluate HPA, VPA, and node autoscaling interactions rather than enabling them independently.

Use affinity, anti-affinity, topology spread, taints, tolerations, and priority only for an explicit placement or service-level contract. Priority and preemption can displace other workloads and do not create capacity.

## Probes, shutdown, and rollout

Treat probes as control signals:

- readiness controls whether a Pod should receive Service traffic;
- liveness can restart a container and should indicate a locally unrecoverable condition;
- startup protects slow initialization from premature liveness and readiness evaluation.

Do not copy fixed paths, delays, timeouts, or thresholds. Derive them from measured startup, normal latency, transient dependency failure, saturation, and recovery behavior. Avoid liveness checks whose dependency failure would restart an otherwise recoverable fleet.

For shutdown and rollout, verify preStop behavior if used, signal handling, `terminationGracePeriodSeconds`, endpoint withdrawal, connection draining, in-flight work, retry and idempotence, sidecar ordering, and maximum request or job duration. Exercise rollouts with realistic capacity and dependency behavior.

Blue-green, canary, rolling, and A/B patterns need explicit artifact identity, cohort or traffic selection, compatibility, capacity, signals, observation window, progression, pause, abort, and recovery. A changed Deployment condition does not alone prove user-facing health.

## Disruption and availability

A PodDisruptionBudget constrains supported voluntary evictions; it does not prevent all disruption, create replicas, guarantee application availability, or protect direct Pod or controller deletion. Confirm selector behavior, `minAvailable` or `maxUnavailable`, unhealthy-Pod policy, controller scale, rollout strategy, drain implementation, and current `disruptionsAllowed`.

Also model:

- involuntary node, zone, network, storage, and process failures;
- maintenance, upgrades, autoscaler actions, preemption, and resource-pressure eviction;
- quorum, leader election, state replication, topology, and external dependencies;
- simultaneous disruptions and capacity needed to reschedule.

Test the specific disruption and recovery path in an authorized environment. If no live exercise is allowed, label the result design-only.

## Upgrade workflow

1. Fix the source and target versions, supported path, component version-skew policy, and provider lifecycle constraints.
2. Inventory served and stored APIs, deprecated fields, feature gates, admission webhooks, CRDs, conversion, CSI/CNI, ingress, metrics, autoscalers, and operators.
3. Read release and distribution notes for every crossed version. Separate mandatory compatibility work from optional modernization.
4. Validate manifests and controllers against the target API behavior. Preserve a rollback window only where the platform and persisted data support it.
5. Protect etcd and application data with verified, restorable backups as appropriate; a snapshot alone is not recovery proof.
6. Rehearse representative workloads and cluster add-ons, then stage control-plane and node changes using the supported order.
7. Observe API health, controllers, nodes, scheduling, DNS, networking, storage, admission, workloads, and user journeys before progression.
8. Reconcile source, generated artifacts, field ownership, and runtime state; record remaining deprecated APIs and owner deadlines.

## Validation and evidence

Use the repository's existing toolchain after inspection. A useful evidence ladder is:

1. parse and schema validation for the exact target version;
2. deterministic Helm or Kustomize render with intended values and overlays;
3. semantic assertions for selectors, ownership, resources, security, policy, and version compatibility;
4. policy checks with rule revision and scope recorded;
5. isolated apply or server-side dry run when authorized and representative;
6. staged live rollout with observed controllers, events, Pods, dependencies, and user-facing signals.

Generated YAML is an artifact: review it, keep sensitive values out, and bind reported results to its digest or repository revision. Distinguish command success, API acceptance, controller reconciliation, Pod readiness, and user-facing correctness.
