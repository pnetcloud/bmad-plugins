# Fullstack Decisions

Use only the sections required by the active feature. Repository contracts,
installed versions, supported clients, data ownership, and deployment policy
take precedence over generic patterns.

## Contents

- Scope and invariants
- Contracts and data evolution
- Authentication, authorization, and security
- Frontend, API, and realtime integration
- Performance and observability
- Testing, delivery, and completion
- Primary sources

## Scope and Invariants

- Map the user journey and its actual layer owners before editing. Distinguish
  current behavior, requested behavior, proposed design, implemented source,
  generated artifacts, deployed state, and observed runtime.
- Resolve exact database, backend, API/schema, frontend, runtime, package,
  browser, build, and deployment versions from repository evidence. Do not
  choose a new stack merely because a checklist names one.
- Define invariants at each boundary: identity, authorization, tenant or account
  scope, schema and null semantics, ordering, time and timezone, money and
  precision, idempotency, concurrency, error mapping, privacy, and retention.
- Trace every public contract consumer: old and new browser clients, services,
  jobs, webhooks, event consumers, administrative tools, generated clients,
  caches, analytics, and externally documented integrations.
- Keep one canonical owner for each state transition. Shared types improve
  compile-time consistency but do not replace runtime validation, authorization,
  or compatibility tests.

## Contracts and Data Evolution

- Define request, response, event, and stored-data schemas with required,
  optional, nullable, omitted, default, unknown-field, error, pagination,
  ordering, and versioning behavior. Preserve wire behavior deliberately.
- Evaluate compatibility in both directions. During a compatibility window,
  deployed consumers must still be able to send their previously valid inputs,
  so do not shrink accepted request, command, or event-input sets without a
  migration. Deployed consumers may reject unfamiliar outputs, so do not expand
  emitted enum values, union variants, response shapes, or event types unless
  their tolerance is proven or rollout sequencing and versioning protect them.
- Prefer additive compatible evolution. Use an expand, backfill, validate,
  switch, and contract sequence when storage and clients cannot change
  atomically. Define mixed-version behavior before rollout.
- Assess migrations for locks, rewrite cost, transaction behavior, replication,
  backups, data volume, timeouts, retry, resumability, observability, and
  rollback or forward repair. Generating a migration is not proof it is safe to
  apply.
- Select transaction boundaries and isolation from the invariant and concurrent
  access pattern. Test lost update, duplicate action, write skew, deadlock,
  serialization failure, cancellation, and retry behavior rather than assuming
  a transaction makes the workflow correct.
- For cross-service or database-plus-message workflows, define the durable
  source of truth, commit boundary, outbox or equivalent publication strategy,
  consumer idempotency, deduplication scope, ordering, replay, poison-event
  handling, and reconciliation. Do not claim an atomic distributed outcome
  without a demonstrated protocol.
- Give mutating operations explicit retry semantics. HTTP method names alone do
  not make application behavior safely repeatable; use repository-supported
  idempotency keys, unique constraints, compare-and-set, or reconciliation when
  duplicate effects matter. Scope each idempotency key to the authenticated
  principal or tenant and operation, bind it to a canonical request
  fingerprint, and reject reuse with a different payload. Define the atomic
  claim and result record, concurrent in-flight duplicate behavior, stable
  response replay, durable retention and expiry covering the retry window, and
  recovery when processing outcome is initially ambiguous.
- Define cache ownership, key scope, identity or tenant isolation, freshness,
  invalidation trigger, stampede behavior, negative caching, and recovery after
  partial failure. A cache must not become a second ungoverned authority.
- Generate clients or shared schemas only from an authoritative contract and
  preserve generated-file ownership. Review code generation, package scripts,
  provenance, pinned integrity, network need, and resulting diffs before
  execution or publication. If execution is authorized, use a disposable
  no-secret environment with only the necessary read-only inputs and a
  dedicated output path, no ambient credentials, no network by default,
  bounded processes and resources, and no write access to the repository or
  unrelated files. Inspect the output before selectively copying owned
  artifacts; do not execute an opaque generator merely because its package name
  or generated diff appears plausible.

## Authentication, Authorization, and Security

- Use the deployed authentication model; secure cookies, bearer tokens, refresh
  tokens, SSO, and service identities are alternatives with different
  boundaries, not features to add together by default.
- If that model uses JWTs, apply distinct verifier-controlled validation rules
  for each token kind and issuer. Pin an allowed algorithm set independent of
  the token header; verify signature, issuer, audience, key binding, expiry,
  not-before, and token type; and prevent access, refresh, identity, or
  cross-issuer token substitution. Bound clock skew. For refresh-token
  rotation, define one-time use, reuse detection, family revocation, storage,
  expiry, and recovery rather than treating a signed token as sufficient.
- Enforce authorization at every trusted operation and data boundary. Frontend
  route guards and feature flags improve UX but are not authorization. Verify
  object-, action-, field-, tenant-, and administrative-level access.
- For browser sessions, define cookie scope and attributes, CSRF defense,
  rotation, renewal, logout, expiry, revocation, concurrent sessions, fixation,
  replay, and behavior across tabs and devices. Do not expose bearer material to
  browser code unless the chosen architecture requires and protects it.
- Validate untrusted input at the boundary that interprets it. Use
  context-appropriate output encoding and parameterization; bound bodies,
  uploads, decompression, parsing, redirects, outbound requests, and resource
  consumption.
- Extract archives only into a disposable root after rejecting absolute and
  traversal paths, link escapes, special files, and collisions. Enforce file
  count, nesting, per-file and total expanded size, compression-ratio, time,
  memory, and cleanup limits before materialization.
- For server-side remote fetches, allow only required schemes and destinations.
  Resolve and validate every address, deny loopback, private, link-local,
  multicast, reserved, and metadata destinations, connect through a controlled
  fetcher that cannot be redirected or rebound to a denied address, and
  revalidate every redirect. Send no ambient credentials, cookies, proxy
  credentials, or internal headers; bound redirects, response bytes, time,
  concurrency, and content processing.
- Keep credentials and privileged configuration out of client bundles, URLs,
  logs, traces, analytics, error responses, generated artifacts, and fixtures.
  Redact sensitive fields while retaining enough correlation for diagnosis.
- Resolve CORS, CSP, transport security, proxy trust, host and origin handling,
  security headers, rate limits, abuse controls, and error disclosure from the
  deployed topology. Source configuration alone does not prove effective
  runtime policy.
- When database row security or policy enforcement is used, verify effective
  identities, connection pooling, bypass roles, background jobs, migrations,
  administrative paths, prepared statements, and failure behavior. Keep service
  authorization as defense in depth.
- Test an identity matrix across unauthenticated, ordinary, privileged,
  cross-tenant, stale-session, revoked, and malformed cases. Do not infer
  security verification from happy-path tests or a scanner score.

## Frontend, API, and Realtime Integration

- Model loading, empty, partial, stale, error, retry, offline, permission,
  duplicate-action, cancellation, and recovery states across the entire
  journey. Preserve accessible focus and announcements when state changes.
- Validate API responses at runtime when trust or compatibility requires it.
  Map transport, validation, authentication, authorization, conflict,
  unavailable, and unexpected failures into stable client behavior without
  leaking internals.
- For optimistic UI, define temporary identity, authoritative acknowledgement,
  ordering, rollback, conflict resolution, duplicate and out-of-order response
  handling, retry, and navigation lifecycle. A local update is not durable
  success.
- Preserve URL and history semantics, direct links, refresh, old bookmarks, and
  server/client rendering behavior when backend contracts change.
- For WebSocket, SSE, notifications, collaboration, or presence, define
  authentication renewal, reconnect and backoff, resume cursor, duplicate and
  out-of-order events, gap detection, snapshot reconciliation, backpressure,
  heartbeat, background lifecycle, teardown, and bounded logging.
- Keep event and request schema evolution compatible with deployed consumers.
  Verify mixed versions and recovery from partial rollout, not only a
  simultaneous local build.

## Performance and Observability

- Set budgets for representative user journeys and supported environments.
  Measure database plans and lock behavior, backend latency and resource cost,
  network payloads and waterfalls, frontend rendering and interaction, bundle
  cost, memory, and background work under controlled conditions.
- Optimize the measured owner. Record revision, build, data shape, concurrency,
  cache state, browser or client, hardware, network, repetitions, percentile,
  trace, and correctness checks. One faster layer can still make the journey
  slower or less reliable.
- Propagate bounded correlation across request, job, event, and client
  boundaries without exposing secrets or personal data. Define logs, metrics,
  traces, audit events, cardinality, sampling, retention, alerts, dashboards,
  and ownership from actual operational needs.
- Distinguish successful request processing from durable completion. Observe
  asynchronous work, event publication, consumer progress, data convergence,
  client refresh, and user-visible outcome when those are part of the feature.

## Testing, Delivery, and Completion

- Test the cheapest observable contract at each layer, then exercise the
  cross-layer journey with real serialization, persistence, auth, browser or
  client behavior, background work, and failure paths where required.
- Cover schema compatibility, migration up and recovery, concurrency,
  idempotency, authorization matrix, validation, error mapping, cache behavior,
  realtime reconnect and gaps, responsive and accessible UI states,
  observability, rollout, and old/new version coexistence.
- Use repository-pinned tools from an already-clean isolated checkout,
  worktree, or temporary copy. Never clean, reset, overwrite, or switch the
  user's active tree to obtain a passing run.
- Require explicit authority and active identity before dependency changes,
  migration application, remote data mutation, preview publication,
  infrastructure changes, deployment, traffic switching, cache invalidation,
  rollback, or production observation that may expose sensitive data.
- For rollout, identify exact source and artifact, target, preconditions,
  compatibility window, feature-flag semantics, data exposure, observation
  window, abort criteria, rollback or forward repair, and owner. Feature flags
  are rollout controls, not authorization.
- Report source edit, generated artifact, static checks, tests, build,
  migration generation, migration application, runtime observation, browser
  journey, performance measurement, preview, deployment, and healthy release as
  separate evidence states.

Completion requires the changed journey and contracts, exact revisions,
commands and results, migration and compatibility state, security and
performance scope, runtime and client observations, rollout state, warnings,
unknowns, remaining risks, and owner actions. Never infer production readiness
from a local build, passing tests, generated migration, or deployment command.

## Primary Sources

- OWASP Application Security Verification Standard 5.0.0:
  <https://owasp.org/www-project-application-security-verification-standard/>
- OWASP Session Management Cheat Sheet:
  <https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html>
- OWASP REST Security Cheat Sheet:
  <https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html>
- JSON Web Token Best Current Practices, RFC 8725:
  <https://www.rfc-editor.org/rfc/rfc8725>
- HTTP Semantics, RFC 9110: <https://www.rfc-editor.org/rfc/rfc9110>
- PostgreSQL current transaction isolation:
  <https://www.postgresql.org/docs/current/transaction-iso.html>
- React documentation: <https://react.dev/>
- Web Content Accessibility Guidelines 2.2:
  <https://www.w3.org/TR/WCAG22/>
