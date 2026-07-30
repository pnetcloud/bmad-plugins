---
name: infrastructure-gitlab-ci-standards
description: GitLab CI/CD standards for stages, rules, caching, artifacts, and secrets.
---

# GitLab CI/CD Standards

- Define only the stages required by artifact- and risk-selected jobs. Preserve
  `lint -> test -> build -> deploy` when all four apply, and omit `deploy` for
  non-deployable outcomes.
- Use `rules:` instead of `only/except` for clarity.
- Cache dependencies with proper keys.
- Store artifacts with expirations; limit retention.
- Keep secrets out of the repository and job output; prefer an external secrets
  provider. When GitLab variables are required, mask, hide, protect, and
  environment-scope them, and expose them only to reviewed trusted jobs on
  protected refs and environments. Treat masking as log redaction, not access
  control, and stop when pipeline code or source trust is unresolved.
- Require pipeline green status before merge.
