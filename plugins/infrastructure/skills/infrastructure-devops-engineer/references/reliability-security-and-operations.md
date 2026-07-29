# Reliability, Security, and Operations

Use this reference for observability, SLOs, alerts, incidents, recovery,
security, compliance, culture, documentation, and continuous improvement.

## Contents

- Observability
- SLI, SLO, and alerts
- Incident response
- Recovery and resilience
- Security and compliance
- Secrets and certificates
- Documentation and collaboration
- Improvement and innovation

## Observability

Start from a decision or failure question. Combine signals when they add
different evidence:

- metrics quantify rates, distributions, and resource behavior;
- logs preserve bounded event detail;
- distributed tracing connects work across components;
- profiles can identify code-level resource use when supported;
- synthetic and real-user evidence show externally visible journeys.

Define schema, units, temporality, aggregation, sampling, retention, access,
cost, ownership, and deletion. Bound metric labels and log fields; user IDs,
raw paths, unbounded error text, and request payloads can create privacy,
cardinality, and cost failures. Propagated trace or baggage values are untrusted
inputs and must not carry secrets or become authorization.

Dashboards need an audience, question, source, freshness, units, thresholds,
links, and owner. A chart existing does not prove the data is complete or the
service is healthy.

## SLI, SLO, and Alerts

- Define the user or operator journey, good event, total event, exclusions,
  measurement point, window, data quality, objective, and owner.
- Availability is only one possible objective; latency, correctness,
  durability, freshness, throughput, and recovery may matter.
- Set objectives from product needs, dependency reality, risk, and historical
  evidence. Do not inherit `99.9%` or any other target without that contract.
- An error budget is a policy input for balancing reliability and change. Define
  how it is calculated, who decides, and what actions follow consumption.
- Page on urgent, actionable user-impact risk with a clear owner and runbook.
  Use tickets or reports for non-urgent work. Route, group, deduplicate,
  inhibit, and test alerts, including missing-data and telemetry-failure cases.
- Connect alerting symptoms to diagnostic signals. CPU, queue depth, or one
  failed probe may explain impact, but is not automatically user impact.

## Incident Response

Establish:

1. timestamp, affected users and services, severity basis, incident lead,
   communications owner, and safe channels;
2. exact environment and current revisions, artifacts, configuration,
   dependencies, deployments, alerts, capacity, and recent changes;
3. observed source, pipeline, runtime, provider, data, network, and user
   evidence separated from hypotheses;
4. containment options, authority, reversibility, data risk, and observation;
5. recovery criteria, residual risk, monitoring window, and follow-up.

Preserve relevant logs, traces, events, timelines, commands, and state within
privacy and access policy. Avoid destructive cleanup before evidence capture.
Do not make broad changes from correlation alone.

Runbooks and automated remediation require exact triggers, targets, prechecks,
authority, bounded actions, abort conditions, verification, escalation, and
audit. A war room or ChatOps channel coordinates work; it does not replace
authorization or the system of record.

Post-incident review should be blameless and evidence-based: user impact,
timeline, contributing technical and organizational conditions, detection,
response, recovery, what helped, what hindered, and prioritized actions with
owners and verification. Do not force a single root cause when evidence shows a
system of conditions.

## Recovery and Resilience

- Define recovery-time and recovery-point objectives, data-loss tolerance,
  dependency order, degraded modes, and business priorities.
- Backups require protected storage, retention, integrity, access, restore
  procedure, application/schema compatibility, and regular exercises.
- Test failover, failback, restore, reconciliation, queued work, duplicate
  effects, partial regions or dependencies, certificate/identity availability,
  and operator access.
- Chaos or fault injection requires a hypothesis, bounded blast radius,
  representative environment, safety controls, stop authority, observation,
  cleanup, and learning goal. “Staging” alone does not make it safe.
- Capacity and auto-scaling do not replace overload behavior, load shedding,
  deadlines, backpressure, and dependency protection.

## Security and Compliance

Integrate security throughout design, build, test, release, and operations:

- protect source, branches, reviews, runners, dependencies, registries,
  artifacts, provenance, signing, infrastructure, deployment identities, and
  update channels;
- model trust boundaries, assets, actors, abuse, network paths, data flow,
  persistence, and recovery;
- apply least privilege and separation of duties to build, release, runtime,
  incident, and break-glass roles;
- scan source, dependencies, secrets, images, infrastructure, and runtime where
  applicable, then inspect scope, freshness, false negatives, exploitability,
  reachability, compensating controls, and ownership;
- map compliance claims to current rule versions and preserved evidence.

A passing scanner or policy engine is one input, not security or compliance
approval. Exceptions need owner, scope, reason, expiry, compensating controls,
retest, and revocation.

## Secrets and Certificates

- Prefer short-lived workload identity when the selected platform supports it.
  Otherwise define approved storage, access, injection, rotation, revocation,
  backup, recovery, audit, and incident procedures.
- Never expose values through source, command arguments, logs, debug output,
  artifacts, caches, plans, environment dumps, process listings, telemetry, or
  support bundles.
- Separate secret references from values and verify runtime authorization.
- Certificate management includes issuer trust, name scope, key protection,
  renewal lead time, deployment, overlap, revocation, client trust, clock
  behavior, alerting, and recovery. A renewed certificate is not complete until
  the correct endpoints serve and clients trust it.

## Documentation and Collaboration

Keep architecture, pipeline, environment, ownership, on-call, SLO, alert,
runbook, release, recovery, access, and dependency documentation near its
authoritative source when practical. Validate links, commands, permissions,
versions, and generated content.

Knowledge sharing, skill development, cross-team projects, documentation
culture, and tool standardization should resolve observed ownership or task
friction. Measure whether people can complete supported journeys safely, not
whether a document, workshop, or catalog exists.

## Improvement and Innovation

- Select improvements from user impact, delivery flow, toil, incidents,
  reliability, security, cost, and developer/operator experience.
- For one application or service, deployment frequency, change lead time,
  failed-deployment recovery time, change fail rate, and deployment rework rate
  can reveal delivery constraints. Use them over time, not as cross-team
  rankings, individual quotas, or universal targets.
- Use small proofs of concept with an explicit hypothesis, owner, scope, data,
  security, cost, license, success/failure criteria, cleanup, and adoption
  decision.
- Evaluate tools for compatibility, maintenance, support, portability,
  operational load, data handling, supply chain, migration, and exit path.
- Hackathons, innovation time, conferences, open-source contribution, and
  continuous learning can be useful practices, but are not delivery evidence.
- Compare a service or workflow with its own baseline over time. Do not rank
  unrelated teams or turn delivery, satisfaction, or activity metrics into
  individual quotas.
