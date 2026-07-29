---
name: infrastructure-makefile-standards
description: Create or update a Docker-first GNU Make interface with grouped help, project-owned overrides, explicit lifecycle targets, and safe validation. Use when a repository asks for these Makefile conventions or already uses the bundled template. Do not use for non-GNU make, a non-Docker workflow, or a repository whose own build contract conflicts with this standard.
---

# Docker-First Makefile Standards

Build a predictable project interface without replacing repository-specific
commands or making mutating targets look successful when they did nothing.

## Read Before Editing

Inspect the repository's instructions, existing Makefiles and included files,
Compose configuration, CI commands, documentation, and callers of public
targets. Read recipes and Make expansions before running any target: parsing an
untrusted Makefile can evaluate functions or included content.

Confirm that GNU Make and a Docker-first development workflow are intended. If
the repository already exposes stable target names, preserve them or provide a
compatible alias unless the user approves a contract change.

## Use the Package Sources

- Read [makefile.md](makefile.md) for the complete conventions.
- Start a new compatible interface from
  [Makefile.template](Makefile.template). For an existing Makefile, merge the
  required behavior instead of overwriting project-owned targets.

Keep technology-specific commands and safe cleanup recipes in `project.mk`.
That file is included last so command variables and additional targets take
effect. Configure the standard command hooks instead of redefining their
recipes, which makes GNU Make emit override warnings. Preserve another
established extension mechanism when the repository already has one.

## Core Contract

- Provide `help`, `up`, `down`, `restart`, `logs`, `watch`, `build`, `check`,
  `clean`, and `status` when they apply to the repository.
- Give every public target a help annotation:
  `target: ## Group: short description`.
- Use the groups `Setup`, `Development`, `Quality`, `Build`, `Maintenance`, and
  `Logs`.
- Use Make variables such as `$(COMPOSE)` and `$(COMPOSE_FILE)` for Compose
  calls. Use `$$name` only when the recipe shell, rather than Make, must expand
  a shell variable.
- Keep recipe syntax compatible with POSIX `sh` where practical, while stating
  honestly that the bundled template relies on GNU Make features.
- Replace sleeps with bounded readiness checks when a real dependency state can
  be observed.
- Never pass untrusted input through command-line Make variable overrides or
  interpolate it into recipes.

Targets for deploy, release, publish, cleanup, or another destructive or
external action must fail clearly until a project-owned implementation exists.
A placeholder message followed by exit status zero is not an implementation.
Adding a target does not authorize executing it.

## Project Override Example

```makefile
# Makefile
include Makefile.template
```

```makefile
# project.mk
PROJECT      := my-service
VERSION      := 1.2.3
DEV_SERVICE  := api
CMD_DEV      := uv run fastapi dev
CMD_TEST     := pytest -q

smoke: ## Quality: Run smoke tests
	@$(COMPOSE) -f $(COMPOSE_FILE) exec $(DEV_SERVICE) pytest -q tests/smoke
```

Treat these values as synthetic. Use the repository's actual commands and
versions; do not copy the example's stack assumptions.

## Validate

After static inspection:

1. verify every annotated public target appears in the intended help group;
2. verify required and compatibility targets exist exactly once after includes;
3. inspect `make -n <target>` output in a disposable or explicitly authorized
   context, remembering that Make expansion and recursive Make can still execute
   during a dry run;
4. run `make help` only after includes and expansions are trusted;
5. run read-only targets, then focused quality/build targets through the
   repository's normal environment;
6. exercise one unimplemented external target and the default cleanup targets,
   confirming that they fail without changing files;
7. execute lifecycle, formatting, cleanup, publish, release, or deploy targets
   only when specifically authorized and in the intended environment.

## Complete

Report preserved and added targets, the override mechanism, exact validation
commands and results, and any unimplemented or unsafe target. Call the interface
ready only when help matches the actual targets, project overrides take effect,
placeholder targets fail closed, and repository tests or builds invoked through
Make match their direct equivalents.
