---
name: infrastructure-devops-standards
description: DevOps standards for CI/CD, configuration management, and pipeline testing.
---

# DevOps Standards

## CI/CD (GitLab)

- Use YAML pipelines with modular, reusable configurations.
- Include stages for build, test, security scans, and deployment.
- Implement gated deployments and rollback mechanisms.

## Configuration Management

- Prefer Terraform for IaC.
- Use Ansible only when explicitly needed and documented.

## Testing

- Test pipelines in sandbox environments.
- Write unit tests for custom scripts or code with mocking for cloud APIs.
