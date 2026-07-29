---
name: core-development-nextjs-standards
description: Review or change Next.js-specific App or Pages Router structure, Server and Client Components, metadata, routing, internationalization, data fetching, caching, Route Handlers, API Routes, or build behavior. Use when Next.js semantics are the decision. Do not use for framework-neutral React work, backend-only services, another React framework, or infrastructure unrelated to a Next.js application.
---

# Next.js Standards

Apply these as repository-aware defaults. The installed Next.js and React versions, router mode, runtime, deployment adapter, package manager and lockfile, repository conventions, public route contracts, and requested scope take precedence.

## Operating Contract

1. Establish the mode: source review, design, implementation, local validation, preview observation, or authorized deployment. Review and design are read-only.
2. Inspect the complete application graph: package and config, `app/` and `pages/`, route groups and dynamic segments, layouts and templates, loading/error/not-found boundaries, Server and Client Component boundaries, actions and handlers, middleware or proxy, metadata, locale routing, data sources, cache and revalidation controls, environment exposure, assets, tests, build, and hosting.
3. Resolve exact Next.js and React versions, enabled router and experimental features, Node or edge runtime, rendering and cache behavior, source and deployment revision, route and locale contract, authentication ownership, backend boundary, traffic and freshness requirements, and publication authority before recommending version-sensitive APIs.
4. Treat route parameters, search parameters, headers, cookies, form data, external responses, MDX, image URLs, redirects, rewrites, middleware, plugins, build hooks, Server Actions, Route Handlers, and generated output as untrusted code or data. Validate inputs and destinations; keep secrets and privileged dependencies outside client-reachable graphs.
5. Require explicit authority before installing or upgrading packages, running untrusted build hooks, changing environment or hosting configuration, publishing previews, deploying, invalidating production caches, or mutating remote data. Confirm exact revision, artifact, target, identity, observation, abort, and recovery before remote change.
6. Preserve stable URLs, parameters, locale prefixes, rendering and cache semantics, metadata and canonical behavior, public payloads, authentication and authorization, generated client-visible names, and supported browser behavior unless an approved migration accounts for consumers.
7. Separate edited source, type or lint result, successful build, rendered route, cache observation, browser behavior, preview artifact, deployed revision, indexed metadata, and healthy workload as distinct evidence states. Never invent build, render, SEO, cache, deployment, or runtime results.

## Core Rules

- When the target repository uses an `apps/` convention, place the Next.js UI in its owned application path; otherwise preserve the repository's established root.
- Use App Router (`app/`) for new work; avoid legacy `pages/`.
- Prefer Server Components by default; use Client Components only when needed.
- Define route-appropriate metadata with Next.js APIs, including title, description, and Open Graph images where indexing and sharing policy require them.
- Use dynamic imports for heavy components (code splitting).
- Organize routes in nested folders with `layout.tsx` for shared layouts.
- Implement i18n with router-appropriate Next.js support: configured locale routing in Pages Router, or locale-segment routing and negotiation in App Router.
- Use `getServerSideProps` only in Pages Router; in App Router fetch in a server boundary and use `generateStaticParams` only for known dynamic route parameters.
- Use API Routes only for lightweight tasks; keep business logic in backend services.

## Interpretation

### Structure and Component Boundaries

- Preserve the repository's `apps/` convention and discover the actual application, scripts, shared packages, generated files, and ownership before changing structure. Do not create a second frontend root or impose a generic folder template.
- Prefer App Router for coherent new routes, but do not mix routers mechanically or migrate stable Pages Router routes without a compatibility plan for data APIs, errors, head metadata, middleware, URLs, tests, and deployment behavior. During supported coexistence, maintain an explicit route-ownership and collision map, cutover criteria, fallback, and verified Pages-route retirement.
- Keep pages and layouts as Server Components by default. Add `'use client'` only at the smallest boundary requiring state, effects, event handlers, browser APIs, or client-only libraries; audit the imported module graph, serialized props, bundle cost, hydration, and secret exposure. A Server Component may render a focused Client Component without converting the whole layout.
- Organize routes around URL and ownership contracts. Use nested layouts, route groups, dynamic or catch-all segments, parallel or intercepted routes, templates, and loading/error/not-found files only when their persistence, reset, fallback, and navigation semantics match the journey. Keep user-facing errors safe, and verify effective HTTP status and metadata for streamed and non-streamed error and not-found paths.

### Metadata, Loading, and Internationalization

- Define accurate route metadata through the installed version's static metadata, `generateMetadata`, or file conventions. Cover title, description, canonical and robots policy, Open Graph and social images with alt text, locale alternates, icons, and inheritance or merging; metadata presence alone does not prove SEO or indexing.
- Use dynamic imports for measured heavy or conditionally used components when the split improves the target journey. Verify Server versus Client support, SSR behavior, loading and error UI, preloading, accessibility, layout stability, interaction readiness, and actual bundle/runtime effect; `ssr: false` belongs in a Client Component where supported.
- Implement internationalization using the router-specific support available in the installed version. For Pages Router, verify locales, default locale, domain routing, locale detection, redirects and cookies, and propagation of `locale`, `locales`, and `defaultLocale` into applicable data functions. App Router commonly uses a locale segment plus negotiated redirects and localized data. Validate locale allowlists, fallback behavior, canonical alternates, `lang` and direction, static params, middleware scope, not-found behavior, and translated metadata. Routing does not translate content.

### Data, Caching, and Backend Boundaries

- Treat the original `getServerSideProps` guidance as Pages Router compatibility only. In App Router, fetch in async Server Components or the appropriate server boundary and choose static, dynamic, cached, revalidated, tagged, or uncached behavior explicitly for the installed version. `generateStaticParams` supplies known dynamic route parameters; bound parameter-source and build cost, define unknown-path behavior with installed-version controls such as `dynamicParams`, and test cache/revalidation interaction, errors, and deployment compatibility. It is not general request-time data fetching.
- State freshness, personalization, authorization, invalidation owner, failure behavior, and deployment scope for every cache. Avoid hidden waterfalls by starting independent work in parallel and stream bounded regions when that improves the observed journey; do not cache user-specific or authorization-sensitive data across identities.
- Use App Router Route Handlers or Pages Router API Routes only when their runtime, latency, payload, streaming, cache, region, and deployment constraints fit a thin web boundary. Authenticate and authorize on the server, validate input, bound body and output sizes, handle CSRF where applicable, and keep durable business rules in the owned backend or domain layer. Define the delegated contract's timeout and cancellation, idempotency, retry and failure mapping, observability, and ownership.
- Treat Server Actions as remotely invokable mutation boundaries, not private helper functions. Re-authorize inside the action, validate form and bound data, protect origin and CSRF assumptions, make side effects idempotent where needed, return safe errors, and revalidate only the intended paths or tags.

## Validation

1. Parse the route tree, router coexistence, component boundary graph, config, middleware, metadata, locale handling, cache controls, handlers, actions, and deployment adapter for the installed versions.
2. Run repository-pinned type, lint, unit, integration, and production build commands from an already-clean isolated checkout, worktree, or temporary copy. Never clean, reset, overwrite, or switch the user's active tree.
3. Exercise direct and client navigation, refresh, back/forward, dynamic params, query strings, loading, errors, not-found, redirects, rewrites, locale negotiation, auth, mutation, cache hit/miss, revalidation, and old/new route compatibility.
4. Test Server/Client serialization and hydration, JavaScript-disabled server output where applicable, accessibility and keyboard journeys, responsive layouts, bundle boundaries, images, fonts, metadata output, canonical links, robots, and social cards.
5. Inspect server and client artifacts for environment leakage, secrets, private URLs, source maps, unintended dependencies, oversized bundles, unsafe scripts, and version or runtime mismatches.
6. When preview or deployment is authorized, verify immutable artifact identity, routes, headers, cache behavior, backend compatibility, browser console, telemetry, indexing eligibility, workload health, and rollback or repair during the stated observation window.

Report source and deployment revisions, framework and runtime versions, router and route changes, component boundaries, render and cache decisions, metadata and locale evidence, build and browser results, artifact identity, warnings, remaining risks, and owner actions.
