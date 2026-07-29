# Components and Styling

Use this reference when a task changes a React component, a Server/Client
boundary, project UI primitives, Tailwind classes, or interaction behavior.
First inspect the installed versions, existing component patterns, and design
system. The examples are synthetic and must be adapted.

## Contents

- [Component Boundary Checklist](#component-boundary-checklist)
- [Server Component Pattern](#server-component-pattern)
- [Client Component Pattern](#client-component-pattern)
- [shadcn/ui](#shadcnui)
- [Tailwind CSS and Conditional Classes](#tailwind-css-and-conditional-classes)
- [Interaction and Accessibility Review](#interaction-and-accessibility-review)

## Component Boundary Checklist

- Default to a Server Component in App Router when the component needs no
  state, effects, event handlers, context, or browser-only API.
- Add `'use client'` at the top of the smallest module that owns client-only
  behavior. Its transitive imports join the client graph.
- Keep privileged data access and secrets in server-only modules. Pass only
  intended, serializable props into Client Components.
- Avoid duplicating server-fetched data with an unconditional client
  `useEffect`; choose the project's established client cache when client-side
  refresh or synchronization is genuinely required.
- Define prop types and preserve existing export style and naming.
- Reuse the project's UI primitives before adding a parallel abstraction.
- Implement applicable pending, disabled, empty, error, keyboard, pointer,
  reduced-motion, and responsive states.
- Confirm runtime behavior before claiming hydration, focus, layout, or
  accessibility success.

## Server Component Pattern

```tsx
import type { Post } from '@/types/post'
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'

interface PostListProps {
  posts: readonly Post[]
}

export function PostList({ posts }: PostListProps) {
  return (
    <div className="grid gap-4">
      {posts.map((post) => (
        <Card key={post.id}>
          <CardHeader>
            <CardTitle>{post.title}</CardTitle>
          </CardHeader>
          <CardContent>{post.content}</CardContent>
        </Card>
      ))}
    </div>
  )
}
```

This example assumes the project owns the shown aliases and UI files. Otherwise
use its actual import paths and primitives.

## Client Component Pattern

```tsx
'use client'

import { useState } from 'react'

interface PostFormFieldsProps {
  action: (formData: FormData) => void | Promise<void>
}

export function PostFormFields({ action }: PostFormFieldsProps) {
  const [title, setTitle] = useState('')

  return (
    <form action={action}>
      <label htmlFor="post-title">Title</label>
      <input
        id="post-title"
        name="title"
        value={title}
        onChange={(event) => setTitle(event.target.value)}
        required
      />
      <button type="submit">Create post</button>
    </form>
  )
}
```

The client component owns only local interaction. The server action supplied by
the parent still validates, authenticates, and authorizes the mutation.

## shadcn/ui

Use shadcn/ui guidance only when the repository has adopted it. Inspect
`components.json`, the installed component source, and the project's wrapper
components before assuming:

- the UI directory or import alias;
- the selected style, base color, icon library, or Tailwind setup;
- whether a primitive has been customized;
- its semantic, keyboard, focus, validation, or screen-reader behavior.

shadcn/ui copies source into the project; the project owns that code and may
modify it. Preserve intentional local changes. Do not follow the obsolete rule
that generated UI source must never be edited.

A primitive can provide a strong accessibility foundation, but composition and
customization can still break names, roles, states, focus order, contrast, or
keyboard behavior. Test the resulting interaction.

## Tailwind CSS and Conditional Classes

Use Tailwind utilities only when the project has adopted Tailwind. Follow its
installed major version, tokens, class ordering, merge utility, and lint rules.
If the project uses `cn()`, preserve its actual import path and semantics:

```tsx
import { cn } from '@/lib/utils'

interface ButtonProps {
  variant?: 'primary' | 'secondary'
  className?: string
}

export function Button({
  variant = 'primary',
  className,
}: ButtonProps) {
  return (
    <button
      className={cn(
        'rounded-md px-4 py-2',
        variant === 'primary' && 'bg-primary text-primary-foreground',
        variant === 'secondary' && 'bg-secondary text-secondary-foreground',
        className,
      )}
    >
      Continue
    </button>
  )
}
```

Do not introduce a conditional-class dependency merely to reproduce this
example. Plain template expressions, CSS Modules, CSS-in-JS, or another project
utility may be the established choice.

## Interaction and Accessibility Review

For each interactive component, trace:

1. semantic element, accessible name, role, and state;
2. keyboard entry, operation, focus visibility, escape, and return behavior;
3. pointer and touch target behavior;
4. disabled versus pending semantics and duplicate-submission handling;
5. error association, status announcements, and recovery;
6. zoom, reflow, long content, localization, and reduced motion;
7. server-rendered markup and hydrated behavior.

Static source can establish some defects but not computed contrast, layout,
focus order, assistive-technology behavior, or device behavior. Report those as
manual checks unless runtime evidence was collected.
