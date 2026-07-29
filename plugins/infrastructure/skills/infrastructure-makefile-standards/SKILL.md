---
name: infrastructure-makefile-standards
description: Create, update, or review a self-documenting Makefile for a Docker-first repository. Use when a user asks to add or standardize Make targets, repair Makefile safety or portability, or wrap existing project commands with Make. Do not use for application debugging, CI-only changes, or executing deploy, release, teardown, or cleanup targets without explicit authorization.
---

# Docker-First Makefile Standards

Build a thin, truthful interface over commands the repository already supports.
Do not turn the Makefile into a second build system or invent commands to fill a
standard target list.

## Establish the Contract

Before editing:

1. Read the applicable project instructions, existing Makefiles and included
   `.mk` files, developer documentation, Compose configuration, and CI commands.
2. Confirm that Docker-first development is an existing project rule or an
   explicit user request. If it is not, preserve the repository's actual
   execution model instead of imposing this template.
3. Identify the requested public targets, their real underlying commands,
   prerequisites, side effects, and expected exit behavior.
4. Check callers in scripts, CI, documentation, and nested Makefiles before
   renaming or removing a target.
5. Treat every existing recipe as untrusted executable code. Inspect it before
   running `make`, including with dry-run flags.

For a new Docker-first Makefile, read
[references/conventions.md](references/conventions.md), then adapt
[Makefile.template](Makefile.template). Copy the template into the project;
do not include it from an agent installation or cache path.

## Design the Interface

- Keep targets task-oriented and stable: callers should request an outcome, not
  reproduce a tool invocation.
- Declare non-file targets in `.PHONY`.
- Make the default target `help`, and document each public target as
  `target: ## Group: Description`.
- Put project-specific values and commands in `project.mk` or the project's
  existing override mechanism. Use Make variables such as `$(CMD_TEST)`, not
  shell environment syntax, in recipes and documentation.
- Use `?=` for overridable defaults. Preserve command-line overrides unless a
  verified invariant requires GNU Make's `override` directive.
- Use `$(MAKE)` for recursive invocation so flags and jobserver state propagate.
- Keep recipes compatible with the declared shell. Do not claim POSIX
  portability when recipes rely on Bash features or GNU-only utilities.
- Do not print credentials, environment dumps, or interpolated secret values in
  `help`, `info`, logs, or error messages.

Required targets come from repository behavior. A Docker-first project commonly
needs `help`, `config`, `up`, `down`, `restart`, `logs`, `status`, `watch`,
`test`, `lint`, `check`, `validate`, `build`, and `clean`, but omit any target
that has no truthful implementation.

## Guard Side Effects

- Keep read-only inspection separate from lifecycle changes.
- Run Compose validation before starting services when practical.
- Use non-interactive container execution for automation; reserve interactive
  execution for development targets such as `watch`.
- Never add a successful placeholder for deploy, release, publish, migration,
  or destructive maintenance. An unavailable operation must be absent or fail
  clearly.
- Make routine cleanup delete only a narrow generated path. Reject empty,
  absolute, parent, hidden, or multi-segment cleanup paths before deletion.
- Do not remove volumes, dependency caches, databases, or user data from the
  ordinary `clean` target. Put exceptional cleanup behind a separately named
  target with explicit confirmation and project authorization.
- Do not run lifecycle, deployment, release, migration, or cleanup targets
  merely to validate the Makefile.

## Validate

Validate in increasing order of cost and authority:

1. Inspect the raw diff and included files for unexpected recipes, target
   collisions, unsafe interpolation, and broken callers.
2. Parse and preview only inspected targets. `make -n` is a preview, not a
   sandbox: recursive `$(MAKE)` recipe lines may still execute sub-makes.
   It also prints expanded recipes, so do not preview commands that may contain
   credentials or other non-public values.
3. Run `make help` and verify that every intended public target appears once
   with an accurate group and description.
4. For Compose-backed targets, run the repository's read-only configuration
   validation, normally `docker compose config --quiet`.
5. Run the narrowest relevant quality target, then the repository's full
   validation target if authorized. Record a timeout as a timeout, not as a test
   failure; investigate or rerun with an appropriate bound.
6. Exercise failure paths: missing command overrides, invalid configuration,
   and rejected cleanup paths must fail non-zero with actionable messages.
7. Check idempotence and parallel behavior only for targets that claim those
   properties. Do not assume prerequisite targets are safe under `make -j`.

If the repository has no executable fixture or services are unavailable,
perform static checks and safe dry-runs, then state exactly what remains
unverified.

## Completion

Complete only when:

- the Makefile exposes real project operations and preserves existing callers;
- `help` is truthful and the default target is safe;
- routine validation cannot trigger destructive or privileged operations;
- focused validation passes before any full validation claim;
- cleanup and other side effects are narrowly bounded;
- the result and handoff distinguish local checks, full checks, timeouts, and
  any downstream outcome the user explicitly requested.

Report the targets added, changed, or removed; commands actually run; observed
results; skipped side-effecting checks; and remaining risks.
