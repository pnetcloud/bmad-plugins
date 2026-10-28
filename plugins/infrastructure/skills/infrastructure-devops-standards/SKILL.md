---
name: infrastructure-devops-standards
description: DevOps standards for CI/CD, configuration management, and pipeline testing.
---

# DevOps Standards

## Purpose and selection

Apply CI/CD, configuration-management, and provider-backpressure standards to the requested pipeline or infrastructure artifact; do not introduce a new platform or IaC tool for unrelated application-only work.

## Working mode

Inspect the existing pipeline, deployment model, IaC/state ownership, provider operating mode, and test entrypoints first. Select only rules relevant to the requested change; ask for unresolved environment, ownership, throughput, or acceptance requirements before mutation.

## Focus

### CI/CD (GitLab)

- Use YAML pipelines with modular, reusable configurations.
- Select build, test, security, and deployment jobs with artifact- and
  risk-based rules. Deployment rules must fail closed, and non-deployable
  outcomes must not create deployment jobs.
- Each deployment job must name its exact environment, use protected-environment
  deploy permissions and required approvals where applicable, and serialize
  changes with a matching `resource_group`. Observe rollout health and prove
  rollback; a green job alone is not deployment verification.

### Configuration Management

- Follow the repository's existing IaC tool, state, and ownership boundaries.
  Prefer Terraform for new IaC only when those boundaries permit it; introduce
  or migrate to Terraform only with an explicit, reviewed adoption and state
  migration plan. Before adopting existing resources, map each remote object to
  exactly one configured resource address, protect and back up state, use state
  locking where supported, and approve a plan with no unintended create,
  change, or destroy actions before transferring ownership.
- Use Ansible only for an identified configuration-management need. Document
  its inventory source, ownership, and interaction with IaC.
- Stop before changing managed infrastructure when its tool, state, ownership,
  inventory source, or mutation boundaries are unresolved. Do not give IaC and
  Ansible overlapping authority over the same resource properties.

### Runtime Provider Limits and Backpressure

- When pipelines or services depend on rate-limited external providers, document
  both configured and effective throughput in one canonical unit, then expose
  actual throughput, throttles, 429/limit responses, timeouts, retry backlog,
  overdue retry checkpoints, and drain ETA separately.
- Treat free, proxy, or development-provider modes as constrained operating
  modes, not production assumptions. Lower request rates and wait through
  expected throttling when that mode is selected; require subscription/API-mode
  limits and acceptance evidence before claiming production readiness.
- Preserve baseline safety holds, but avoid letting transient provider failures
  block durable stream progress indefinitely: persist retryable work before
  acknowledging source offsets, replay it from a retry scheduler or parking lot,
  and verify backlog drains before closing the change.

## Quality checks

### Testing

- Test pipelines in sandbox environments.
- Write unit tests for custom scripts or code with mocking for cloud APIs.

Report actual sandbox/test results, rollout and rollback evidence, and backlog-drain observations separately from configuration or submitted jobs. Mark unavailable checks and unmeasured provider limits explicitly.

## Return

Return the affected pipeline/configuration changes or review, source revision when available, selected risks and checks, observed outcomes, unresolved state/ownership or provider-limit gaps, and the next validation owner.

## Boundaries

Loading this standard does not authorize deployments, state adoption/migration, cloud calls, provider subscription changes, or overlapping resource ownership. Require explicit target-scoped authority for external writes, protect state and secrets, and stop when source trust, environment, or mutation scope is unresolved.
