---
title: Use Activity Component for Show/Hide
impact: MEDIUM
impactDescription: preserves state/DOM
tags: rendering, activity, visibility, state-preservation
---

## Use Activity Component for Show/Hide

Use React's `<Activity>` to preserve state for components that frequently toggle
visibility when the project runs a React version that provides it. Hidden
Activity boundaries hide content, clean up Effects, and may continue
lower-priority rendering; they are not a promise of zero background work.
Verify availability and lifecycle behavior in the current official documentation.

**Usage:**

```tsx
import { Activity } from 'react'

function Dropdown({ isOpen }: Props) {
  return (
    <Activity mode={isOpen ? 'visible' : 'hidden'}>
      <ExpensiveMenu />
    </Activity>
  )
}
```

Use this when preserved state and background preparation justify the retained
tree. Measure the tradeoff against unmounting or ordinary conditional rendering.
