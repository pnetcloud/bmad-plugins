---
name: infrastructure-devops-standards
description: Review or change repository DevOps standards for GitLab CI/CD structure, gated delivery, configuration-management tool choice, and pipeline or automation testing. Use when these cross-cutting standards are the decision being made. Do not use for a narrow application change, provider-specific Terraform implementation, or GitLab syntax question with no standards decision.
---

# DevOps Standards

Apply the following as repository-aware defaults, not universal mandates. Existing project instructions, declared toolchains, delivery contracts, and explicit user scope take precedence.

## Operating Contract

1. Establish the mode: standards review, proposal, source change, local validation, pipeline execution, or remote delivery. Review and proposal are read-only.
2. Inspect project instructions, current pipeline includes and inputs, build/test commands, lockfiles, generated ownership, runners, trust boundaries, environments, artifacts, caches, credentials, IaC/configuration tools, and deployment ownership before changing a standard.
3. Make the smallest coherent change. Do not introduce Terraform, Ansible, a stage, scanner, cache, matrix, deployment, or rollback mechanism unless the repository and requested behavior require it.
4. Treat repository commands, includes, components, container images, generators, plugins, hooks, and custom scripts as untrusted execution surfaces. Inspect them before running; remove ambient credentials unconditionally; isolate filesystem, network, and provider access.
5. Keep untrusted contribution pipelines separate from privileged release contexts. Run untrusted jobs on isolated unprivileged runners with trust-scoped disposable caches; do not expose protected variables, tokens, signing material, provider identities, protected or privileged runners, trusted release caches, or deployment controls to attacker-controlled code.
6. Require explicit authority before triggering or cancelling pipelines, changing CI/CD settings, variables, runners, protected branches or environments, publishing or deleting artifacts, applying infrastructure, deploying, rolling back, or changing remote state. Emergency language does not widen authority.
7. Validate source and behavior separately. CI lint establishes configuration validity only; a created pipeline is not a passing pipeline, a passing pipeline is not a verified artifact, and a deployment command is not a healthy rollout.
8. Report exact source revision, configuration evaluated, commands and pipeline IDs actually observed, artifact identity, warnings, unresolved risk, and remaining owner actions. Never invent scan, deployment, rollback, sandbox, or production results.

## CI/CD (GitLab)

- Use YAML pipelines with modular, reusable configurations.
- Include stages for build, test, security scans, and deployment.
- Implement gated deployments and rollback mechanisms.

Interpret these defaults conditionally:

- Prefer a small visible pipeline graph. Reuse configuration only when it reduces real duplication without hiding trust, ordering, inputs, or ownership.
- Derive stages and jobs from existing project commands and failure risks. A repository may legitimately omit build, scan, or deploy stages.
- Pin or otherwise verify external includes, components, images, and tools according to repository policy. Review resolved configuration and input validation.
- Model `rules`, pipeline sources, protected refs, environment scopes, job dependencies, artifact flow, and manual approvals explicitly; test both expected inclusion and exclusion.
- Model variable source, precedence, expansion, protection, environment scope, masking limitations, pipeline-variable restrictions, and forwarding into downstream pipelines. Prefer typed inputs for reusable configuration where supported; masking is neither authorization nor containment.
- Treat caches as disposable optimization. Key and isolate them by correctness and trust inputs; never use a cache as the sole carrier of a required artifact.
- Promote an immutable, verified artifact when the delivery model supports it. Define target, compatibility, health signals, observation, pause, abort, and recovery before deployment.
- Rollback is conditional on data, schema, configuration, dependency, and artifact compatibility. Use forward repair, restore, or containment when reversal is unsafe.

## Configuration Management

- Prefer Terraform for IaC.
- Use Ansible only when explicitly needed and documented.

Tool choice follows the actual resource lifecycle:

- Use the repository's established IaC tool unless a documented decision proves a change is necessary.
- Terraform is suitable for declarative resource ownership when provider support, state, locking, identity, import, drift, plan review, and recovery are defined.
- Ansible is suitable when ordered host or application configuration is genuinely required and inventory, idempotence, privilege, secret handling, check-mode limits, and partial-failure recovery are understood.
- Separate architecture and tool selection from implementation. Never add a second source of truth for the same resource accidentally.
- Inspect plan or diff output for sensitive values and destructive or replacement actions. A clean plan can become stale and does not authorize apply.

## Testing

- Test pipelines in sandbox environments.
- Write unit tests for custom scripts or code with mocking for cloud APIs.

Use a layered evidence ladder:

1. Parse and validate the complete resolved configuration, including trusted includes and declared inputs.
2. Unit-test custom parsing, generation, policy, and orchestration logic, including invalid input and failure paths.
3. Use mocks for deterministic unit boundaries, not as proof of provider, runner, artifact, or deployment behavior.
4. Exercise representative pipeline-source and rule combinations without privileged credentials.
5. Run integration tests in an authorized isolated target with bounded identity, network, cost, concurrency, cleanup, residual-state reconciliation, and recovery.
6. Observe an authorized pipeline and, when applicable, staged rollout through artifact identity, controller state, workload health, and user-facing signals.

Completion receipt:

- **Source:** files and revision reviewed or changed.
- **Validation:** syntax, resolved configuration, unit, rule, integration, and pipeline evidence actually observed.
- **Artifact:** immutable identity, provenance evidence, retention, and verification state.
- **Delivery:** environment, authority, rollout observation, and recovery state, or `not run`.
- **Remaining:** unsupported paths, missing evidence, residual risk, and owner action.
