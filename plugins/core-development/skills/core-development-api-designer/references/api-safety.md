# API safety design gates

Use only the sections relevant to the interface being designed. Record
not-applicable decisions rather than adding controls mechanically.

- [Specification and trust boundaries](#specification-and-trust-boundaries)
- [OAuth, tokens, and credentials](#oauth-tokens-and-credentials)
- [Protocol-neutral authentication](#protocol-neutral-authentication)
- [Mutations, idempotency, and retries](#mutations-idempotency-and-retries)
- [Pagination and consistency](#pagination-and-consistency)
- [Webhooks and outbound destinations](#webhooks-and-outbound-destinations)
- [Error and lifecycle contracts](#error-and-lifecycle-contracts)
- [Minimum review scenarios](#minimum-review-scenarios)
- [Primary sources](#primary-sources)

## Specification and trust boundaries

- Select and pin a published OpenAPI version supported by the required
  validators and generators. Do not label an older minor as the latest. Resolve
  and inspect external references under explicit network, size, cycle, and
  trusted-origin limits; sanitize rendered Markdown or HTML.
- Identify principals, resources, operations, fields, tenants, trust zones,
  sensitive data, and externally supplied URLs. Model authentication and
  authorization separately.
- Require deny-by-default authorization at object, field/property, function,
  and tenant boundaries. Specify ownership and relationship checks for every
  client-supplied resource identifier; do not rely on an unguessable ID.
- Bound request and response sizes, nesting, query complexity, fan-out,
  concurrency, execution time, result count, and cost. Define rejection and
  observability behavior without exposing sensitive internals.

## OAuth, tokens, and credentials

- Select flows from the current OAuth security best current practice.
  Authorization servers must support PKCE and prevent downgrade. Redirect-based
  public clients must use authorization code with transaction-bound PKCE
  (`S256`); confidential clients should use it, with only the documented
  OpenID Connect `nonce` alternative. Require issuer validation and CSRF/mix-up
  defenses. Match redirect URIs exactly except for the standards exception that
  permits a dynamically assigned port on a native app's loopback redirect; keep
  the rest of the URI fixed.
- Do not use the resource-owner password credentials grant. Prefer code-based
  flows over the implicit grant; allow an exceptional implicit flow only when
  the design records why code flow is unsuitable and demonstrates prevention
  of access-token injection plus mitigation of the specified leakage vectors.
- Define client type, token audience, least-privilege scopes, sender
  constraints where applicable, expiration, revocation, and storage. If public
  clients receive refresh tokens, require rotation or sender constraint and
  replay handling.
- Treat JWT as a token format, not an authentication scheme. Pin allowed
  algorithms and issuer/audience/key rules; reject algorithm substitution,
  unsafe key lookup, and expired or not-yet-valid tokens. Never place secrets
  or unnecessary personal data in client-readable token claims.

## Protocol-neutral authentication

- State whether a mechanism authenticates a person, service, client
  application, or project. API keys usually identify callers, not end users;
  scope, rotate, revoke, and store them safely, keep them out of URLs and logs,
  and never substitute them for per-user authorization.
- For cookie sessions, define secure, HTTP-only, same-site attributes, CSRF
  protection, fixation prevention and post-authentication rotation, idle and
  absolute expiry, logout and server-side revocation, and concurrent-session
  policy.
- For passwords and recovery, use approved salted password hashing, generic
  non-enumerating responses, single-use expiring recovery artifacts, protected
  delivery, and notification of security-relevant changes. Recovery must not
  be materially weaker than primary authentication. Define adequate length for
  the authenticator context, allow long passphrases and password-manager input,
  reject common or known-compromised values, avoid arbitrary composition
  rules, and require rotation on compromise or an explicit governing policy
  rather than by default on a short periodic schedule.
- Bound login, recovery, token, and verification attempts using signals
  proportionate to risk; detect credential stuffing without making account
  lockout an easy denial-of-service primitive. Define monitoring, escalation,
  and safe client feedback.
- Require recent or stronger reauthentication for sensitive operations, and
  define MFA or phishing-resistant authentication where the threat model needs
  it. Authentication success never replaces object, field, function, or tenant
  authorization.

## Mutations, idempotency, and retries

- For retried or financially/materially significant mutations, define an
  idempotency key contract: principal and operation scope, request fingerprint,
  concurrent-duplicate behavior, storage duration, replayed response, and
  conflict response. Do not treat HTTP method names alone as proof of
  idempotent implementation.
- Publish retry guidance only for safe or idempotency-protected operations.
  Specify retryable statuses, `Retry-After` handling, exponential backoff with
  jitter, maximum attempts or elapsed time, and cancellation. Prevent retry
  storms and duplicated side effects.
- For bulk create, update, or delete, require an explicit bounded selector,
  per-item authorization, maximum batch size, dry-run or preview for destructive
  work, atomicity or partial-success semantics, idempotency, auditability, and
  a resumable asynchronous job when synchronous limits would be unsafe.

## Pagination and consistency

- Define a deterministic total order with a stable tie-breaker. Document how
  inserts, updates, and deletes affect traversal and whether the API offers
  snapshot, eventual, or live-list semantics.
- Treat cursors as opaque and integrity-protected when they carry state. Bind
  them to the relevant principal, filters, sort, page-size policy, and expiry;
  reject mismatches rather than silently changing the query.
- Cap page size and query cost. State whether totals are exact, approximate,
  omitted, or scoped to a snapshot; never promise a cheap exact total without
  an implementation basis.

## Webhooks and outbound destinations

- Define event ID, schema version, subject, occurrence time, ordering scope,
  duplicate behavior, and compatibility policy. Receivers must be able to
  deduplicate; do not promise exactly-once delivery across a network boundary.
- Sign the raw delivered bytes with a timestamped, versioned scheme; define
  replay tolerance, constant-time verification, secret rotation, and failure
  behavior. Do not put webhook secrets in query strings or example payloads.
- Bound retry duration and attempts with backoff and jitter; define terminal
  failure, dead-letter or operator-visible state, safe manual replay, and
  subscription disablement.
- For user-supplied destinations, require HTTPS policy, normalized validation,
  DNS/IP re-checks, redirect limits, blocked internal and metadata ranges,
  egress controls, response-size/time limits, and safe verification to reduce
  SSRF and resource-exhaustion risk.

## Error and lifecycle contracts

- Use stable machine-readable error codes, a correlation identifier, and safe
  user guidance. Do not expose stack traces, queries, credentials, tokens,
  internal topology, or cross-tenant existence through errors or timing.
- Version and deprecate with an inventory of affected clients, compatibility
  tests, notice and support windows, migration guidance, observable usage, and
  an accountable sunset decision. A header or URI version alone is not a
  migration policy.

## Minimum review scenarios

- Same identifier under another principal or tenant is denied without leaking
  existence.
- Duplicate and concurrent mutations do not duplicate effects.
- Cursor reuse with changed filters, sort, principal, or expiry fails safely.
- Bulk partial failure, cancellation, retry, and destructive preview follow the
  documented contract.
- Webhook signature rotation, replay, duplicates, reordering, receiver outage,
  redirect, and internal-address destination fail safely.
- Limits hold for oversized payloads, deep GraphQL queries, expensive filters,
  high fan-out, and slow downstream dependencies.

## Primary sources

- OpenAPI Specification, latest published version:
  <https://spec.openapis.org/oas/latest.html>
- OAuth 2.0 Security Best Current Practice, RFC 9700:
  <https://www.rfc-editor.org/rfc/rfc9700.html>
- OWASP API Security Top 10, 2023:
  <https://owasp.org/API-Security/editions/2023/en/0x10-api-security-risks/>
- NIST SP 800-63B, Digital Identity Guidelines:
  <https://pages.nist.gov/800-63-4/sp800-63b.html>
