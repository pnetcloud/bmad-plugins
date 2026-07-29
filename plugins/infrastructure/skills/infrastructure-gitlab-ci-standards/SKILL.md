---
name: infrastructure-gitlab-ci-standards
description: GitLab CI/CD standards for stages, rules, caching, artifacts, and secrets.
---

# GitLab CI/CD Standards

- Define stages: lint -> test -> build -> deploy.
- Use `rules:` instead of `only/except` for clarity.
- Cache dependencies with proper keys.
- Store artifacts with expirations; limit retention.
- Use protected variables for secrets.
- Require pipeline green status before merge.
