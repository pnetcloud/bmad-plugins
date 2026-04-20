---
name: core-development-javascript-standards
description: JavaScript/TypeScript standards for code style, typing, runtime configuration, testing, and security.
---

# JavaScript/TypeScript Standards

## Code Style and Conventions

- Enforce ESLint and Prettier with consistent import ordering.
- Use `camelCase` for variables and functions; `PascalCase` for classes and components.
- Prefer `kebab-case` for file names and keep folder structure consistent.
- Favor small, pure functions with single responsibility.

## TypeScript

- Enable `strict`; avoid `any`; prefer precise types.
- Define explicit interfaces/types for APIs and component props.
- Use type narrowing and type guards; leverage utility types.

## Async and Errors

- Prefer async/await; always handle rejections.
- Centralize error handling and logging at boundaries; no silent failures.
- Validate inputs at edges; sanitize untrusted data.

## Node/Runtime

- Manage config via environment; no secrets in code or VCS.
- Use `.nvmrc` or `engines` to pin Node version; lock dependencies.
- Prefer pnpm for JS/TS projects; set `packageManager` in `package.json`.
- For containerized development, keep `node_modules`, build outputs (for example, `.next`), and pnpm store in volumes to avoid host pollution and symlink issues.

## Testing

- Unit and integration tests per module; avoid snapshot-only tests.
- Aim for meaningful coverage; test behavior and edge cases.

## Performance and Security

- Avoid expensive work in render loops; debounce/throttle user-driven events.
- No `eval` or dynamic code from untrusted sources; audit dependencies regularly.
