# Measurement and Review

Use this reference to turn a broad performance request into a bounded,
falsifiable investigation.

## Define the Observation

Write down:

- the user action, route, render, or server operation;
- the slow, unstable, or resource-heavy observation;
- the environment, build mode, runtime, device class, and data size;
- the metric and acceptance threshold;
- the comparison method and number of samples;
- behavior that must not change.

Development builds are valuable for diagnostics but are not substitutes for
production-build performance. Compare like with like and record warm versus
cold behavior, cache state, network conditions, and any throttling.
Development Strict Mode may intentionally repeat renders and Effect setup.
Profilers, traces, source maps, and instrumentation can add overhead or capture
private content, so keep the instrumentation identical across comparisons and
protect or minimize the resulting artifacts.

## Evidence Ladder

Choose the smallest layer that can confirm or reject the hypothesis.

| Question | Useful evidence | Insufficient alone |
| --- | --- | --- |
| Is data serialized by awaits? | request trace or server span with dependency timing | sequential-looking source |
| Is too much code shipped? | framework bundle analysis and loaded chunks for the route | package size or import count |
| Is React rendering expensive? | React Performance tracks or Profiler data for the interaction | render count without duration |
| Is the browser main thread blocked? | performance trace with long tasks, layout, and paint | subjective animation feel |
| Is server work repeated? | request/query/cache telemetry with scoped keys | presence of an uncached function |
| Did the change help users? | comparable end-to-end metric plus behavior checks | a microbenchmark only |

Prefer user-centric and route-level measurements before local microbenchmarks.
Use a microbenchmark only when it represents the demonstrated bottleneck and
does not erase allocation, I/O, JIT, or integration costs that matter in
production.

## Review Algorithm

For each candidate:

1. State the current behavior and supporting evidence.
2. Explain the causal mechanism, including framework and version assumptions.
3. Estimate reach: critical path, frequency, data scale, and affected users.
4. Identify correctness, security, accessibility, caching, and compatibility
   risks.
5. Propose the smallest reversible change.
6. Define the focused test and comparable measurement before editing.
7. Reject the candidate if evidence disproves the mechanism or the expected
   value does not justify the risk.

Use these dispositions:

- **Fix now** — reproduced defect or meaningful measured cost on the target path.
- **Validate** — plausible high-impact risk that needs a focused measurement.
- **Defer** — real but outside the current contract or below the value threshold.
- **Reject** — unsupported, version-inapplicable, or likely to regress behavior.

## Common False Positives

- `Promise.all` across operations that are dependent, ordered, rate-limited, or
  expected to fail independently, or that exceed an upstream concurrency limit.
- Manual memoization of cheap expressions, unstable inputs, or code already
  handled by an enabled compiler.
- A render count treated as latency without render duration or interaction cost.
- Deep package imports assumed to be smaller without checking the package's
  supported exports and actual chunks.
- Lazy loading above-the-fold or layout-critical UI that worsens loading,
  interaction, or layout stability.
- A module-level cache without a bound, invalidation, isolation, or deployment
  model.
- Moving derivation to the client when it increases payload, client work, or
  exposure of server-only data.
- Treating transitions as throttling, debouncing, or a way to make network work
  faster.
- Suppressing hydration warnings instead of fixing an unexpected mismatch.
- Combining readable array operations without proof that iteration cost matters.
- Comparing runs with different build modes, instrumentation, cache state, data,
  hardware, or network conditions.

## Scenario Matrix

At minimum, validate:

1. normal data and the primary interaction;
2. empty, missing, or unauthorized data;
3. slow and failed async work;
4. rapid repeated input or navigation;
5. server render and hydration when applicable;
6. cache miss, cache hit, mutation, and invalidation when caching changed.

Add large-data, low-end-device, reduced-motion, localization, or cross-browser
coverage when they are part of the observed risk.

## Reporting Example

Keep each finding compact:

```text
Finding: route-level request waterfall
Evidence: request trace shows B starts only after independent A completes
Impact: adds one network round trip to the primary route
Change: initiate A and B together; preserve separate error handling
Validation: focused tests pass; median route metric compared over matching runs
Risk: upstream concurrency limit; monitored and bounded
Status: verified / unmeasured / rejected
```

Never manufacture a before/after number. If execution is unavailable, provide
the exact command or observation needed to close the evidence gap.
