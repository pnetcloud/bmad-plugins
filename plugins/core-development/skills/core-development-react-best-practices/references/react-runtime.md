# React Runtime Review

Apply this reference to React behavior. Check the installed version and official
documentation before using a recently introduced API.

## Correctness First

- Keep components and Hooks pure. Do not mutate props, state, or values produced
  during render.
- Derive values during render when possible. Use an Effect to synchronize with
  an external system, not as a default data-flow mechanism.
- Put interaction-specific work in the event that caused it. Avoid Effects that
  mirror an event and create an extra render or race.
- When next state depends on previous state, use the functional updater form.
- Preserve exhaustive dependencies. Refactor the Effect or use an appropriate
  Effect Event; do not suppress the dependency rule to force timing.
- Clean up subscriptions and async work. Test rapid changes so stale results do
  not overwrite newer state.
- Define nested components at module scope so their identity and state are not
  reset on every parent render.
- Use stable keys that represent item identity; array position is unsafe when
  items can be inserted, removed, or reordered.
- Subscribe to external mutable sources through an established
  `useSyncExternalStore` adapter rather than ad hoc reads during render.

Correctness changes may also improve performance, but report them as correctness
findings unless their cost was measured.

## Rendering and Memoization

Use React Performance tracks or the Profiler to find the slow interaction and
component. Then inspect:

- expensive work repeated with unchanged inputs;
- unstable object, array, or callback identities crossing a memoized boundary;
- overly broad context or external-store subscriptions;
- large lists without an appropriate rendering or virtualization strategy;
- synchronous updates that block an urgent interaction.

Prefer simpler component boundaries and narrower subscriptions. Add `memo`,
`useMemo`, or `useCallback` only when the measured work is meaningful and the
dependencies are correct. Memoization has comparison, allocation, and
maintenance cost; it is not semantic correctness.

If React Compiler is enabled and supported, inspect its diagnostics before
adding manual memoization. Do not enable it as an incidental optimization.

## Effects and Effect Events

In React versions that support `useEffectEvent`, use it to separate non-reactive
logic that must read the latest values from the reactive Effect lifecycle. An
Effect Event is not a general callback stabilizer and must not be used to hide a
dependency that should re-synchronize the Effect. Invoke Effect Events from
Effects or other Effect Events; do not pass them to unrelated components or
Hooks.

For older versions, a carefully maintained ref can expose the latest callback
to a stable subscription. Keep the ref update, subscription, cleanup, and event
type explicit. Prefer the project’s established helper.

## Transitions and Deferred Rendering

Use a transition for non-urgent rendering that may be interrupted while urgent
input stays responsive. Do not use one for the controlled state of a text input,
for throttling event frequency, or as a substitute for fixing slow synchronous
work. A transition does not make network requests faster.

Use `useDeferredValue` when a derived subtree may lag behind an urgent value.
Make the stale state understandable to the user and verify that the expensive
subtree can actually avoid urgent work.

`Activity` is version-dependent. Consider it when hidden UI should preserve
state and may benefit from lower-priority work. Compare it with conditional
rendering, CSS visibility, memory cost, Effects while hidden, and accessibility
behavior before adopting it. Hidden Activity children preserve state but their
Effects are cleaned up; verify the exact behavior in the installed release.

## Hydration and Browser State

Server and first client render must agree. Investigate time, locale, random
values, browser-only APIs, invalid markup, external DOM mutation, and divergent
data before suppressing a warning.

Use a two-pass client render only when the temporary server representation is
acceptable. Use `suppressHydrationWarning` only for a known, unavoidable,
single-level difference. It is an escape hatch, not a repair.

Inline scripts that read browser storage require an explicit security and
content-security-policy design. Never interpolate untrusted content into script
text. Prefer framework-supported theming or a constrained static bootstrap when
the product requires pre-hydration state.

Browser storage is synchronous, shared with page scripts, size-limited, and
externally mutable. Do not store credentials or sensitive records. Validate
schema, failure behavior, cross-tab updates, and server-render fallbacks.

## Browser Work

- Batch layout reads separately from writes when a trace shows layout thrashing.
- Use passive listeners only when the handler never calls `preventDefault`.
- For frequent events, consider browser scheduling, throttling, or a ref when
  intermediate values need not render.
- Preserve keyboard, focus, reduced-motion, and screen-reader behavior when
  changing rendering or animation.
- Use `content-visibility`, virtualization, resource hints, or preload only
  after checking support and the actual critical path.

## Primary References

- [React performance tracks](https://react.dev/reference/dev-tools/react-performance-tracks)
- [React Profiler](https://react.dev/reference/react/Profiler)
- [Removing Effect dependencies](https://react.dev/learn/removing-effect-dependencies)
- [`useEffectEvent`](https://react.dev/reference/react/useEffectEvent)
- [`startTransition`](https://react.dev/reference/react/startTransition)
- [`useDeferredValue`](https://react.dev/reference/react/useDeferredValue)
- [`Activity`](https://react.dev/reference/react/Activity)
- [`hydrateRoot`](https://react.dev/reference/react-dom/client/hydrateRoot)
- [React Compiler](https://react.dev/learn/react-compiler)
