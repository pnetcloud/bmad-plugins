---
name: core-development-javascript-standards
description: JavaScript/TypeScript standards for code style, typing, runtime configuration, testing, and security.
---

# JavaScript/TypeScript Standards

## Purpose and selection

Apply these standards when writing or reviewing JavaScript or TypeScript in a repository. Use framework-specific guidance for routing or rendering decisions; this is not a mandate to migrate another language or replace the project stack.

## Working mode

Inspect the affected code, package manifest, lockfile, runtime pins, and lint/type/test configuration before changing it. Use the existing commands and report missing configuration rather than silently introducing a new toolchain.

## Focus

### Code Style and Conventions

- Enforce ESLint and Prettier with consistent import ordering.
- Use `camelCase` for variables and functions; `PascalCase` for classes and components.
- Prefer `kebab-case` for file names and keep folder structure consistent.
- Favor small, pure functions with single responsibility.

### TypeScript

- Enable `strict`; avoid `any`; prefer precise types.
- Define explicit interfaces/types for APIs and component props.
- Use type narrowing and type guards; leverage utility types.

### Async and Errors

- Prefer async/await; always handle rejections.
- Centralize error handling and logging at boundaries; no silent failures.
- Validate inputs at edges; sanitize untrusted data.

### Node/Runtime

- Manage config via environment; no secrets in code or VCS.
- Follow the repository's runtime-version mechanism; if none exists, choose an
  explicit runtime pin for development and CI. Use `engines` to declare
  supported Node versions, not as an assumed enforced pin; commit the lockfile.
- Follow the repository's existing package manager and lockfile. For a new
  project, choose the manager explicitly and record its version in
  `packageManager`.
- For containerized development, keep `node_modules`, build outputs (for
  example, `.next`), and the selected package manager's cache or store in
  volumes to avoid host pollution and symlink issues.

### Performance and Security

- Avoid expensive work in render loops; debounce/throttle user-driven events.
- No `eval` or dynamic code from untrusted sources; audit dependencies regularly.

## Quality checks

Run the relevant configured lint, formatting, type, and test checks on the affected scope; exercise async failures and input boundaries where changed. Identify checks not available or not run.

### Testing

- Unit and integration tests per module; avoid snapshot-only tests.
- Aim for meaningful coverage; test behavior and edge cases.

## Return

Return the focused patch or review findings with file locations, applicable runtime/toolchain context, check results, and remaining risks.

## Boundaries

Do not replace package managers, upgrade runtimes, install global tools, expose secrets, or deploy merely to enforce this standard. Seek approval for compatibility-breaking changes outside the requested scope.
