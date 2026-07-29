# Data, Routing, Forms, and Route States

Use this reference for App Router data reads, mutations, forms, caching,
routing, metadata, loading UI, and error boundaries. Verify every API and
default against the installed Next.js version.

## Contents

- [Server Data Reads](#server-data-reads)
- [Server Actions and Mutations](#server-actions-and-mutations)
- [Forms](#forms)
- [App Router Structure](#app-router-structure)
- [Metadata](#metadata)
- [Loading UI and Suspense](#loading-ui-and-suspense)
- [Error Boundaries](#error-boundaries)
- [Validation Matrix](#validation-matrix)

## Server Data Reads

Prefer server-side reads when the data is needed to render a Server Component
and no client synchronization requirement exists. Do not assume every request
is cached, uncached, or deduplicated: Next.js semantics vary by version, API,
rendering mode, and explicit options.

```tsx
import { PostList } from '@/components/PostList'
import { z } from 'zod'

const postsSchema = z.array(
  z.object({
    id: z.string(),
    title: z.string(),
    content: z.string(),
  }),
)

async function getPosts(): Promise<z.infer<typeof postsSchema>> {
  const response = await fetch('https://api.example.test/posts', {
    cache: 'no-store',
  })

  if (!response.ok) {
    throw new Error(`Post request failed with status ${response.status}`)
  }

  return postsSchema.parse(await response.json())
}

export default async function PostsPage() {
  const posts = await getPosts()
  return <PostList posts={posts} />
}
```

Before adopting the example:

- choose freshness, cache, revalidation, and invalidation semantics from the
  product contract;
- inspect current official documentation for the installed framework version;
- validate untrusted response data at the boundary when its shape is not
  guaranteed by a trusted typed client;
- keep authentication material and privileged fields server-side;
- preserve independent loading and failure behavior when parallel reads do not
  share one success boundary;
- avoid accidental waterfalls by starting independent work concurrently.

## Server Actions and Mutations

A Server Action is a remotely invokable server entry point, even when it is
referenced from a Server Component. Perform authorization inside the mutation
boundary; hiding a control in the UI is not authorization. Authenticate the
actor and authorize the exact operation before changing state.

```tsx
'use server'

import { redirect } from 'next/navigation'
import { z } from 'zod'

const createPostSchema = z.object({
  submissionId: z.string().uuid(),
  title: z.string().trim().min(1).max(160),
  content: z.string().trim().min(1).max(10_000),
})

interface CreatePostState {
  issues?: Record<string, string[] | undefined>
}

export async function createPost(
  _previousState: CreatePostState,
  formData: FormData,
): Promise<CreatePostState> {
  const actor = await requireAuthenticatedActor()
  await requirePermission(actor, 'post:create')

  const parsed = createPostSchema.safeParse({
    submissionId: formData.get('submissionId'),
    title: formData.get('title'),
    content: formData.get('content'),
  })

  if (!parsed.success) {
    return { issues: parsed.error.flatten().fieldErrors }
  }

  await postsRepository.createOnce({
    actor,
    idempotencyKey: `${actor.id}:${parsed.data.submissionId}`,
    post: {
      title: parsed.data.title,
      content: parsed.data.content,
    },
  })
  redirect('/posts')
}
```

Adapt authentication, authorization, schema, repository, error, audit, and
redirect behavior to the project. `createOnce` represents a durable uniqueness
or transactional deduplication contract, not an in-memory check. Preserve one
stable submission ID across retries, scope it to the actor and operation, and
test that replay returns the original result without another write. Never log
raw sensitive form values.

## Forms

Preserve the project's established form stack:

- plain HTML form plus Server Action for a small server-owned mutation;
- React action-state or pending-state APIs when supported by the installed
  versions;
- `react-hook-form` with Zod or another approved schema library when complex
  client validation and field orchestration justify it;
- existing shadcn/ui Form wrappers only after inspecting their installed source.

Validate again on the trusted server boundary. Client validation improves
feedback but is not a security boundary. Return field-safe errors, retain user
input according to the product's privacy rules, and make pending/error/success
states observable.

When returning action state, pair the server signature with a compatible client
consumer:

```tsx
'use client'

import { useActionState } from 'react'
import { createPost } from '@/app/actions/posts'

interface CreatePostState {
  issues?: Record<string, string[] | undefined>
}

const initialCreatePostState: CreatePostState = {}

interface PostFormProps {
  submissionId: string
}

export function PostForm({ submissionId }: PostFormProps) {
  const [state, formAction, pending] = useActionState(
    createPost,
    initialCreatePostState,
  )
  const titleIssue = state.issues?.title?.[0]
  const contentIssue = state.issues?.content?.[0]
  const formIssue = state.issues?.submissionId?.length
    ? 'Unable to submit this form. Refresh and try again.'
    : undefined

  return (
    <form action={formAction}>
      <input type="hidden" name="submissionId" value={submissionId} />
      {formIssue ? <p role="alert">{formIssue}</p> : null}
      <label htmlFor="post-title">Title</label>
      <input
        id="post-title"
        name="title"
        aria-describedby={titleIssue ? 'post-title-error' : undefined}
        required
      />
      {titleIssue ? (
        <p id="post-title-error" role="alert">
          {titleIssue}
        </p>
      ) : null}
      <label htmlFor="post-content">Content</label>
      <textarea
        id="post-content"
        name="content"
        aria-describedby={contentIssue ? 'post-content-error' : undefined}
        required
      />
      {contentIssue ? (
        <p id="post-content-error" role="alert">
          {contentIssue}
        </p>
      ) : null}
      <button type="submit" disabled={pending}>
        {pending ? 'Creating…' : 'Create post'}
      </button>
    </form>
  )
}
```

Generate `submissionId` on a trusted rendering boundary with a
cryptographically strong unique value. If the installed React version does not
support this action-state API, use the project's equivalent state consumer
without dropping server validation or replay protection.

## App Router Structure

Use the existing router. Common file conventions include:

```text
app/
  posts/
    page.tsx
    loading.tsx
    error.tsx
    [id]/
      page.tsx
```

- static route: `app/posts/page.tsx`;
- nested route: `app/posts/archive/page.tsx`;
- dynamic segment: `app/posts/[id]/page.tsx`;
- route group: `app/(marketing)/about/page.tsx`.

Do not introduce route groups, parallel routes, intercepting routes, or a new
feature hierarchy unless the behavior needs them.

For the Next.js 15 App Router, dynamic route parameters are asynchronous in
documented page/layout signatures:

```tsx
import { notFound } from 'next/navigation'

interface PostPageProps {
  params: Promise<{ id: string }>
}

export default async function PostPage({ params }: PostPageProps) {
  const { id } = await params
  const post = await getPost(id)

  if (!post) {
    notFound()
  }

  return <PostDetail post={post} />
}
```

Confirm the signature against the installed version during migrations rather
than copying it into older or newer code blindly.

## Metadata

Use static metadata when values are fixed and the installed version's dynamic
metadata API when values depend on route data:

```tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Posts',
  description: 'Browse published posts',
  openGraph: {
    title: 'Posts',
    description: 'Browse published posts',
  },
}
```

Follow the product's title template, canonical URL, robots, locale, and social
preview policy. Do not invent SEO claims or expose private data in metadata.

## Loading UI and Suspense

`loading.tsx` provides route-segment loading UI through a Suspense boundary.
Choose segment-level versus nested boundaries based on which content can stream
independently. A minimal fallback:

```tsx
export default function Loading() {
  return (
    <div role="status" aria-live="polite">
      Loading posts…
    </div>
  )
}
```

Avoid full-viewport spinners when stable page structure or skeletons can reduce
layout shift. Do not announce rapidly changing decorative loaders repeatedly.

## Error Boundaries

An App Router `error.tsx` is a Client Component. It handles errors in the
covered segment's rendered subtree, not every error in the application or
necessarily errors in the same segment's layout/template. Verify the installed
version's boundary behavior and place boundaries according to the desired
recovery scope.

```tsx
'use client'

import { useEffect } from 'react'

interface ErrorProps {
  error: Error & { digest?: string }
  reset: () => void
}

export default function Error({ error, reset }: ErrorProps) {
  useEffect(() => {
    reportClientError(error)
  }, [error])

  return (
    <section aria-labelledby="route-error-title">
      <h2 id="route-error-title">Something went wrong</h2>
      <button type="button" onClick={reset}>
        Try again
      </button>
    </section>
  )
}
```

Use the project's observability client and avoid exposing sensitive exception
details. Test reset behavior and failures that occur outside the boundary.

## Validation Matrix

Exercise applicable cases:

- authenticated, unauthorized, and forbidden mutations;
- valid, invalid, duplicate, stale, and oversized form submissions;
- cache hit, miss, invalidation, and stale-data behavior;
- loading, empty, partial, error, not-found, redirect, and recovery paths;
- static, dynamic, grouped, localized, and deep-linked routes;
- direct navigation, client navigation, refresh, and browser history;
- metadata with missing, long, localized, and private source fields.
