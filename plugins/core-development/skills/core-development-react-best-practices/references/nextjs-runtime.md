# Next.js Runtime Review

Use this reference only for a Next.js application. Check the installed release,
router, deployment runtime, and current official documentation: caching and
rendering semantics change between versions.

## Server and Client Boundaries

Keep server-only values, authorization decisions, and privileged data on the
server. Add a Client Component boundary only where browser APIs, state, events,
or client-only libraries require it.

At each boundary, inspect:

- data serialized to the browser, including nested and duplicated values;
- whether the client needs the original or a safe minimal projection;
- serializability and hydration behavior;
- bundle growth caused by client imports;
- exposure of internal or sensitive fields.

Do not move work to the client solely to reduce server time. Compare response
payload, browser execution, interactivity, privacy, and caching.

## Data Dependencies and Streaming

Draw the dependency graph before changing awaits:

- start independent work together;
- start dependent work as soon as its prerequisite exists;
- preserve ordering where mutations, locks, quotas, or failure semantics require
  it;
- use component composition and Suspense for streaming when the fallback and
  layout behavior are acceptable.

Server Actions are mutation endpoints, not a general parallel-fetch transport.
Treat every action as directly reachable: validate input, authenticate,
authorize the specific resource, and constrain side effects inside the action.
Do not rely only on page, layout, or middleware checks.
Next.js dispatches client-triggered Server Actions sequentially per client in
current releases. Do parallel independent work inside one authorized action or
use the appropriate read endpoint; do not expect several client calls to run in
parallel.

Streaming can improve initial visibility while worsening layout shift or hiding
critical errors. Test the fallback, slow response, rejected response, and final
layout.

## Caching

Do not add a cache without documenting:

- request-local, process-local, deployment-wide, or external scope;
- key composition and tenant or user isolation;
- freshness and stale behavior;
- size and eviction;
- mutation invalidation and read-your-own-writes expectations;
- error, rejection, and empty-result handling;
- behavior across replicas, cold starts, and deployments.

React `cache` memoizes server work within the supported server-rendering
context; it is not a general durable cache. Framework data and route caches have
version-specific defaults and APIs. Verify the current semantics rather than
repeating an older rule such as “all fetches are automatically cached.”

Process-local LRU caches are unsafe for request-specific data without keys and
isolation, diverge across instances, disappear on restart, and can retain
objects unexpectedly. Use them only when the deployment model and invalidation
contract make those properties acceptable.

## Work After the Response

Use `after` only for work whose completion does not determine the response.
Understand the platform's execution duration, retry, observability, and failure
guarantees. Keep security-relevant audit records and required transactions in a
delivery mechanism that satisfies their durability contract.

Do not place secrets or raw session values into analytics or ordinary logs.
Make failures visible through an approved observability channel.

## Client Bundle

Use framework build output and a bundle analyzer to identify route-level cost.
Then:

- prefer documented package exports over unsupported deep paths;
- verify whether the current framework already optimizes the package;
- lazy-load code that is large, optional, and outside the critical first
  interaction;
- retain an accessible loading and error state;
- preload only from a credible user-intent or route signal;
- confirm the chunk is absent from the initial path and loaded when required.

Do not equate source imports with delivered bytes. Tree shaking, package
exports, side effects, CommonJS boundaries, and framework transforms determine
the actual result.

## Validation Matrix

When changing an App Router path, cover:

1. direct request and client navigation;
2. authenticated, unauthorized, and cross-resource access;
3. slow, failed, empty, and partial data;
4. streamed fallback and completed content;
5. cache miss, hit, mutation, invalidation, and refresh;
6. server logs and browser console without leaked data;
7. production build output and intended deployment runtime.

## Primary References

- [Fetching data](https://nextjs.org/docs/app/getting-started/fetching-data)
- [Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components)
- [Data security](https://nextjs.org/docs/app/guides/data-security)
- [Server Actions](https://nextjs.org/docs/app/guides/server-actions)
- [Caching and revalidation](https://nextjs.org/docs/app/getting-started/caching-and-revalidating)
- [`after`](https://nextjs.org/docs/app/api-reference/functions/after)
- [Lazy loading](https://nextjs.org/docs/app/guides/lazy-loading)
- [Package bundling](https://nextjs.org/docs/app/guides/package-bundling)
