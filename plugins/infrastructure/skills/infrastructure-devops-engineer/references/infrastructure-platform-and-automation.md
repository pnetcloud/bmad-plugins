# Infrastructure, Platform, and Automation

Use this reference for infrastructure as code, configuration, containers,
cloud, networking, GitOps, platform engineering, automation, performance, and
cost.

## Contents

- Infrastructure and configuration
- Containers and orchestration
- Cloud and network boundaries
- GitOps
- Automation design
- Platform engineering
- Performance and capacity
- Cost and sustainability

## Infrastructure and Configuration

Follow the selected repository and tool contract for Terraform modules,
CloudFormation templates, Ansible playbooks, Pulumi programs, or other
configuration management. Do not translate practices between tools without
checking their state, preview, execution, failure, and secret semantics.

- Version infrastructure and configuration source, but do not commit state,
  sensitive plans, credentials, or generated secret-bearing output.
- Identify the exact root, state or inventory, backend, account, region,
  environment, identity, lock, and writer before provider contact or mutation.
- Review previews or diffs against current remote state. Drift can mean a defect,
  an intentional external owner, an incident, or stale evidence; do not
  reconcile it blindly.
- Define imports, moves, replacements, removals, lifecycle, retries, partial
  failure, recovery, and disaster-recovery evidence.
- Keep dynamic configuration, service discovery, certificates, and feature
  flags under explicit ownership, schema, access, propagation, audit, expiry,
  and failure rules.

## Containers and Orchestration

Inspect the repository's Docker, Kubernetes, Helm, registry, service-mesh, and
runtime contracts rather than assuming all are present.

- Build minimal auditable images from verified bases. Separate build and runtime
  contents when useful; remove build credentials and unnecessary tools.
- Define process, signal, filesystem, user, capability, network, resource,
  startup, readiness, liveness, and shutdown behavior from the application.
  Multiple coordinated processes can be legitimate when lifecycle ownership is
  explicit; “one process” is not a universal rule.
- Pin and promote by immutable digest where the platform supports it. Protect
  registry permissions, mutable tags, retention, signing/provenance, scanning,
  and garbage collection.
- For Kubernetes and Helm, verify namespace/context, selectors, ownership,
  policies, service accounts, storage, disruption, scheduling, autoscaling,
  probes, hooks, CRDs, values/schema, upgrade path, and rollback limits.
- Treat service mesh adoption as an architecture change with identity,
  certificate, policy, traffic, latency, observability, failure, upgrade, and
  operator-cost consequences.

## Cloud and Network Boundaries

Do not select a single-cloud or multi-cloud strategy from a capability list.
Establish business continuity, data residency, latency, service dependency,
skills, portability, cost, contractual, and failure-domain needs.

Public-cloud families such as AWS, Azure, and GCP differ in identity, account
hierarchy, region, managed-service, quota, network, and recovery semantics.
Inspect the selected provider and repository contracts instead of transferring
resource or permission assumptions between them.

- Verify account/subscription/project, region, network, DNS, certificate, load
  balancer, firewall/policy, routing, identity, quota, and shared-service owners.
- Prefer least exposure and explicit allow rules, but derive public/private
  reachability and encryption boundaries from the actual trust and product
  contract. Internal location alone is not trust.
- Test name resolution, certificate renewal, failover, health checks, retries,
  timeouts, connection limits, and asymmetric routing where applicable.
- Disaster recovery requires objectives, dependency inventory, protected
  backups or replicas, access, restore/failover procedure, exercises, and
  reconciliation—not a diagram or successful scheduled job.

## GitOps

Call a workflow GitOps only when:

1. desired state is declarative;
2. it is versioned with immutable history;
3. software agents pull desired state from the approved source;
4. agents continuously observe and attempt to reconcile actual state.

Define repository and ownership boundaries, source-to-target mapping, promotion,
branch and merge policy, deployment triggers, secret references, controller
identity, reconciliation interval, health, drift, suspension, emergency
changes, rollback or forward repair, audit, and break-glass reconciliation.

A push-based deployment from Git is CI/CD, but not automatically GitOps. Manual
runtime repair may be necessary during an incident; record it and reconcile the
declared source afterward without overwriting still-needed evidence.

## Automation Design

Scripts, internal tools, API integrations, workflow automation, ChatOps,
runbook automation, and self-service operations need:

- explicit typed inputs and exact target resolution;
- authentication, authorization, least privilege, and audit;
- preview or dry-run semantics when truthful;
- idempotency or reconciliation behavior;
- bounded concurrency, retries, timeouts, rate limits, and pagination;
- partial-success and cleanup handling;
- safe output and redaction;
- stable exit/result contracts and tests;
- owner, version, support, deprecation, and emergency stop.

Chat commands are not authorization by themselves. Confirm the initiator,
scope, target, approval, and visible result through the trusted control plane.
Measure toil removed and task success, not lines of automation or percentage of
manual work replaced.

## Platform Engineering

Treat a platform as a product for internal users:

- start from frequent journeys and constraints;
- define supported golden paths and documented escape hatches;
- expose stable platform APIs, service catalogs, templates, portals, and
  policy feedback only when they reduce verified friction;
- keep ownership, tenancy, quota, access, cost visibility, compliance,
  observability, support, versioning, migration, and deprecation explicit;
- measure adoption, retention, task success, reliability, delivery outcomes,
  cognitive load, and developer experience.

Do not force tool standardization where teams have different constraints and no
shared support benefit. A portal that links to manual tickets is not proven
self-service; test the complete user journey.

## Performance and Capacity

Use representative workload, topology, data, configuration, network, and
release mode. Establish a baseline before changing:

- application and dependency latency, throughput, errors, and saturation;
- CPU, memory, storage, image/startup, queue, connection, and concurrency use;
- caching correctness, keys, freshness, invalidation, stampede, and failure;
- load-balancing distribution, draining, health, retry, and failover behavior;
- autoscaling signals, stabilization, limits, cold starts, quotas, and scale-down;
- database tuning ownership, plans, locks, connections, replication, and recovery.

Change one evidenced bottleneck and remeasure with the same method. Faster
pipeline or infrastructure execution is not useful if it weakens correctness,
reproducibility, or recovery.

## Cost and Sustainability

- Tie estimates to a dated plan, pricing source, region, usage, discounts,
  shared costs, retention, data transfer, support, and excluded items.
- Define budgets and alerts by scope, owner, currency, period, threshold,
  notification delay, and response. An alert is not a spending cap.
- Validate tag/label support and propagation before relying on chargeback or
  showback. Document unattributed and shared costs.
- Base optimization on observed usage and service constraints. Review
  reservations, rightsizing, scheduling, storage tiers, retention, egress, and
  architecture changes with reliability and labor tradeoffs.
- Automated cost actions that scale down, stop, delete, or change commitment
  require explicit authority, safety bounds, and recovery.
- Report realized savings only from comparable bills or usage over a meaningful
  period; label estimates and ROI assumptions.
