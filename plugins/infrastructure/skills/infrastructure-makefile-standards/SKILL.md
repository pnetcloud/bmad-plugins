---
name: infrastructure-makefile-standards
description: Makefile conventions and usage patterns for this repo.
---

# Makefile Standards (Docker-first)

Use this skill when creating or updating Makefiles in this repo.

## Source of truth

- Standards: `makefile.mdс`
- Template: `Makefile.template`

## Core rules (summary)

- Base all project Makefiles on the template.
- Put tech-specific commands in `project.mk` overrides, not in the template.
- Required targets: `help`, `up`, `down`, `restart`, `logs`, `watch`, `build`, `check`, `clean`, `status`.
- All public targets must include a docstring: `target: ## <Group>: <short description>`.
- Use `${COMPOSE}` + `${COMPOSE_FILE}` for Docker Compose calls.
- Prefer POSIX shell; avoid GNU-only utilities and non-deterministic sleeps.

## Help convention

- Use `make help` for grouped, colorized output.
- Group labels: `Setup`, `Development`, `Quality`, `Build`, `Maintenance`, `Logs`.

## Example

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
