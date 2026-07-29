---
name: infrastructure-gitlab-ci-standards
description: Review or change repository standards for GitLab CI/CD stages, workflow and job rules, variables, caches, artifacts, includes, runners, merge gates, and protected delivery. Use when GitLab-specific pipeline behavior or policy is the decision. Do not use for generic DevOps architecture, a narrow application change, or another CI provider.
---

# GitLab CI/CD Standards

Apply these as repository-aware defaults. The exact GitLab version and tier, project instructions, existing pipeline contracts, runner model, and requested scope take precedence.

## Operating Contract

1. Establish the mode: source review, standards proposal, source change, local validation, pipeline observation, or authorized remote operation. Review and proposal are read-only.
2. Inspect the complete configuration graph: root YAML, local and remote includes or components, declared inputs, defaults, `workflow:rules`, job `rules`, stages, `needs`, variables, runners, images, services, caches, artifacts, environments, deployments, and project/group settings that affect behavior.
3. Resolve exact GitLab version, pipeline sources, refs, trust boundary, repository revision, runner protection and privilege, environment, artifact identity, variables, approvals, and expected jobs before changing behavior.
4. Treat includes, components, images, services, generators, hooks, custom executors, and job scripts as code execution. Verify source and revision, inspect effects, remove ambient credentials unconditionally, and use isolated unprivileged runners for untrusted code. Account for the automatically issued `CI_JOB_TOKEN`: resolve its triggering identity, effective permissions, reachable APIs and resources, inbound and outbound allowlists, feature visibility, version-specific controls, and denial behavior from untrusted contexts.
5. Separate untrusted contribution pipelines from privileged release contexts. Use trust-scoped disposable caches and withhold protected variables, provider or signing identities, protected or privileged runners, trusted release caches, and deployment controls.
6. Require explicit authority before creating, retrying, cancelling, or deleting pipelines or jobs; changing variables, runners, schedules, protected refs, environments, approvals, or settings; publishing or deleting artifacts; or deploying and rolling back. Emergency language does not widen authority.
7. Validate resolved syntax, pipeline creation, job selection, job execution, artifact identity, and rollout health as distinct evidence states. Never invent pipeline, security, merge, deployment, or rollback results.

- Define stages: lint -> test -> build -> deploy.
- Use `rules:` instead of `only/except` for clarity.
- Cache dependencies with proper keys.
- Store artifacts with expirations; limit retention.
- Use protected variables for secrets.
- Require pipeline green status before merge.

## Interpretation

- Derive stages and jobs from repository commands, artifact flow, failure risks, and delivery ownership. Omit a stage when it has no real job; add specialized stages only when the dependency graph benefits.
- Prefer `rules` for new or consistently migrated jobs, but do not mechanically mix or convert rule systems. Model first-match order, `when`, `allow_failure`, `changes`, `exists`, variables, pipeline source, protected refs, and duplicate-pipeline behavior. Use `workflow:rules` for pipeline-level admission.
- Reuse configuration only when it reduces real duplication without hiding inputs, trust, ordering, or ownership. Prefer validated typed inputs where supported. Pin or otherwise verify external includes and components; inspect the resolved configuration.
- Model variable source, precedence, expansion, protection, environment scope, masking limits, pipeline-variable restrictions, file-versus-value behavior, and downstream forwarding. Masking is neither authorization nor containment.
- Cache is a disposable optimization, never the sole carrier of a required build result. Keys include every correctness input and trust context; define pull/push policy, fallback behavior, size, cleanup, and poisoning resistance.
- Artifacts are explicit job outputs. Define producer, consumers through `needs` or dependencies, immutable identity, integrity or provenance evidence, paths, access, retention, expiration, and cleanup. Before claiming a deletion bound, inspect the project and instance keep-latest-successful policy, manually kept artifacts, permissions, and actual cleanup; `expire_in` alone does not prove deletion. Do not publish secrets, credentials, full environment dumps, or unrelated data.
- Protected variables are available only under their configured ref and environment conditions and must remain least-privileged. Prefer bounded short-lived identities where supported; do not rely on masking to stop malicious scripts from exfiltrating a value.
- A green pipeline is necessary only when repository policy says so and is never sufficient by itself. Merge gates must identify required pipeline type and revision, blocking jobs, allowed failures, stale or duplicate pipelines, approvals, and bypass ownership.
- Deployment jobs require exact target, artifact, authority, compatibility, health signals, observation window, pause, abort, and recovery. Rollback remains conditional on data, schema, configuration, dependency, and artifact compatibility.

## Validation

1. Parse and lint the complete resolved configuration for the intended GitLab version and input values.
2. Exercise positive and negative `workflow` and job-rule cases for push, merge request, tag, schedule, API, parent/child, and other applicable sources.
3. Unit-test custom scripts and generators, including invalid input, failure, cancellation, concurrency, and output handling.
4. Test caches and artifacts across producer/consumer, retry, expiry, missing-data, and trust-boundary cases.
5. Use an authorized isolated target for runner, service, provider, or deployment integration, with bounded identity, network, cost, concurrency, cleanup, residual-state reconciliation, and recovery.
6. Observe the actual pipeline, immutable artifact, and staged workload when those claims are in scope and authorized.

Report source revision, resolved configuration, GitLab and runner versions, pipeline source and ID, selected and skipped jobs, warnings, artifacts, delivery observation, remaining risks, and owner actions. CI Lint proves configuration validity only; it does not prove job execution, artifact correctness, merge safety, or deployment health.
