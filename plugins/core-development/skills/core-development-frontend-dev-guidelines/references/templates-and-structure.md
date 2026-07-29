# Templates and Structure

Use these checklists and templates only after inspecting the target repository.
They preserve the original quick-start surface while making project-specific
choices explicit.

## Contents

- [New Component Checklist](#new-component-checklist)
- [New Page Checklist](#new-page-checklist)
- [Import Aliases](#import-aliases)
- [Common Imports](#common-imports)
- [File Organization Alternatives](#file-organization-alternatives)
- [Server Component Template](#server-component-template)
- [Client Component Template](#client-component-template)
- [Related Guidance](#related-guidance)

## New Component Checklist

- [ ] Determine the smallest valid Server/Client Component boundary.
- [ ] Add `'use client'` only for required client behavior.
- [ ] Define props with the project's TypeScript conventions.
- [ ] Reuse established UI primitives, tokens, aliases, and utilities.
- [ ] Keep privileged data and secrets on a trusted server boundary.
- [ ] Pass serializable props across the server/client boundary.
- [ ] Implement relevant pending, empty, error, disabled, and success states.
- [ ] Verify keyboard, focus, responsive, locale, and motion behavior.
- [ ] Preserve the project's export and file-placement conventions.
- [ ] Add or update focused tests.

## New Page Checklist

- [ ] Confirm App Router and the installed Next.js version.
- [ ] Create the route in the repository's established route hierarchy.
- [ ] Keep the page server-side unless it owns client-only behavior.
- [ ] Define data freshness, cache, invalidation, and authorization semantics.
- [ ] Reuse page-specific and shared components in their existing locations.
- [ ] Add loading, empty, error, not-found, and redirect behavior as applicable.
- [ ] Add static or dynamic metadata under the product's SEO/privacy policy.
- [ ] Test direct navigation, client navigation, refresh, and relevant devices.

## Import Aliases

Aliases are configured contracts, not defaults. Inspect `tsconfig.json`,
`jsconfig.json`, bundler configuration, and `components.json`.

| Common alias | Possible target | Example |
| --- | --- | --- |
| `@/` | project or source root | `import type { Post } from '@/types/post'` |
| `@/components` | shared components | `import { Button } from '@/components/ui/button'` |
| `@/lib` | shared utilities | `import { cn } from '@/lib/utils'` |
| `@/hooks` | client hooks | `import { useMobile } from '@/hooks/use-mobile'` |
| `@/app` | App Router root | `import { createPost } from '@/app/actions/posts'` |

Use only aliases the target resolves. Preserve relative imports if they are the
project convention.

## Common Imports

Server-capable module:

```tsx
import type { Metadata } from 'next'
import { Suspense } from 'react'
import { notFound, redirect } from 'next/navigation'
```

Client module:

```tsx
'use client'

import { useCallback, useMemo, useState } from 'react'
```

Import optimization hooks only when the component actually needs them. Typical
project-owned UI and utility imports may look like:

```tsx
import type { ComponentProps } from 'react'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { cn } from '@/lib/utils'
```

These paths are illustrative. Inspect the target configuration first.

## File Organization Alternatives

Next.js prescribes route file conventions, not one universal organization for
all non-route code. Preserve the current project layout.

### Route-colocated example

```text
app/
  posts/
    page.tsx
    loading.tsx
    error.tsx
    components/
      PostList.tsx
    actions.ts
```

### Feature-oriented example

```text
app/
  posts/
    page.tsx
features/
  posts/
    components/
      PostList.tsx
    actions/
      posts.ts
    types/
      post.ts
components/
  ui/
lib/
hooks/
```

### Shared route structure

```text
app/
  layout.tsx
  page.tsx
  globals.css
  (routes)/
    posts/
      page.tsx
      loading.tsx
      error.tsx
      [id]/
        page.tsx
components/
  ui/
lib/
hooks/
```

Do not create `app/features`, root `features`, route groups, or shared folders
merely because an example includes them. Choose colocation and sharing
boundaries from actual consumers.

## Server Component Template

```tsx
import type { Post } from '@/types/post'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

interface PostCardProps {
  post: Post
}

export function PostCard({ post }: PostCardProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{post.title}</CardTitle>
      </CardHeader>
      <CardContent>
        <p>{post.content}</p>
      </CardContent>
    </Card>
  )
}
```

## Client Component Template

```tsx
'use client'

import { useState } from 'react'

interface ExpandablePostProps {
  title: string
  content: string
}

export function ExpandablePost({
  title,
  content,
}: ExpandablePostProps) {
  const [expanded, setExpanded] = useState(false)

  return (
    <article>
      <h2>{title}</h2>
      <button
        type="button"
        aria-expanded={expanded}
        onClick={() => setExpanded((current) => !current)}
      >
        {expanded ? 'Hide details' : 'Show details'}
      </button>
      {expanded ? <p>{content}</p> : null}
    </article>
  )
}
```

For the original create-post form pattern, use the Server Action and form
guidance in [data-routing-and-states.md](data-routing-and-states.md). Keep
pending state tied to the actual action lifecycle; do not leave a manual loading
flag stuck when a redirect or exception interrupts a handler.

## Related Guidance

Use the repository's backend or API guidance for contracts consumed by the
frontend. This package does not invent backend endpoints, authentication,
database behavior, or deployment architecture.
