---
name: infrastructure-devops-standards
description: DevOps standards for CI/CD, configuration management, and pipeline testing.
---

# DevOps Standards

## CI/CD (GitLab)

- Use YAML pipelines with modular, reusable configurations.
- Select build, test, security, and deployment jobs with artifact- and
  risk-based rules. Deployment rules must fail closed, and non-deployable
  outcomes must not create deployment jobs.
- Each deployment job must name its exact environment, use protected-environment
  deploy permissions and required approvals where applicable, and serialize
  changes with a matching `resource_group`. Observe rollout health and prove
  rollback; a green job alone is not deployment verification.

## Configuration Management

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

## Runtime Provider Limits and Backpressure

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

## Testing

- Test pipelines in sandbox environments.
- Write unit tests for custom scripts or code with mocking for cloud APIs.
