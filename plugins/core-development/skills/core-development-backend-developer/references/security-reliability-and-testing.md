# Security, Reliability, and Testing

Read this reference for trust-boundary, production-readiness, performance, or
operational changes. Tailor controls to the data, threat model, repository, and
deployment environment.

## Contents

- Authentication and authorization
- Input, output, and dependency trust
- Data and secrets
- Reliability and configuration
- Observability
- Performance and capacity
- Test matrix
- Container and release readiness

## Authentication and Authorization

- Reuse the established identity provider and validated library. Do not invent
  token formats or implement cryptographic protocols from scratch.
- Validate issuer, audience, signature/algorithm, validity window, and
  credential status as the selected protocol requires. Bound clock tolerance
  and reject ambiguous identities.
- Separate authentication from authorization. Enforce permission for the
  specific action, object, field, tenant, and current state on every path,
  including batch, export, background, administrative, and indirect-reference
  paths.
- Fit role-based, attribute-based, or relationship-based policy to the existing
  domain; do not force RBAC when roles cannot express the required boundary.
- Derive tenant scope from trusted identity or server-side state, not a
  caller-provided identifier alone.
- Treat sessions, refresh credentials, API keys, service identities, and
  webhook secrets as credentials with issuance, scope, storage, rotation,
  revocation, audit, and expiry behavior.
- Avoid disclosing whether a protected object exists when that distinction
  leaks information.

## Input, Output, and Dependency Trust

- Use current OWASP API Security guidance as a threat checklist where
  applicable, not as proof that an implementation is secure or compliant.
- Validate syntactic shape and semantic constraints; canonicalize only when its
  security meaning is defined.
- Use context-appropriate output encoding. Sanitization is not a universal
  substitute for validation, safe APIs, or authorization.
- Constrain server-initiated requests by allowed scheme, destination, DNS/IP
  resolution behavior, redirect policy, port, response size, time, and network
  boundary. Re-check after redirects and resolution changes as the platform
  requires.
- Verify webhook origin using the protocol's authenticated bytes and replay
  controls before parsing side effects. Preserve the raw representation when
  signature rules require it.
- Treat upstream APIs as untrusted: validate schema, bounds, status, redirects,
  and failure behavior; do not forward their errors or credentials blindly.
- Inventory externally reachable endpoints and remove accidental debug,
  metadata, health-detail, documentation, or legacy exposure through an
  authorized change.

## Data and Secrets

- Minimize collected, returned, logged, cached, and retained data. Apply
  field-level response allowlists where overexposure is plausible.
- Use established transport protection and managed cryptographic facilities.
  Record key ownership and rotation without exposing key material.
- Keep secrets out of source and default configuration. Prevent secret values
  from appearing in exceptions, command output, build layers, telemetry, or
  fixtures.
- Make audit events tamper-resistant enough for their purpose and include actor,
  action, target category, outcome, and trusted time while excluding secret and
  unnecessary sensitive values.

## Reliability and Configuration

- Validate required non-secret configuration at startup. Distinguish absent,
  malformed, unsafe, and unavailable secret material without printing it.
- Keep feature flags temporary and owned. Define default, scope, evaluation
  failure, mixed-version behavior, observability, and removal criteria.
- Liveness should answer whether restart may help; readiness should answer
  whether new work can be served. Avoid deep dependency checks that create
  restart storms or leak internals.
- During shutdown, stop admission, mark unready when appropriate, drain bounded
  work, respect the platform deadline, and preserve/requeue work according to
  acknowledgement semantics.
- Configuration hot reload is optional. If used, validate atomically, retain
  the last known-good state, expose version/outcome safely, and define which
  fields require restart.

## Observability

Use the repository's selected logging and telemetry stack. Traces, metrics, and
logs are complementary signals, not mandatory products.

- Logs: structured event and error class with bounded context; redact at the
  source and test the redaction path.
- Metrics: user-visible outcomes, rate, latency distribution, error class, and
  saturation with bounded cardinality.
- Traces: meaningful boundaries and status with controlled sampling,
  propagation, and attribute allowlists.
- Health and business signals: truthful ownership, threshold rationale,
  alert route, and runbook.

Correlation identifiers are not authentication and may be sensitive. Do not
return or propagate internal identifiers solely for convenience.

## Performance and Capacity

1. Define the user-visible metric, workload, data distribution, environment,
   baseline, budget, and expected change.
2. Profile before optimizing and identify the limiting resource.
3. Change one coherent bottleneck while preserving correctness and security.
4. Re-measure with the same method; include warmup, sample size, percentile or
   distribution, variance, and resource use.
5. Test saturation and recovery, not only the happy-path median.

Consider query count/plans, serialization, allocations, connection and worker
pools, lock contention, cache behavior, payload sizes, compression, queue lag,
downstream quotas, and autoscaling feedback. Do not claim improvement from a
microbenchmark that omits the production bottleneck.

## Test Matrix

Select applicable layers:

| Layer | Evidence |
| --- | --- |
| Unit | domain invariants, validation, error mapping, idempotency decision |
| Endpoint integration | routing, middleware, decoding, auth, serialization, error mapping |
| Data integration | real store plus transaction commit, rollback, isolation, atomicity, conflicts |
| Authentication flow | credential/session/token validation, claims, expiry, refresh, rotation, revocation |
| Dependency integration | real broker/cache/upstream boundary and cleanup |
| Contract | request/event schema, compatibility, errors, limits, examples |
| Migration | clean install, upgrades, representative volume, interruption |
| Authorization | cross-identity object, action, field, tenant, and state cases |
| Concurrency | race, duplicate, conflict, cancellation, timeout, shutdown |
| Resilience | dependency slow/fail/recover, overload, retry budget, degraded mode |
| Security | injection classes, SSRF boundary, credential leakage, abuse limits |
| Performance | representative workload, baseline, saturation, recovery |
| Operational | built artifact, config, health, signals, rollout/rollback exercise |

Use generated, synthetic, or approved fixtures. Keep tests deterministic where
possible, isolate external effects, and retain a failing input as a regression
case. A mocked boundary proves local behavior, not integration behavior.

## Container and Release Readiness

When containers are part of the existing deployment:

- use the project's build path, multi-stage build where it materially reduces
  the trusted runtime surface, and pinned/reviewed base policy;
- keep build tools and credentials out of the runtime image;
- run as the expected non-privileged identity where supported;
- define filesystem, network, signal, resource, and shutdown needs;
- scan the actual built artifact using supported tooling and triage findings;
- verify health behavior and configuration inside the resulting artifact.

Prefer promoting the same verified artifact with external environment-specific
configuration over rebuilding different application code for each environment.

Before rollout, establish migration ordering, compatibility window, canary or
staged signals, abort criteria, rollback/forward-fix limits, and responsible
operator. Report separately: locally tested, artifact built, scan completed,
deployed, traffic shifted, and production verified.
