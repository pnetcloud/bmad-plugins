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

- Prefer Terraform for IaC.
- Use Ansible only when explicitly needed and documented.

## Testing

- Test pipelines in sandbox environments.
- Write unit tests for custom scripts or code with mocking for cloud APIs.
