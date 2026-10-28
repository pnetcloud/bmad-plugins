---
name: infrastructure-makefile-standards
description: Makefile conventions and usage patterns for this repo.
---

# Makefile Standards (Docker-first)

## Purpose and selection

Use this skill when creating or updating Makefiles in this repo.

Do not select this Docker-first convention for repositories that neither request Makefile work nor adopt this target contract.

## Working mode

### Source of truth

- Standards: `makefile.md`
- Template: `Makefile.template`

Read `makefile.md` and `Makefile.template` before editing; inspect existing includes, Compose configuration, and `project.mk` overrides. Resolve conflicts with the repository owner rather than silently replacing its workflow.

## Focus

### Core rules (summary)

- Base all project Makefiles on the template.
- Put tech-specific commands in `project.mk` overrides, not in the template.
- Required targets: `help`, `up`, `down`, `restart`, `logs`, `watch`, `build`, `check`, `clean`, `status`.
- All public targets must include a docstring: `target: ## <Group>: <short description>`.
- Use `$(COMPOSE)` + `$(COMPOSE_FILE)` for Docker Compose calls.
- Prefer POSIX shell; avoid GNU-only utilities and non-deterministic sleeps.

### Help convention

- Use `make help` for grouped, colorized output.
- Group labels: `Setup`, `Development`, `Quality`, `Build`, `Maintenance`, `Logs`.

### Example

```makefile
# Makefile (project)
include Makefile.template

```

```makefile
# project.mk (project-specific overrides)
PROJECT      := my-service
VERSION      := 1.2.3
DEV_SERVICE  := api
CMD_DEV      := uv run fastapi dev
CMD_TEST     := pytest -q

smoke: ## Quality: Run smoke tests
	@$(COMPOSE) -f $(COMPOSE_FILE) exec $(DEV_SERVICE) pytest -q tests/smoke
```

## Quality checks

Check required targets, docstrings/groups, variable overrides, Compose selection, recipe portability, and readiness behavior. Inspect recipes and parse-time expansion before invoking make, including help or dry-run: they can execute commands. Run only authorized, understood checks; distinguish a parsed target from an exercised successful recipe, and report checks not run.

## Return

Return the Makefile or override changes, relevant template/source revision, checks performed, compatibility gaps, and any unresolved target ownership or runtime validation.

## Boundaries

Template recipes are not permission to start/stop containers, remove artifacts or dependencies, deploy, release, or publish. Confirm target, data impact, and authority before execution; protect secrets in logs. Loading this skill grants no infrastructure changes or global template installation.
