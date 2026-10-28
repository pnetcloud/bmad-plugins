---
name: infrastructure-gitlab-ci-standards
description: GitLab CI/CD standards for stages, rules, caching, artifacts, and secrets.
---

# GitLab CI/CD Standards

## Purpose and selection

Apply these rules when authoring, reviewing, or optimizing GitLab CI/CD stages, job selection, caches, artifacts, or secret handling; do not select them for another CI provider or unrelated application code.

## Working mode

Inspect the current pipeline/includes, artifact/deployment intent, protected refs/environments, runner resources, and required checks. Establish representative timing/cache baselines before optimization; request missing source-trust or environment requirements rather than guessing.

## Focus

- Define only the stages required by artifact- and risk-selected jobs. Preserve
  `lint -> test -> build -> deploy` when all four apply, and omit `deploy` for
  non-deployable outcomes.

- Use `rules:` instead of `only/except` for clarity.

- Cache dependencies with proper keys.

- Store artifacts with expirations; limit retention.

## Quality checks

- When optimizing slow pipelines, measure queue/setup time, test/job durations,
  and the critical path before changing test selection. Compare representative
  before/after runs with the same required checks and runner resources; record
  cache state. Do not treat cache hits, test splitting, or a green pipeline with
  skipped required checks as proof of faster equivalent validation. If timings
  or coverage equivalence cannot be verified, report the gap rather than claim
  an improvement.

- Require pipeline green status before merge.

Validate expanded configuration and representative selected jobs with available GitLab/repository checks. A green job is not rollout health or equivalent coverage; report checks not run and distinguish configuration, attempted runs, and observed results.

## Return

Return pipeline changes or findings, relevant source revision and included configuration, selected required checks, measured timings/cache conditions when applicable, validation results, and unresolved trust, coverage, or deployment decisions.

## Boundaries

- Keep secrets out of the repository and job output; prefer an external secrets
  provider. When GitLab variables are required, mask, hide, protect, and
  environment-scope them, and expose them only to reviewed trusted jobs on
  protected refs and environments. Treat masking as log redaction, not access
  control, and stop when pipeline code or source trust is unresolved.

Loading this standard grants no GitLab API, variable, runner, protected-environment, merge, or deployment changes. Use only available tools and explicitly authorized targets; stop before unapproved external writes and verify the exact target after authorized changes.
