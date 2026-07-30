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

## Testing

- Test pipelines in sandbox environments.
- Write unit tests for custom scripts or code with mocking for cloud APIs.
