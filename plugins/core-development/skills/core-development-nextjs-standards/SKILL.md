---
name: core-development-nextjs-standards
description: Next.js standards for App Router, components, SEO, routing, and data fetching.
---

# Next.js Standards

## Purpose and selection

Use for Next.js App Router components, routes, metadata, localization, and data-loading work. Do not apply App Router APIs to a different framework or convert an existing Pages Router application without a migration request.

## Working mode

Inspect the installed Next.js version, application root, router, translation system, and cache behavior first. Treat the `apps/` statement below as a layout assumption to confirm, not permission to relocate an existing application. Request missing route or freshness requirements before selecting behavior.

## Focus

- Project context: Next.js UI lives under `apps/` (primary frontend stack).

- Use App Router (`app/`) for new work; avoid legacy `pages/`.

- Prefer Server Components by default; use Client Components only when needed.

- Always define metadata (`title`, `description`, `og:image`) for SEO.

- Use dynamic imports for heavy components (code splitting).

- Organize routes in nested folders with `layout.tsx` for shared layouts.

- In App Router, implement locale negotiation and locale-prefixed routes
  explicitly (for example, `app/[lang]`), set the document language, and load
  localized content through the project's translation system. Do not assume
  Pages Router `i18n` configuration provides App Router routing or translations.

- In App Router, fetch data directly from its source in async Server Components;
  use Route Handlers when a Client Component or external caller needs an HTTP
  endpoint. Choose caching or revalidation explicitly. Use
  `generateStaticParams` only to prebuild dynamic route segments; do not use
  Pages Router data functions such as `getServerSideProps` under `app/`.

- Use API Routes only for lightweight tasks; keep business logic in backend services.

## Quality checks

Use configured build, type, lint, and route tests; verify metadata, localized navigation, server/client boundaries, and the intended caching or revalidation behavior for changed routes. Report checks and runtime states not exercised.

## Return

Return the targeted implementation or review findings, affected routes and source revision where relevant, validation results, and unresolved localization or data-freshness decisions.

## Boundaries

Do not change framework versions, move application roots, migrate routers, modify backend contracts, or deploy beyond the authorized request. Preserve existing route and cache contracts unless their change is approved.
