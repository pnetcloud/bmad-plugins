# API Contract Decisions

Use only the sections relevant to the selected protocol and change. Repository
contracts and exact installed or deployed versions take precedence.

## REST, OpenAPI, Pagination, and Compatibility

- For REST, use resource and method semantics from the applicable HTTP
  specifications. Safe and idempotent method properties affect retries, but
  method idempotence does not prove an implementation or side effect is safe.
  Define conditional requests, cache keys and `Vary`, content negotiation,
  redirects, range behavior, and retry guidance only where the use case needs
  them.
- Keep one canonical OpenAPI graph when OpenAPI is the contract. Pin the exact
  OAS and JSON Schema dialect, resolve references safely, model every
  operation's parameters, bodies, media types, success and error responses,
  security alternatives, examples, callbacks or webhooks, and validate
  generated artifacts separately from the source. Before resolving a remote
  reference, require network authority and policy-approved schemes and
  destinations; validate DNS and IP results before connection and after every
  redirect, block private, link-local, loopback, and metadata destinations
  where applicable, forward no ambient credentials, and bound redirects,
  response size, time, and graph expansion. Prefer a reviewed local or vendored
  copy when network access is unnecessary.
- Choose a pagination model from data mutation rate, ordering guarantees,
  traversal needs, count cost, and client behavior. Define a stable total order,
  tie-breaker, token opacity and scope, snapshot or drift semantics, bounds,
  invalid or expired token errors, filters and sort coupling, empty or terminal
  pages, and whether totals are exact, estimated, omitted, or
  permission-filtered. Use an authenticated cursor or an unguessable
  server-side handle, bind it to the principal, tenant, query, filter, and sort
  scope, and reject altered, replayed-across-scope, or unauthorized cursors.
- Define idempotency for mutation semantics, not merely HTTP method names. For
  retryable non-idempotent operations, specify key scope, payload binding,
  concurrency behavior, retention, replayed response, partial-failure handling,
  and conflict outcomes.
- Treat compatibility directionally. Existing accepted request sets must not
  shrink and existing emitted response sets must not expand beyond what clients
  can safely consume without a migration. Check requiredness, nullability,
  enums, constraints, ordering, status and error changes, auth scopes,
  pagination tokens, webhooks, SDKs, and tolerant-reader assumptions.
- Define one stable, documented error envelope with safe machine codes,
  actionable but non-sensitive messages, field details only when disclosure is
  authorized, retry guidance, and a bounded opaque correlation identifier.
  Never expose stack traces, queries, credentials, internal hosts or paths,
  private identifiers, or sensitive field values in public error payloads.

## GraphQL

- Distinguish input and output types, model nullability as a client contract,
  and use interfaces or unions for their semantic purpose. Deprecate fields
  with migration guidance and observed usage; do not assume adding a field,
  enum value, union member, argument, or stronger non-null constraint is
  harmless for every client or generator.
- Bound depth, breadth, aliases, list sizes, recursion, variables, resolver
  fan-out, execution time, and response size using measured resolver cost
  rather than one universal depth number. Authorize at the operation, object,
  and field boundary; prevent batching and aliases from bypassing rate or
  authorization controls. Address N+1 work with request-scoped batching or
  equivalent repository-supported mechanisms.
- Execute top-level fields of a GraphQL mutation serially in document order;
  do not incorrectly extend that guarantee to nested resolver work. Make side
  effects, conflict handling, idempotency, and partial results explicit. For
  subscriptions, define authentication renewal,
  connection and tenant limits, filtering, backpressure, ordering, resume or
  loss semantics, heartbeats, disconnect cleanup, and schema evolution.
  Federation requires ownership, key and entity lifecycle, composition checks,
  authorization propagation, rollout ordering, and partial-subgraph failure.

## Authentication, Webhooks, and Bulk Operations

- Apply the current OAuth security best practice for the chosen client and
  deployment model. Keep tokens out of URLs and logs, restrict redirect URIs,
  scopes, audience, lifetime, and refresh behavior, protect replay-sensitive
  credentials, and distinguish authentication from resource authorization.
  For JWTs, let the verifier choose an explicit algorithm allowlist and validate
  every cryptographic operation; bind issuer, verification keys, audience, and
  subject as required, validate temporal claims with bounded clock skew, and
  use mutually exclusive validation rules for distinct token types to prevent
  substitution. Never derive accepted algorithms from untrusted token headers
  or mix incompatible key uses. Define key rotation and revocation behavior.
- For webhooks, define event identity and version, tenant and subject,
  synthetic examples, signature input and key rotation, replay window,
  retries and backoff, ordering, duplication, timeout, disablement, redelivery,
  endpoint verification, payload minimization, and receiver idempotency.
  Registration and every delivery must enforce policy-approved schemes and
  destinations, revalidate DNS/IP and redirects, block private, link-local,
  loopback, and metadata destinations where applicable, forward no ambient
  credentials, and use bounded egress, time, redirects, and response size. A
  successful HTTP response is delivery evidence, not proof of downstream
  processing.
- For bulk operations, require bounded size and cost, authorization per item,
  deterministic item identity, atomic versus partial-success semantics,
  asynchronous job lifecycle where needed, cancellation, status retention,
  retry and deduplication, safe mass-delete confirmation, and recovery.

## Handoffs

- Align the implementation owner on feasibility and generated-code ownership.
- Validate consumer journeys with web, mobile, partner, or SDK owners.
- Review query and transaction implications with data owners.
- Review authentication, authorization, abuse, privacy, and webhook boundaries
  with security owners.
- Review latency, capacity, rate limits, observability, and failure behavior
  with operations owners.
- Align service boundaries and rollout ordering with architecture owners.

## Validation and Completion

1. Validate the canonical REST or GraphQL contract with repository-pinned tools
   in an already-clean isolated checkout, worktree, or temporary copy. Never
   clean, reset, overwrite, or switch the user's active tree.
2. Compare the proposed contract with the deployed baseline in both request and
   response directions. Resolve the full reference or federated graph and
   distinguish tool errors from contract findings.
3. Exercise representative success, validation, authorization, not-found,
   conflict, rate-limit, timeout, retry, pagination, concurrency, and partial
   failure cases. Add GraphQL complexity/nullability and webhook replay,
   ordering, signature, and redelivery cases when applicable.
4. When generation is in scope, inspect generated manifests, build hooks,
   plugins, macros, annotation processors, and dependencies before compiling.
   Compile in an isolated no-secret environment with bounded filesystem,
   process, and network access, then test at least one real consumer path per
   materially different consumer class. Generated output or mock success alone
   does not prove runtime compatibility.
5. Scan source, rendered documentation, examples, logs, generated artifacts,
   and publication metadata for secrets, private identifiers, internal URLs,
   personal data, unsafe executable samples, and recognizable private
   architecture. Use synthetic or composite examples.
6. If publication or rollout is authorized, verify immutable artifact and
   revision identity, gateway and backend compatibility, observability,
   consumer adoption, deprecation notice, pause criteria, rollback or forward
   repair, and the observation window. Do not claim sunset until unsupported
   traffic is resolved and the retired surface is actually unavailable.

Report the design decisions and rejected alternatives, canonical revision,
compatibility findings, auth and data boundaries, pagination/error/retry
semantics, validation and consumer evidence, publication state, warnings,
remaining risks, and owner actions.

## Primary Sources

- HTTP Semantics: <https://www.rfc-editor.org/rfc/rfc9110.html>
- HTTP Caching: <https://www.rfc-editor.org/rfc/rfc9111.html>
- OAuth 2.0 Security Best Current Practice:
  <https://www.rfc-editor.org/rfc/rfc9700.html>
- JSON Web Token Best Current Practices:
  <https://www.rfc-editor.org/rfc/rfc8725.html>
- GraphQL specification: <https://spec.graphql.org/>
- OpenAPI specification: <https://spec.openapis.org/oas/latest.html>
