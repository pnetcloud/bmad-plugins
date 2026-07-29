---
title: Cross-Request LRU Caching
impact: HIGH
impactDescription: caches across requests
tags: server, cache, lru, cross-request
---

## Cross-Request LRU Caching

`React.cache()` is request-scoped. For reusable, non-sensitive data that may be
shared across requests in one process, consider a bounded LRU cache after
defining freshness and invalidation.

**Implementation:**

```typescript
import { LRUCache } from 'lru-cache'

const cache = new LRUCache<string, PublicItem>({
  max: 1000,
  ttl: 5 * 60 * 1000
})

export async function getPublicItem(id: string) {
  const cached = cache.get(id)
  if (cached) return cached

  const item = await loadPublicItem(id)
  cache.set(id, item)
  return item
}

// A later request handled by this process may reuse the item.
```

Use only when stale data for the chosen TTL is acceptable. Include tenant,
locale, authorization scope, and representation version in the key whenever
they affect the result. Do not put credentials, authorization decisions, or
unbounded user-specific data in a shared process cache.

**With Vercel's [Fluid Compute](https://vercel.com/docs/fluid-compute):** LRU caching is especially effective because multiple concurrent requests can share the same function instance and cache. This means the cache persists across requests without needing external storage like Redis.

**In serverless runtimes:** A warm instance may serve multiple sequential
requests, but instance reuse and affinity are not guaranteed. Module state can
therefore persist across requests on one instance while being absent on another.
Use a shared cache only when the application requires cross-instance coherence.

Process-local caches are opportunistic: multiple instances do not share entries
and a restart clears them. Measure hit rate and memory, cap entry size, define
invalidation, and test stale and cross-scope behavior before relying on one.

Reference: [https://github.com/isaacs/node-lru-cache](https://github.com/isaacs/node-lru-cache)
