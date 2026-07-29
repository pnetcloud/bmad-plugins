---
title: Cache Storage API Calls
impact: LOW-MEDIUM
impactDescription: reduces expensive I/O
tags: javascript, localStorage, storage, caching, performance
---

## Cache Storage API Calls

`localStorage`, `sessionStorage`, and `document.cookie` are synchronous and expensive. Cache reads in memory.

**Incorrect (reads storage on every call):**

```typescript
function getTheme() {
  return localStorage.getItem('theme') ?? 'light'
}
// Called 10 times = 10 storage reads
```

**Correct (Map cache):**

```typescript
const storageCache = new Map<string, string | null>()

function getLocalStorage(key: string) {
  if (!storageCache.has(key)) {
    storageCache.set(key, localStorage.getItem(key))
  }
  return storageCache.get(key)
}

function setLocalStorage(key: string, value: string) {
  localStorage.setItem(key, value)
  storageCache.set(key, value)  // keep cache in sync
}
```

Use a Map (not a hook) so it works everywhere: utilities, event handlers, not just React components.

**Safely scoped cookie-read cache:**

Cache only explicitly allowlisted, non-sensitive presentation preferences when
profiling proves repeated cookie parsing matters:

```typescript
const NON_SENSITIVE_COOKIE_KEYS = new Set(['ui-density'])
const preferenceCookieCache = new Map<string, string | null>()

function getCachedPreferenceCookie(name: string) {
  if (!NON_SENSITIVE_COOKIE_KEYS.has(name)) return null
  if (preferenceCookieCache.has(name)) {
    return preferenceCookieCache.get(name) ?? null
  }

  const prefix = `${encodeURIComponent(name)}=`
  const match = document.cookie
    .split('; ')
    .find(cookie => cookie.startsWith(prefix))
  let value: string | null = null
  try {
    value = match ? decodeURIComponent(match.slice(prefix.length)) : null
  } catch {
    value = null
  }
  preferenceCookieCache.set(name, value)
  return value
}

function invalidatePreferenceCookie(name: string) {
  preferenceCookieCache.delete(name)
}
```

Invalidate on every application-owned write and when the document becomes
visible again if the server or another tab may change the cookie. Never use this
cache for session, authentication, authorization, CSRF, consent, account,
tenant, or other security-relevant state. Prefer server-owned session checks
and an application-owned state source when correctness matters more than the
measured parsing cost.

**Important (invalidate on external changes):**

If storage can change externally (another tab, server-set cookies), invalidate cache:

```typescript
window.addEventListener('storage', (e) => {
  if (e.key) storageCache.delete(e.key)
})

document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    storageCache.clear()
    preferenceCookieCache.clear()
  }
})
```

Bound the cache and minimize stored values. Clear relevant entries on logout,
tenant or account changes, schema migration, and permission changes.
