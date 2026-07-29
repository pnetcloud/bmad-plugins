# Frontend Decisions

Use only the sections relevant to the selected framework and change. Repository
contracts and exact installed framework, renderer, TypeScript, browser,
package-manager, and build-tool versions take precedence.

## Contents

- Components, state, and rendering
- Data, forms, routing, and realtime
- Accessibility, internationalization, and responsive UX
- Browser security and privacy
- Performance and build output
- Testing, handoffs, and completion
- Primary sources

## Components, State, and Rendering

- Model components around user and ownership boundaries, not arbitrary visual
  fragments. Preserve public props, events, slots/children, controlled versus
  uncontrolled behavior, defaults, null/missing semantics, focus, and
  serialization unless a migration accounts for consumers.
- Keep render or template evaluation pure. Derive values during rendering when
  possible; use effects/watchers/lifecycle hooks to synchronize with external
  systems, not as a default place for event logic or derived state. Define
  cleanup, cancellation, stale-result, dependency, replay, and remount behavior.
- Place state at the narrowest owner that must coordinate it. Distinguish
  canonical server state, URL state, persistent user preference, shared client
  state, form draft, optimistic state, and ephemeral view state. Do not create a
  second mutable authority or mirror props into state without a reset contract.
- Preserve state intentionally across routing, list reordering, conditional
  rendering, tabs, virtualization, and hydration. Use stable semantic identity
  and explicit reset behavior; array index keys or incidental DOM position are
  not identity.
- Respect the repository's server/client, SSR/SSG/CSR, streaming, hydration,
  suspense, and cache boundaries. Keep server and client output deterministic,
  avoid browser-only reads during server rendering, and test slow, partial,
  error, not-found, and hydration-mismatch paths.
- Prefer native platform behavior and the established component/design system.
  Reuse tokens and primitives when their semantics fit; do not force reuse that
  breaks behavior, accessibility, ownership, or bundle boundaries.

## Data, Forms, Routing, and Realtime

- Define request ownership, schema validation, authentication, authorization,
  freshness, cache key and scope, cancellation, timeout, retry, idempotency,
  partial response, error mapping, loading, empty, stale, and offline behavior.
  Treat external data as untrusted even when TypeScript types exist.
- Preserve URL and history semantics for shareable state. Validate route and
  query input, distinguish push from replace, prevent update loops, and test
  direct load, refresh, back/forward, duplicate tabs, unsupported values,
  redirects, and old links.
- For forms, use semantic controls and labels; define normalization, client and
  server validation ownership, field and form errors, pending and duplicate
  submission, cancellation, idempotency, focus/announcement, autofill,
  password-manager, unsaved changes, reset, and recovery behavior.
- For optimistic UI, define authoritative acknowledgement, temporary identity,
  ordering, rollback/reconciliation, duplicate/out-of-order responses,
  concurrent edits, retry, offline queue, and user-visible failure. Never show
  durable success solely because a local state update succeeded.
- For WebSocket, SSE, collaboration, notifications, or presence, define
  authentication renewal, reconnect/backoff/jitter, resume cursor, duplicate
  and out-of-order events, gap detection, snapshot reconciliation,
  backpressure, heartbeat, offline behavior, visibility/background lifecycle,
  teardown, and bounded logs. Presence is observation, not durable truth.

## Accessibility, Internationalization, and Responsive UX

- Resolve the applicable accessibility standard and conformance target. Start
  with semantic HTML, correct names/roles/values, keyboard behavior, visible
  focus, logical reading and focus order, error identification, status
  announcements, target size, text zoom/reflow, reduced motion, contrast, and
  alternatives to pointer, drag, hover, color, sound, and timing alone.
- A linter or automated audit is a bounded signal, not conformance proof. Record
  exact pages, states, viewports, browsers, assistive technologies, manual
  journeys, standard, and criteria covered; keep untested scope explicit.
- Design responsive behavior from content and task constraints, not only common
  device widths. Test narrow, wide, zoomed, reflowed, long/translated text,
  dynamic type, virtual keyboard, safe areas, orientation, pointer/keyboard,
  high contrast, print, and container embedding where supported.
- Use repository locale routing and message tooling. Preserve stable message
  identities, plural/date/number/time-zone semantics, fallback and missing-key
  behavior, bidirectional layout, truncation, search/sort collation, translated
  metadata, and server/client locale consistency. Do not concatenate
  translatable sentence fragments.

## Browser Security and Privacy

- Prevent DOM XSS with contextual escaping and safe DOM APIs. Treat HTML/Markdown
  sanitization as an explicit policy with tested allowed elements, attributes,
  protocols, CSS, links, images, embeds, and mutation behavior. Do not use
  framework escape hatches on untrusted content without that boundary.
- Define CSP, Trusted Types, script/style/image/connect/frame sources, nonce or
  hash ownership, third-party script lifecycle, subresource integrity where
  applicable, and reporting from the actual deployment. A meta tag or source
  configuration alone does not prove effective response headers.
- Keep credentials and privileged configuration out of browser bundles,
  source maps, logs, analytics, storage, URLs, and error messages. Treat
  browser storage as script-readable unless a stronger platform boundary is
  demonstrated.
- Protect state-changing requests using the deployed authentication and CSRF
  model. Validate `postMessage` origin/source/schema, iframe sandbox and
  permissions, redirect destinations, file/blob/object URLs, downloads, and
  external links. Bound uploads, previews, parsing, and resource exhaustion.
- Define analytics purpose, consent, minimization, redaction, retention,
  deletion, region, identity, and disabled behavior. Feature flags need safe
  defaults, exposure-event semantics, ownership, expiry, and compatibility;
  they are not authorization.

## Performance and Build Output

- Establish budgets from representative journeys and supported devices before
  optimizing. Measure navigation and interaction latency, rendering work,
  layout stability, resource and bundle cost, memory, long tasks, and network
  behavior in production-like builds; record device, browser, cache/network,
  data, repetitions, percentiles, revision, and trace.
- Profile before memoizing, virtualizing, splitting, preloading, or changing
  state architecture. Optimize the measured owner and verify user-visible
  benefit plus accessibility, correctness, power, memory, and maintenance cost.
- Avoid hidden request waterfalls and unbounded rendering. Start independent
  work in parallel, prioritize critical content, paginate or virtualize only
  with stable identity and accessibility, and bound images, fonts, third-party
  scripts, caches, observers, event listeners, timers, and retained DOM.
- Inspect production output for unintended modules, duplicate dependencies,
  secrets, private URLs, source maps, debug code, polyfills, incompatible
  syntax, unsafe chunks, cache/header mismatches, and route-specific regressions.
  Bundle analysis is evidence about bytes, not user-experience proof.

## Testing, Handoffs, and Completion

- Test observable contracts at the cheapest useful layer: pure state and
  formatting logic, component interaction and accessibility, integration with
  routing/data/browser APIs, and end-to-end critical journeys. Coverage is a
  diagnostic, not proof; prioritize branches, states, races, failures, and real
  browser behavior.
- Run repository-pinned format, lint, type, unit, component, integration,
  accessibility, browser/end-to-end, and production-build checks from an
  already-clean isolated checkout, worktree, or temporary copy. Never clean,
  reset, overwrite, or switch the user's active tree.
- Exercise supported browsers and representative viewport/input combinations:
  direct load, hydration, navigation/history, loading/empty/error/offline,
  auth and permissions, validation, duplicate action, race, realtime
  reconnect/gap, responsive/zoom, keyboard, assistive technology, reduced
  motion, performance, and old/new API compatibility.
- Align visual intent, tokens, responsive behavior, and interaction states with
  design owners; API and realtime contracts with backend owners; data-query
  implications with data owners; test hooks and journeys with QA owners;
  measured budgets with performance owners; CSP, content, auth, privacy, and
  dependency boundaries with security owners; build, preview, cache, rollout,
  and recovery with release owners.
- If preview or deployment is authorized, confirm active identity, exact source
  and artifact, target, access and data exposure, observation window, abort
  criteria, rollback or forward repair, and owner before remote mutation.

Report exact source/artifact revisions, changed journeys and contracts,
framework/browser matrix, validation commands and results, accessibility scope,
performance and bundle evidence, preview/deployment state, warnings, remaining
risks, and owner actions.

## Primary Sources

- React documentation: <https://react.dev/>
- Vue documentation: <https://vuejs.org/guide/>
- Angular documentation: <https://angular.dev/>
- TypeScript configuration reference: <https://www.typescriptlang.org/tsconfig/>
- Web Content Accessibility Guidelines 2.2: <https://www.w3.org/TR/WCAG22/>
- ARIA Authoring Practices Guide: <https://www.w3.org/WAI/ARIA/apg/>
- HTML Living Standard: <https://html.spec.whatwg.org/>
