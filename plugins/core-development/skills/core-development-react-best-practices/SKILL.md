---
name: core-development-react-best-practices
description: Diagnose, review, or improve web React and Next.js correctness and performance using version-aware, measurement-led changes. Use for React render latency, hydration, effects, state, concurrency, Server Components, data waterfalls, caching, serialization, or client-bundle work. Do not use for React Native, framework-free JavaScript tuning, visual design, or speculative rewrites without a reported symptom or review scope.
license: MIT
---

# Evidence-Led React Performance

Improve the user-visible outcome without trading away correctness, security,
accessibility, or maintainability. Treat every optimization as a hypothesis
until the intended environment supplies evidence.

## Establish the Contract

Before proposing or editing code:

1. Read repository instructions, manifests, lockfiles, framework configuration,
   compiler settings, routes, tests, and the complete affected data flow.
2. Record the installed React and framework versions. Distinguish plain React,
   a framework integration, and framework-specific server behavior; never apply
   a Next.js rule to an unrelated React application.
3. Identify the observed symptom, affected interaction or route, target
   environment, device or runtime class, expected behavior, and success metric.
4. Preserve existing semantics, authorization, accessibility, error handling,
   cache consistency, and browser support unless the task explicitly changes
   them.
5. Capture a reproducible baseline when execution is authorized. If no runtime
   is available, label conclusions as static review findings rather than
   measured gains.

Permission to review or edit code does not authorize installing packages,
starting services, running a production build, accessing accounts, or sending
traffic to production. Inspect project commands before executing them because
package and build scripts can run arbitrary host code. Do not install a newer
framework, enable a compiler, or change shared infrastructure merely to
investigate.

## Rank the Work

Investigate in this order:

1. correctness, security, hydration, and stale-state defects;
2. request and render waterfalls on the critical path;
3. excessive client code, assets, or server-to-client serialization;
4. repeated server work, cache scope, and invalidation;
5. expensive React renders during real interactions;
6. browser layout, paint, memory, and long-task pressure;
7. JavaScript micro-optimizations in a demonstrated hot path.

Do not assign universal severity or percentage gains to a pattern. Priority
comes from the product path, frequency, affected users, measured cost, and
change risk.

## Diagnose Before Editing

Build a short hypothesis table with the symptom, suspected cause, evidence
needed, and disconfirming result. Read
[references/measurement-and-review.md](references/measurement-and-review.md)
for the evidence ladder and review format.

For React state, Effects, memoization, transitions, hydration, lists, or browser
work, read [references/react-runtime.md](references/react-runtime.md). For
Next.js App Router, Server Components, Server Actions, caching, streaming, or
bundle behavior, also read
[references/nextjs-runtime.md](references/nextjs-runtime.md).

Prefer evidence at the failing boundary:

- network timing for request waterfalls;
- framework build or bundle output for shipped code;
- React Performance tracks or Profiler data for render cost;
- browser performance traces for long tasks, layout, and paint;
- server traces, query counts, and cache telemetry for backend work;
- focused tests for correctness, hydration, and race behavior.

Synthetic examples and rule matches can locate risk; they do not prove impact.

## Make the Smallest Defensible Change

Change one causal boundary at a time so the result can be attributed:

- start independent work together, but preserve dependency and failure
  semantics, cancellation, transaction ordering, and resource limits;
- move work across a server/client boundary only after checking serialization,
  security, and runtime support;
- reduce shipped code only when the import path and lazy boundary remain
  supported by the package and bundler;
- add memoization only when work is expensive and inputs are stable;
- introduce a cache only with explicit scope, key, lifetime, invalidation,
  error, and tenant-isolation behavior;
- use concurrency features for interruptible non-urgent rendering, not to hide
  uncontrolled event frequency or slow I/O;
- preserve observable error paths rather than swallowing failures.

Avoid broad rewrites, copied benchmark numbers, unsupported deep imports,
unbounded module-level caches, ad hoc authentication caches, blanket lazy
loading, blanket memoization, and dependency-array suppression.

## Validate the Outcome

Use the narrowest project-declared checks, then widen in proportion to risk:

1. type-check, lint, and run focused unit or component tests;
2. exercise success, failure, empty, loading, and rapid-update behavior;
3. verify server and client rendering or hydration when the boundary changed;
4. repeat the baseline measurement under comparable conditions;
5. inspect regressions in bundle size, requests, render count, responsiveness,
   accessibility, and error behavior;
6. run broader project gates for shared code or configuration.

Use multiple samples for noisy timings and report the environment. A faster
single run, a smaller source file, or fewer component renders is not sufficient
unless it improves the target outcome without a material regression.

## Report

Return:

- scope, versions, environment, and observed symptom;
- findings ordered by evidence-backed impact and risk;
- changes made, with the causal reason for each;
- exact validation commands and results;
- comparable before/after measurements, or an explicit unmeasured status;
- collected artifact locations and their privacy or retention handling;
- correctness, security, accessibility, and compatibility checks;
- remaining hypotheses, limitations, and rollback guidance.

Call an optimization verified only when the target behavior and metric were
reproduced after the change. Keep static recommendations clearly separate from
runtime evidence.

This skill preserves and refines concepts from
[Vercel Labs Agent Skills](https://github.com/vercel-labs/agent-skills), whose
React best-practices package declares the MIT license.
