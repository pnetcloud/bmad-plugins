# Makefile Conventions for Docker-First Repositories

Read this reference when creating a Makefile from the bundled template or when
reviewing the detailed behavior of an existing Docker-first Makefile.

## Contents

- Public target contract
- Variables and overrides
- Self-documenting help
- Docker Compose
- Portability and parallelism
- Safe cleanup
- Validation ladder

## Public Target Contract

Choose targets from demonstrated project operations. Keep names stable once
scripts, CI, or documentation depend on them.

| Target | Expected behavior |
|---|---|
| `help` | List public targets and their truthful descriptions without side effects. |
| `config` | Validate configuration without starting or changing services. |
| `up` | Create or start the development stack. |
| `down` | Stop the stack without deleting persistent data by default. |
| `restart` | Restart existing services without implying a rebuild or reconfiguration. |
| `logs` | Stream service logs; allow service selection when the project needs it. |
| `status` | Show current service state without mutation. |
| `watch` | Run the declared interactive development command. |
| `test` / `lint` | Run one focused quality operation and preserve its exit status. |
| `check` | Run the fast, repeatable quality set in a deterministic order. |
| `validate` | Run the project's complete local validation contract. |
| `build` | Produce the documented build artifact. |
| `clean` | Remove only explicitly bounded generated output. |

Do not add a target solely for uniformity. In particular, deployment, release,
publication, database migration, and data-reset targets need a real authorized
workflow and stronger project-specific gates.

## Variables and Overrides

- Use `?=` for safe defaults that a command line or `project.mk` may replace.
- Keep command variables empty when no portable default exists. Fail clearly
  when a target needs an unset command.
- Use recursively expanded `=` variables when their value must reflect
  overrides loaded later; use simply expanded `:=` variables for fixed values.
- Quote shell values according to the declared recipe shell. Make expansion and
  shell expansion are different stages; do not pass untrusted values through
  either without understanding both.
- Use `$(MAKE)` rather than a literal `make` for recursive calls.
- Avoid the `override` directive unless a command-line value would violate a
  verified invariant.

Keep secrets outside Make defaults and checked-in override files. Never expose
them through diagnostic targets.

## Self-Documenting Help

Use one machine-readable annotation shape:

```makefile
test: ## Quality: Run focused tests
```

The help parser and annotations must agree exactly. Keep internal helpers
undocumented so they do not appear as public operations. Avoid mandatory color
or terminal control sequences because help is also consumed by CI logs and
other tools.

## Docker Compose

- Prefer the current `docker compose` command unless the repository documents a
  different compatible wrapper.
- Pass the Compose file explicitly when reproducibility requires it. Otherwise,
  preserve the repository's normal discovery behavior.
- Validate with `docker compose config --quiet` before mutation when practical.
- Use project naming or equivalent isolation when multiple local stacks can
  collide.
- Use non-interactive execution for tests, lint, builds, and CI. Interactive
  defaults are appropriate only for developer-facing sessions.
- Keep volume deletion and orphan cleanup out of ordinary lifecycle targets
  unless the project's public contract explicitly requires them.

## Portability and Parallelism

Declare the intended Make and shell implementations. `.PHONY`,
`.DEFAULT_GOAL`, and `.DELETE_ON_ERROR` are appropriate for GNU Make templates;
do not describe such a template as portable to every Make implementation.

Assume each recipe line runs in a separate shell unless the Makefile explicitly
changes that behavior. Avoid hidden dependence on shell state from a previous
line. When targets share mutable services or output, sequence them explicitly
instead of relying on prerequisite order under parallel execution.

## Safe Cleanup

A routine cleanup target should:

1. operate on a generated path owned by the project;
2. permit the selected path through a narrow project-owned allowlist;
3. quote the argument and prefix relative names explicitly;
4. leave dependencies, caches, volumes, databases, and user data intact;
5. propagate deletion errors rather than claiming success.

Use a separate, plainly destructive target for any wider cleanup and require
explicit user authorization before running it.

## Validation Ladder

Use the cheapest discriminating evidence first:

1. inspect the Makefile and includes;
2. verify parsing and `help`;
3. validate configuration without mutation;
4. run a focused target;
5. run the full local validation contract;
6. verify downstream artifacts or state only when the user requested that
   outcome and authorized the required access.

A dry-run does not prove shell commands will succeed, and a local green check
does not prove publication, deployment, or another downstream outcome.
