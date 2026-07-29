# GraphQL Decisions

Use only the sections required by the active task. Repository behavior, the
installed GraphQL and federation versions, supported clients, data ownership,
and deployment policy take precedence over generic examples.

## Contents

- Scope and evidence
- Schema and operation contracts
- Resolvers, data access, and performance
- Federation
- Authorization and resource safety
- Subscriptions and live delivery
- Clients, evolution, and rollout
- Testing and completion
- Primary sources

## Scope and Evidence

- Map the graph's actual owners: schema sources, resolvers, backing services,
  router or gateway, operation clients, generated artifacts, registry,
  subscriptions, and deployment targets. Separate current behavior, proposal,
  source edits, generated output, local checks, runtime observations, published
  schema, deployed artifact, and healthy release.
- Resolve exact implementation and protocol versions from manifests, lockfiles,
  schema links, generated headers, runtime configuration, and supported clients.
  Do not assume one GraphQL library, federation version, WebSocket protocol, or
  HTTP draft.
- Trace the affected field from operation through authorization, resolver,
  batching or cache, data source, serialization, client interpretation, and
  observability. Define ownership and invariants at every trust boundary.
- Preserve public schema, operation semantics, error and null behavior, stable
  identifiers, pagination, authorization, events, and mixed-version clients
  unless an approved migration accounts for each consumer.

## Schema and Operation Contracts

- Model domain capabilities rather than storage tables or service internals.
  Give each field one semantic owner. Use objects, interfaces, unions, enums,
  input objects, directives, and custom scalars only when their wire behavior
  and consumer value are explicit.
- Define output nullability from real failure and absence semantics. A non-null
  field error propagates to a nullable ancestor and can erase otherwise useful
  partial data; do not tighten output nullability until runtime data and every
  resolver path satisfy the invariant. Clients must handle the documented
  combination of `data`, field nulls, and `errors`.
- Define input omission, explicit null, defaults, unknown fields, coercion,
  validation, and error semantics separately. Adding a required input field,
  narrowing an accepted scalar or enum set, or changing omission behavior can
  invalidate deployed operations.
- Allow recursive output types and recursive input objects when a nullable or
  list boundary breaks the input cycle. Reject an unbroken cycle formed only by
  singular non-null input-object fields, as required by GraphQL schema
  validation. Diagnose resolver, module, or schema-file import cycles
  separately; type recursion alone is not a dependency defect.
- Treat schema compatibility directionally. Adding a selectable output field is
  normally non-breaking, but adding an emitted enum value or new concrete union
  or interface member can break exhaustive generated clients. Removing or
  renaming types, fields, arguments, enum values, or directives; changing type
  shape; making an input stricter; or changing defaults requires consumer
  evidence and migration sequencing.
- Design mutations around one business intent and stable outcome. Define
  authorization, validation, transaction boundary, idempotency and retry,
  concurrency conflict, partial failure, client mutation identifier when used,
  and user-safe structured errors. A GraphQL mutation is not automatically
  atomic or safely repeatable. When using an idempotency key, scope it to the
  authenticated principal or tenant and mutation, bind it to a canonical
  operation and variables fingerprint, and reject reuse with different input.
  Define atomic in-flight ownership, concurrent duplicate behavior, stable
  result replay, durable retention and expiry covering the retry window, and
  recovery when the first outcome is ambiguous.
- For lists, define deterministic ordering, maximum and default page sizes,
  filters, authorization, cursor opacity and stability, snapshot or live
  semantics, empty and deleted items, and navigation under concurrent writes.
  Avoid unbounded list fields. Protect cursor integrity with an authenticated
  encoding or unpredictable server-side handle bound to the principal or
  tenant, operation or field, filters, sort, and relevant snapshot or version.
  Reject altered, expired, or cross-scope cursors without leaking cursor
  contents.
- Keep transport behavior explicit and versioned: supported methods and media
  types, operation selection, variables, status handling, partial responses,
  caching, upload behavior, and intermediary expectations. The GraphQL-over-HTTP
  specification is still a draft; do not silently replace an established wire
  contract with draft recommendations.
- Document stable public error codes and recovery behavior without exposing
  stack traces, queries, internal service names, storage details, or sensitive
  values. Preserve the GraphQL error `path` and correlation only where safe and
  useful.

## Resolvers, Data Access, and Performance

- Keep resolvers thin around domain owners. Validate returned values at trust
  boundaries, propagate cancellation and deadlines, bound retries, and avoid
  hidden writes in query fields unless the documented contract requires them.
- Treat N+1 as an observed execution pattern, not an SDL-only property. Measure
  resolver and data-source call counts for representative operations, including
  aliases, fragments, nested lists, federation hops, errors, and authorization
  filtering.
- Scope batching and memoization to the request or an equivalently safe
  isolation boundary. Batch keys must include every identity, tenant, locale,
  version, and authorization dimension that affects the result; preserve input
  order and duplicate keys. A global DataLoader can leak data or serve stale
  authorization decisions.
- Define cache owner, key, authorization scope, freshness, invalidation,
  negative caching, stampede control, partial-error behavior, and recovery.
  GraphQL response, field, router, CDN, and backing-service caches have
  different identities and invalidation boundaries.
- Cost controls must model actual work. Account for field weights, list
  cardinality and pagination arguments, aliases, fragments, repeated selections,
  recursion, batching, federation fan-out, deferred or streamed work when
  supported, and data-source cost. Depth alone is not a sufficient budget.
- Apply bounds before execution and again at expensive downstream boundaries:
  request and variable sizes, document parsing and validation, operation count,
  aliases, batch size, depth, calculated cost, resolver concurrency, time,
  response size, memory, and subscription count. Propagate cancellation.
- Persisted operations or allowlists are an optional contract, not proof of
  authorization or low cost. Define registration authority, exact hash and
  canonicalization, cache poisoning resistance, unknown-hash behavior, rollout,
  old-client compatibility, and emergency revocation.

## Federation

- Federate only when independent domain ownership and delivery justify the
  operational cost. Preserve a monolithic graph when it is the simpler
  established boundary.
- Assign every field and entity transition an accountable subgraph owner.
  Choose entity keys that are stable, globally unambiguous in their scope,
  available without forbidden data exposure, and resolvable under partial
  failure. Do not use an implementation detail merely because it is unique
  today.
- Verify reference resolvers, key variants, shared value types, interface or
  union membership, directives, overrides, required fields, and error/null
  propagation against the installed federation specification. Do not paste
  directives from a newer version into an older router.
- Run local subgraph validation and full composition with the pinned production
  toolchain. Inspect representative query plans, hop count, fan-out,
  authorization context propagation, entity fetch cardinality, cache behavior,
  and failure isolation; composition success alone does not prove an efficient
  or secure graph.
- Evolve subgraph and router versions through an explicit compatibility window.
  Identify publish order, old and new supergraph behavior, traffic observation,
  abort criteria, rollback or forward repair, and the owner of every coordinated
  schema change.

## Authorization and Resource Safety

- Authenticate at the trusted transport boundary and authorize the actual
  object, field, action, and tenant at each resolver or domain boundary.
  Root-field checks, hidden UI fields, directives, introspection settings, and
  operation allowlists do not replace object-level authorization.
- Ensure authorization survives edges and direct node lookup, aliases,
  fragments, batches, entity references, caches, subscriptions, internal
  subgraph calls, administrative paths, and partial failures. New fields should
  fail closed until their policy is explicit.
- Treat directives as metadata unless runtime enforcement and coverage are
  proven. Verify that router and subgraph identities cannot bypass each other's
  policy and that trusted context cannot be forged by client headers.
- Validate variables, custom scalars, uploaded content, and downstream
  parameters at the interpreting boundary. Parameterize data access and bound
  decompression, parsing, redirects, and outbound fetches where resolvers
  perform them.
- Rate-limit and meter by authenticated identity, tenant, operation, and actual
  cost where possible. Bound batched requests and aliases so one transport
  request cannot bypass per-operation or per-object abuse controls.
- Decide introspection and interactive tooling exposure from the threat model
  and environment. Disabling introspection is defense in depth, not a substitute
  for authorization, cost controls, safe errors, or removal of private fields.
- Exclude credentials, tokens, personal values, raw variables, and sensitive
  resolver results from logs, traces, operation registries, generated artifacts,
  examples, and fixtures. Bound operation-name and field-path cardinality.

## Subscriptions and Live Delivery

- Use subscriptions only when the user journey needs server-pushed updates and
  the deployed transport and operational ownership support them. Record the
  exact protocol, connection lifecycle, capacity, and fallback.
- Authenticate connection establishment and authorize the subscription's
  object, field, filter, and tenant. Define token expiry and renewal, revocation,
  permission changes, and per-event revalidation where stale authorization
  would expose data.
- Define event source of truth, publication commit boundary, filtering,
  ordering, duplicates, gaps, replay or resume cursor, snapshot reconciliation,
  backpressure, slow consumers, reconnect and jitter, heartbeat, teardown,
  background clients, and bounded telemetry.
- Version event payloads and GraphQL subscription selection semantics for mixed
  clients. A successful connection or delivered event is not proof that durable
  state and client state converged.

## Clients, Evolution, and Rollout

- Inventory actual operations, fragments, generated clients, normalized-cache
  keys, optimistic updates, offline behavior, and supported client versions.
  Usage telemetry is evidence, not proof that an operation is safe to remove;
  account for infrequent, offline, external, and uninstrumented consumers.
- Define stable entity identity and `__typename` behavior for normalized caches.
  Coordinate field moves, entity-key changes, pagination policies, error/null
  semantics, and optimistic responses with cache migration and rollback.
- Deprecate with a reason, replacement, owner, observation period, consumer
  migration, and removal gate. Validate stored or persisted operations and
  generated code against both sides of the compatibility window.
- Generate code only from an authoritative schema with the repository-pinned
  toolchain. Verify provenance and integrity and inspect package scripts,
  plugins, configuration, network need, and expected outputs. If execution is
  explicitly authorized, use a disposable no-secret environment with only
  minimal read-only inputs, a dedicated writable output directory, no
  repository or unrelated-path writes, no network by default, and bounded
  processes, time, memory, and disk. Reject execution when these controls cannot
  be established; inspect outputs before selectively accepting owned artifacts.
- Publish schemas, update registries, change routers, and deploy only with
  explicit authority, verified active identity, exact artifact and target,
  compatibility evidence, observation and abort criteria, and rollback or
  forward repair.

## Testing and Completion

- Test schema validity, operation validation, resolver and data-source behavior,
  null bubbling and partial errors, inputs and custom scalars, mutation
  concurrency and retry, pagination, authorization matrix, cost and abuse
  limits, batching and cache isolation, composition, query plans, subscriptions,
  generated clients, and old/new version coexistence as applicable.
- Use repository-pinned tools in an already-clean isolated checkout, worktree,
  or temporary copy. Never clean, reset, overwrite, or switch the user's active
  tree for a passing run.
- Measure representative operations under controlled data shape, identity,
  concurrency, cache state, router and subgraph revisions, and network
  conditions. Report percentiles, call counts, cost decisions, errors, resource
  use, correctness, and the exact evidence source.
- Report schema source edit, generated artifact, validation, composition,
  resolver tests, client contract tests, performance, runtime observation,
  publication, deployment, and healthy-release state separately. Never infer
  production readiness, coverage, latency, federation scale, or delivery from a
  template or an unobserved command.

## Primary Sources

- GraphQL specification: <https://spec.graphql.org/>
- GraphQL over HTTP working draft:
  <https://graphql.github.io/graphql-over-http/draft/>
- Apollo Federation documentation:
  <https://www.apollographql.com/docs/graphos/schema-design/federated-schemas/>
- OWASP GraphQL Cheat Sheet:
  <https://cheatsheetseries.owasp.org/cheatsheets/GraphQL_Cheat_Sheet.html>
