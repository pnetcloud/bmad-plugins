# Delivery Pipelines and Artifacts

Use this reference for CI/CD, build, test, artifact, promotion, deployment, and
recovery decisions.

## Contents

- Pipeline contract
- Trust and execution
- Tests and quality gates
- Dependencies and caches
- Artifact identity and provenance
- Promotion and deployment
- Feature flags and configuration
- Failure and recovery
- Pipeline evidence

## Pipeline Contract

Model the pipeline as a state machine with explicit inputs, outputs, owners, and
failure transitions:

1. reviewed source revision and generated-source ownership;
2. dependency resolution and toolchain/runtime identity;
3. build and test contexts;
4. immutable artifact identity and metadata;
5. policy, security, license, and cost evidence;
6. environment-specific configuration and approvals;
7. deployment, observation, abort, and recovery.

Keep independent safe checks parallel when that reduces latency without hiding
dependencies. Fail early on deterministic cheap defects, but do not call a gate
“fast” if it starves representative tests or makes failures nondiagnostic.

## Trust and Execution

- Separate untrusted contribution contexts from trusted release contexts.
  Untrusted code, workflow changes, build scripts, test output, and artifacts
  must not gain release credentials merely by running in CI.
- Minimize token and credential scope, duration, audience, environment, and
  repository reach. Protect logs, debug modes, process listings, artifacts,
  caches, and child processes from disclosure.
- Treat runners and reusable workflows as dependencies. Verify their ownership,
  isolation, update policy, egress, persistence, and access to other jobs.
- Require review for workflow, permission, identity, protected-environment,
  signing, registry, and release-policy changes.
- Serialize writers that can race on a shared environment, state, registry tag,
  release record, or mutable deployment target.

## Tests and Quality Gates

Use a risk-shaped portfolio:

- format, syntax, schema, lint, and generated-file checks;
- unit and component tests;
- contract and compatibility tests;
- dependency, data, infrastructure, and provider integration;
- security, policy, license, and supply-chain checks;
- performance, capacity, resilience, recovery, and operational tests;
- end-to-end checks for the critical user or operator journey.

Measure coverage only when its definition and decision are explicit. A coverage
percentage is not a universal quality threshold and does not prove important
failures. Quarantine does not cure flaky tests: preserve evidence, assign an
owner, bound duration, and either fix the cause or remove a test only when its
behavior is covered elsewhere.

Every gate needs:

- a threat or failure it detects;
- deterministic inputs and a supported environment;
- a clear owner and remediation path;
- bounded retry and timeout behavior;
- an exception owner, scope, expiry, compensating controls, and retest;
- a distinction between warning, blocking, and unavailable evidence.

## Dependencies and Caches

- Use repository lock files and verified package, action, image, module, chart,
  plugin, and tool sources. Treat tag mutability and transitive dependencies as
  supply-chain inputs.
- Do not upgrade dependencies incidentally. Review source, version, digest or
  checksum, signatures or attestations when used, platform compatibility,
  release notes, and generated lock changes.
- Key caches by all inputs that affect correctness and trust. Never let an
  untrusted context populate a cache later trusted by a release job without
  verification and isolation.
- Do not cache credentials, sensitive plans, signing material, or uncontrolled
  build output. Define retention and invalidation.

## Artifact Identity and Provenance

An artifact contract should identify:

- source revision and dirty/generated state;
- build definition, platform, toolchain, dependencies, and external parameters;
- immutable digest and content type;
- tests and policy evidence that apply to that digest;
- signature or provenance producer and verification expectations;
- SBOM or equivalent dependency inventory when required;
- retention, access, promotion, deprecation, and revocation.

Provenance is verifiable information about how an artifact was produced. A
self-authored metadata file or a CI badge is not equivalent to trusted,
verified provenance. Verify artifact identity again at promotion and deployment.

## Promotion and Deployment

Choose by failure mode, capacity, compatibility, and recovery:

- rolling updates trade speed, surge capacity, and mixed-version time;
- canaries expose a bounded population and require cohort-aware signals;
- blue/green or parallel environments require capacity and data/config
  compatibility before traffic changes;
- recreate strategies may be appropriate when overlap is unsafe;
- progressive delivery needs explicit steps, observation windows, pause and
  abort criteria, and ownership.

Promote the same verified artifact when it is truly environment-neutral.
Externalize environment configuration without weakening validation. When
compile-time or platform-specific inputs change the artifact, produce and attest
distinct identities rather than pretending they are the same build.

Before remote delivery, verify target, artifact digest, configuration, secrets
references, migrations, dependencies, capacity, health semantics, alert state,
traffic path, change window, approver authority, and recovery.

## Feature Flags and Configuration

- Define owner, purpose, type, safe default, audience, evaluation location,
  exposure event, dependency, expiry, and removal plan.
- Protect configuration and flags as change surfaces. Audit privileged changes
  and validate schema, compatibility, propagation, stale-cache, and unavailable
  provider behavior.
- Do not use a flag to bypass a required deployment, security, compliance, or
  marketplace review.
- Separate secret values from ordinary configuration and from feature-control
  data. A secret reference is not proof that runtime identity may read it.

## Failure and Recovery

Treat rollback as conditional rather than universal.

For every deploy or pipeline mutation define:

- timeout, cancellation, partial success, and retry semantics;
- idempotency or reconciliation identity;
- cleanup and residual-artifact ownership;
- concurrent writer behavior;
- data/schema and mixed-version compatibility;
- whether rollback, roll-forward, traffic isolation, disablement, or restore is
  the safe recovery path;
- evidence required to declare recovery complete.

Do not automate rollback solely from one noisy signal. Confirm user impact,
artifact and target identity, signal quality, recovery safety, and ownership.

## Pipeline Evidence

Do not collapse evidence states: a valid workflow file is not an executed
pipeline, a passing build is not a deployable artifact, and a deployment
command is not a healthy rollout.

Report separately:

- configuration parsed or validated;
- pipeline executed and exact revision/context;
- artifact produced and digest;
- artifact checks and their scope;
- environment deployment attempted;
- rollout observed and user-facing signal;
- recovery exercised;
- remaining approvals or evidence.
