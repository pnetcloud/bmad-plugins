---
name: core-development-nextjs-standards
description: Next.js standards for App Router, components, SEO, routing, and data fetching.
---

# Next.js Standards

- Project context: Next.js UI lives under `apps/` (primary frontend stack).
- Use App Router (`app/`) for new work; avoid legacy `pages/`.
- Prefer Server Components by default; use Client Components only when needed.
- Always define metadata (`title`, `description`, `og:image`) for SEO.
- Use dynamic imports for heavy components (code splitting).
- Organize routes in nested folders with `layout.tsx` for shared layouts.
- Implement i18n with Next.js built-in internationalization support.
- In App Router, fetch data directly from its source in async Server Components;
  use Route Handlers when a Client Component or external caller needs an HTTP
  endpoint. Choose caching or revalidation explicitly. Use
  `generateStaticParams` only to prebuild dynamic route segments; do not use
  Pages Router data functions such as `getServerSideProps` under `app/`.
- Use API Routes only for lightweight tasks; keep business logic in backend services.
