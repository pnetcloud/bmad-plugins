# TypeScript and Performance

Use this reference for TypeScript contracts and evidence-backed frontend
performance work. Inspect compiler options, lint rules, React/Next versions,
React Compiler configuration, runtime target, and existing measurement tools.

## Contents

- [TypeScript Contract](#typescript-contract)
- [Performance Workflow](#performance-workflow)
- [Stable Optimization Patterns](#stable-optimization-patterns)
- [Image Pattern](#image-pattern)
- [Suspense Pattern](#suspense-pattern)
- [Memoization](#memoization)
- [Completion Evidence](#completion-evidence)

## TypeScript Contract

Follow the repository's configuration. Prefer:

- strict checking where the project supports it;
- explicit component prop and boundary types;
- `import type` where required by compiler or lint configuration;
- `unknown` plus validation for untrusted data;
- generated/client types at trusted integration boundaries;
- discriminated unions for meaningful UI states;
- narrow assertions only where runtime evidence establishes the invariant.

Do not impose explicit return types, interfaces over type aliases, a ban on all
`any`, JSDoc on every prop type, or one export style unless the project owns
that rule. Do reject unjustified `any` at public and untrusted boundaries.

```tsx
import type { ComponentProps } from 'react'
import { Button } from '@/components/ui/button'

interface LoadingButtonProps extends ComponentProps<typeof Button> {
  pending?: boolean
}

export function LoadingButton({
  pending = false,
  disabled,
  children,
  ...props
}: LoadingButtonProps) {
  return (
    <Button
      {...props}
      aria-disabled={pending || undefined}
      disabled={pending || disabled}
    >
      {pending ? 'Loading…' : children}
    </Button>
  )
}
```

The spread precedes the enforced state so callers cannot accidentally re-enable
a pending control.

## Performance Workflow

1. Define the user-visible symptom and affected route or interaction.
2. Capture a production-like baseline with device/network profile, cold/warm
   state, framework/runtime version, and relevant traces or metrics.
3. Identify the dominant cause: request waterfall, server work, client bundle,
   render churn, image/font delivery, cache miss, layout instability, or
   interaction latency.
4. Change one proven bottleneck while preserving loading, error, cancellation,
   ordering, freshness, authorization, and accessibility behavior.
5. Re-measure under the same conditions and report the observed delta.

Do not add optimizations merely because they appear on a checklist.

## Stable Optimization Patterns

- Keep unnecessary code out of the client graph by placing Client Component
  boundaries narrowly.
- Start independent asynchronous work concurrently; await at the latest point
  that preserves intended failure and rendering boundaries.
- Use the installed Next.js image and font integrations when they fit the
  deployment and content contract.
- Lazy-load genuinely optional client code when the loading cost and user
  experience justify the added boundary.
- Stream independent server-rendered regions with Suspense when fallbacks,
  layout stability, and error behavior are designed.
- Choose explicit cache and invalidation semantics; never trade correctness or
  authorization isolation for an unmeasured cache hit.

## Image Pattern

```tsx
import Image from 'next/image'

interface AvatarProps {
  src: string
  alt: string
}

export function Avatar({ src, alt }: AvatarProps) {
  return (
    <Image
      src={src}
      alt={alt}
      width={40}
      height={40}
      sizes="40px"
      className="rounded-full"
    />
  )
}
```

Confirm allowed remote sources, dimensions, crop behavior, priority, responsive
sizes, and whether the image is informative or decorative.

## Suspense Pattern

```tsx
import { Suspense } from 'react'
import { PostList } from '@/components/PostList'
import { PostListFallback } from '@/components/PostListFallback'

export default function Page() {
  return (
    <Suspense fallback={<PostListFallback />}>
      <PostList />
    </Suspense>
  )
}
```

Suspense does not make arbitrary asynchronous work streamable and does not
replace explicit error handling. Use framework-supported data and rendering
patterns for the installed version.

## Memoization

`useMemo`, `useCallback`, and component memoization are performance
optimizations. Add them only when at least one of these contracts exists:

- an expensive calculation is measured and dependencies are correct;
- a stable object/function identity prevents proven downstream work;
- a project API explicitly requires stable identity;
- existing intentional manual memoization must be preserved.

They do not make a value correct, stop function creation, or guarantee a faster
render. Current React Compiler configurations may automate memoization; inspect
the project before adding manual hooks. Never remove existing manual
memoization casually because its identity contract may be externally relevant.

## Completion Evidence

Report the baseline and post-change measurements, environment, trace or metric
used, user-visible effect, correctness tests, and residual uncertainty. Without
comparable evidence, describe the change as a hypothesis or structural
improvement rather than a verified performance gain.
