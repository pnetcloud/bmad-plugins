---
title: Cache Repeated Function Calls
impact: MEDIUM
impactDescription: avoid redundant computation
tags: javascript, cache, memoization, performance
---

## Cache Repeated Function Calls

Use a bounded module-level cache for a pure function when profiling shows
repeated computation with the same inputs. Include every input that affects the
result and define eviction or invalidation.

**Incorrect (redundant computation):**

```typescript
function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // slugify() called 100+ times for same project names
        const slug = slugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**Correct (cached results):**

```typescript
// Module-level cache
const slugifyCache = new Map<string, string>()
const MAX_SLUG_CACHE_ENTRIES = 256

function cachedSlugify(text: string): string {
  if (slugifyCache.has(text)) {
    return slugifyCache.get(text)!
  }
  const result = slugify(text)
  if (slugifyCache.size >= MAX_SLUG_CACHE_ENTRIES) {
    const oldestKey = slugifyCache.keys().next().value
    if (oldestKey !== undefined) slugifyCache.delete(oldestKey)
  }
  slugifyCache.set(text, result)
  return result
}

function ProjectList({ projects }: { projects: Project[] }) {
  return (
    <div>
      {projects.map(project => {
        // Computed only once per unique project name
        const slug = cachedSlugify(project.name)
        
        return <ProjectCard key={project.id} slug={slug} />
      })}
    </div>
  )
}
```

**Simpler pattern for an immutable helper:**

```typescript
let shortDateFormatter: Intl.DateTimeFormat | null = null

function formatShortDate(value: Date): string {
  if (!shortDateFormatter) {
    shortDateFormatter = new Intl.DateTimeFormat('en', {
      dateStyle: 'short'
    })
  }
  return shortDateFormatter.format(value)
}
```

Use a Map (not a hook) so it works everywhere: utilities, event handlers, not just React components.

Do not use a module cache for credentials, authorization decisions, mutable
request data, or user-scoped results unless the cache key, lifetime, isolation,
and invalidation model make cross-user reuse impossible.

Reference: [How we made the Vercel Dashboard twice as fast](https://vercel.com/blog/how-we-made-the-vercel-dashboard-twice-as-fast)
