# Workload Architecture, Reliability, and Migration

Use for service selection, workload decomposition, scaling, resilience, disaster recovery, hybrid or multi-cloud placement, and migration.

## Contents

- [Start from the workload](#start-from-the-workload)
- [Select patterns and services](#select-patterns-and-services)
- [Reliability and recovery](#reliability-and-recovery)
- [Multi-cloud and hybrid placement](#multi-cloud-and-hybrid-placement)
- [Migration workflow](#migration-workflow)

## Start from the workload

Define business journeys, users, trust boundaries, data, dependencies, demand shape, latency, availability and recovery objectives, change rate, operating skills, regulatory scope, and unit economics. Prioritize requirements and record which pillar tradeoffs are accepted. Provider Well-Architected reviews are workload-specific decision inputs, not certifications or proof of implementation.

Map current flows and ownership before drawing a target. Separate known evidence, assumptions, decisions, and open questions. Use an architecture decision record for material choices: context, options, selection, consequences, cost basis, security and recovery impact, owner, review trigger, and exit constraints.

## Select patterns and services

Choose the simplest supported service that satisfies the required behavior and operating model:

- serverless functions need event, concurrency, retry, idempotency, duration, state, cold-start, quota, observability, and cost contracts;
- event-driven designs need schema, ordering, delivery, duplicate, poison-message, replay, backpressure, retention, and ownership contracts;
- API gateways need identity, authorization, validation, quotas, routing, versioning, failure, and exposure boundaries;
- containers and service meshes need an evidenced orchestration or identity/traffic need plus lifecycle, capacity, upgrade, and operator ownership;
- microservices require independently owned business boundaries and justified distribution costs, not anticipated scale alone;
- edge and IoT designs require device identity, intermittent connectivity, update, revocation, local data, physical trust, and fleet recovery;
- GPU and HPC choices require workload fit, scheduler, data locality, quota, utilization, interruption, supply, and exit analysis.

Avoid a provider service mapping that hides different consistency, identity, failure, quota, lifecycle, or pricing semantics behind a false common API.

## Reliability and recovery

Derive SLOs from business journeys and dependencies. Availability is an observed outcome over a defined window, not a property of a diagram or replica count.

Model region, zone, control plane, identity, DNS, network, compute, storage, data, key management, deployment, and third-party failures. Define degradation, load shedding, retries, timeouts, circuit breaking, capacity headroom, and reconciliation without creating retry storms or correlated failure.

For DR:

1. define RTO and RPO per protected journey and data set;
2. establish consistency, replication, backup, keys, dependencies, and recovery environment;
3. define detection, decision authority, failover, traffic, writer fencing, and split-brain prevention;
4. exercise restore or failover and failback with representative application and business validation;
5. reconcile infrastructure, data, queues, identity, DNS, clients, and source of truth;
6. report measured results, data loss, residual risk, and untested dependencies.

Multi-region is optional. It adds replication, consistency, traffic, cost, deployment, security, and operator complexity; use it only when the objectives justify those tradeoffs.

## Multi-cloud and hybrid placement

Select providers or on-premises placement from workload needs, residency, service capability, failure independence, latency, connectivity, skills, contracts, cost, and exit requirements. Multi-cloud is not automatically resilient, portable, cheaper, or free of lock-in.

For each distributed workload, define source of truth, identity federation, trust, connectivity, routing, data synchronization, consistency, observability, management plane, cost allocation, capacity, failure isolation, and recovery. Test cloud/provider and private-connectivity loss rather than assuming diverse brands imply independent failure.

Lock-in mitigation is a deliberate tradeoff. Preserve portability at the interfaces and data boundaries where exit value exceeds the loss of provider capability and the continuing abstraction cost.

## Migration workflow

Use the provider or organization's named and versioned migration taxonomy as a classification aid, not an automatic answer. Current AWS guidance uses 7 Rs; if existing material says 6Rs, identify the omitted or combined strategy instead of silently treating the taxonomies as equivalent. For each application:

1. discover dependencies, data, identity, traffic, schedules, licenses, owners, operational procedures, and current baseline;
2. choose retain, retire, rehost, relocate, replatform, repurchase, or refactor based on business value and risk;
3. group waves by dependency and recovery boundaries, not convenience alone;
4. run a bounded pilot representative of the hard parts;
5. validate security, performance, cost, operations, compatibility, and recovery;
6. define data replication, freeze or coexistence, cutover, observation, abort, fallback limits, and communication;
7. decommission only with separate authority after retention, audit, billing, DNS, identity, backup, and residual-data checks.

A completed transfer is not a completed migration. Require business journey, data, integration, security, observability, cost, support, and recovery evidence.
