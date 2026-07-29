---
title: Prevent Hydration Mismatch Without Flickering
impact: MEDIUM
impactDescription: avoids visual flicker and hydration errors
tags: rendering, ssr, hydration, localStorage, flicker
---

## Prevent Hydration Mismatch Without Flickering

When presentation state can be resolved on the server, render that state into
the server markup and seed the first client render with the same value. This
avoids both a hydration mismatch and a post-hydration correction.

**Incorrect (breaks SSR):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  // localStorage is not available on server - throws error
  const theme = localStorage.getItem('theme') || 'light'
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

Server-side rendering will fail because `localStorage` is undefined.

**Incorrect (visual flickering):**

```tsx
function ThemeWrapper({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState('light')
  
  useEffect(() => {
    // Runs after hydration - causes visible flash
    const stored = localStorage.getItem('theme')
    if (stored) {
      setTheme(stored)
    }
  }, [])
  
  return (
    <div className={theme}>
      {children}
    </div>
  )
}
```

Component first renders with default value (`light`), then updates after hydration, causing a visible flash of incorrect content.

**Correct (server and first client render agree):**

```tsx
type Theme = 'light' | 'dark'

function ThemeDocument({
  children,
  initialTheme,
}: {
  children: ReactNode
  initialTheme: Theme
}) {
  return (
    <html data-theme={initialTheme}>
      <body>
        {children}
      </body>
    </html>
  )
}
```

Resolve `initialTheme` from an approved server-readable preference such as an
allowlisted cookie, and pass that same value to any client-side theme state.
Validate the value before rendering it.

When browser storage is the only source, choose the tradeoff explicitly:

- update after hydration and accept a possible visual correction; or
- use the framework's documented before-hydration bootstrap and narrowly mark
  the exact known divergence according to its hydration API.

A generic inline script placed after the target element does not guarantee
ordering under streaming and can still create a mismatch when React expects the
unmodified server attributes.

**Safety and compatibility conditions:**

- Never interpolate untrusted or user-controlled values into a bootstrap.
- Satisfy Content Security Policy with the application's approved nonce, hash,
  or external bootstrap mechanism.
- Use it only for presentation state. Do not derive authentication or
  authorization decisions from browser storage or pre-hydration DOM changes.
- Verify server markup, first client output, streaming order, scripting-disabled
  behavior, blocked storage, and restrictive CSP.
