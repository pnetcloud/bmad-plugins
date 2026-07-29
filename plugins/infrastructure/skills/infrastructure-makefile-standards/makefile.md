---
description: Unified GNU Make standards for a Docker-first development environment
globs: ["**/Makefile", "**/makefile", "**/*.mk"]
alwaysApply: true
priority: 100
category: coding-standards
tags: [makefile, docker, compose, automation, standards]
---

# Makefile Rules — Docker-first

## Goals

- Standardize a minimal, universal target set.
- Use Docker Compose for dev/runtime orchestration.
- Keep tech-specific commands in `project.mk` overrides.

## Source of Truth

- **Template**: `Makefile.template` in this skill package
- Each project Makefile should be based on the template and configure command
  variables or add project targets through `project.mk`.

## Required Core Targets

- `help` — grouped, colorized, self-documenting help
- `up` / `down` / `restart` / `logs` — Docker stack lifecycle
- `watch` — run app in watch mode (via container)
- `build` — produce artefact
- `check` — aggregate: `lint` + `test`
- `clean` — remove artefacts
- `status` — quick health/info summary

## Variables & Overrides

Override in `project.mk`:

- `PROJECT` — project name
- `VERSION` — semver or VCS tag/short SHA
- `COMPOSE` — Docker Compose command (`docker compose` or a compatible wrapper)
- `COMPOSE_FILE` — compose file path (default `compose.yaml`)
- `DEV_SERVICE` — service for `watch`/exec
- `CMD_DEV` — dev command (e.g., `npm run dev`, `air`, `uv run fastapi dev`)
- `CMD_BUILD` — build command
- `CMD_TEST` — run tests
- `CMD_LINT` — run linters
- `CMD_FORMAT` — format code
- `CMD_DEPLOY` — deploy command; empty by default
- `CMD_RELEASE` — release command; empty by default
- `CMD_PUBLISH` — publish command; empty by default
- `CMD_CLEAN` — project-scoped artifact cleanup; empty by default
- `CMD_CLEAN_ALL` — broader project-scoped cleanup; empty by default

Standard targets fail closed while their command variable is empty. Prefer
configuring these hooks over redefining the standard recipes.

## Help Output Conventions

Each public target must include a docstring comment:

```
target-name: ## <Group>: <short description>
```

Group labels: `Setup`, `Development`, `Quality`, `Build`, `Maintenance`, `Logs`.

## Docker Compose Expectations

- Use `$(COMPOSE)` and `$(COMPOSE_FILE)` for all Compose calls.
- Dev service should mount source code and expose required ports.
- `watch` runs inside the container using `$(DEV_SERVICE)` and `$(CMD_DEV)`.

## Cross-platform

- The template uses GNU Make features; do not present it as portable POSIX make.
- Prefer POSIX `sh` in recipes and avoid shell-specific extensions.
- Avoid GNU-only utilities unless guarded.
- Do not print secrets in logs.

## Don’ts

- No tech-specific flags in the global standards file.
- No hard-coded paths to language toolchains.
- Avoid non-deterministic sleeps; use readiness checks where possible.
- No successful placeholder for deploy, release, publish, cleanup, or another
  external or destructive operation.
