# Performance and Testing

Use this reference to define evidence, select tools, and verify mobile behavior
without claiming universal thresholds.

## Contents

- Define measurable budgets
- Profile representative builds and devices
- Apply framework-specific techniques conditionally
- Build a risk-based test matrix
- Monitor production quality

## Define Measurable Budgets

Derive budgets from product expectations, current baselines, supported devices,
store quality signals, and explicit service objectives. Record:

| Field | Required detail |
| --- | --- |
| Journey | exact user action and start/end events |
| Metric | startup, frame pacing, input latency, memory, battery, network, size, crash, or ANR |
| Population | device/OS classes, percentile or distribution, and sample size |
| Build | profile/release mode, symbols/minification, and app version |
| Conditions | dataset, account state, cache, network, power, thermal state, and install/upgrade state |
| Baseline | observed value and trace/result location |
| Budget | source and rationale |
| Result | before/after, variability, and remaining regression |

Measure cold, warm, and hot startup separately where the platform does. Define
both initial presentation and usable/fully drawn state. Do not report a single
"startup time" whose boundary is unknown.

Match frame budget to the display's active refresh rate. Report slow or missed
frames and user-visible jank rather than claiming all devices must sustain a
particular maximum rate.

Measure responsiveness for the actual interaction. A frame interval is not a
complete end-to-end touch latency target.

Measure memory under representative navigation, media, lists, backgrounding,
and pressure. Distinguish managed heap, native allocations, graphics, and
process footprint when the tools support it.

Measure energy with platform tools over a defined journey and duration. Avoid a
universal percentage-per-hour target because radios, sensors, device health,
screen, thermal state, and workload dominate it.

Measure download, install, and on-device size separately. Account for store
delivery, architecture splits, asset packs/on-demand resources, symbols, and
locale/device variants.

## Profile Representative Builds and Devices

- Use a profile or release-representative build for performance conclusions.
  Debug/hot-reload instrumentation can distort results.
- Reproduce on a representative low-end or oldest-supported device and at
  least one current device when the supported matrix warrants it.
- Control cache, install state, data volume, network shaping, battery, and
  thermal conditions.
- Warm up where the metric requires it and repeat enough times to expose
  variance.
- Save traces or machine-readable results when possible.
- Change one causal factor at a time and rerun the same journey.
- Verify that an optimization preserves correctness, accessibility, image
  quality, and lifecycle behavior.

Profile before adding memoization, prefetching, batching, compression,
virtualization, code splitting, native code, custom rendering, or graphics API
work. Each can trade startup, memory, battery, bundle size, complexity, or
freshness against another metric.

Use platform tools appropriate to the active project, such as Instruments and
Xcode metrics on Apple platforms, Android Studio profilers, Perfetto,
Macrobenchmark, and Android vitals on Android. Check current official guidance
and repository support before naming a tool in a command.

## Apply Framework-Specific Techniques Conditionally

### React Native

- Confirm the repository's React Native release and architecture mode.
- Prefer current React Native DevTools and supported platform profilers.
  Do not assume an older external debugger is supported by the active release.
- Use Web Performance-compatible APIs only where the repository version
  supports them, and distinguish them from browser Core Web Vitals.
- Treat Hermes and New Architecture behavior as version-specific. Do not
  require experimental compiler/runtime modes for production.
- Profile JavaScript and UI/native threads, native modules, image decoding,
  bridge/interop work, and commit/render behavior before choosing a fix.
- Configure built-in list virtualization first. Use stable keys, bounded item
  work, appropriate window/batch settings, and measured `renderItem`
  optimization. Adopt a third-party list only with compatibility and benchmark
  evidence.
- Use memoization when profiling or render ownership shows avoidable work; do
  not wrap every component by default.
- Verify startup changes such as lazy initialization, bundle segmentation, or
  inline requirements against the repository version and release build.

### Flutter

- Profile in Flutter's profile mode on representative devices.
- Use Flutter DevTools for frame, CPU, memory, network, and rebuild analysis
  supported by the active version.
- Treat Impeller and renderer selection as platform/version-specific; verify
  defaults before changing configuration.
- Use lazy builders and stable item identity for large lists.
- Move CPU-heavy Dart work off the UI isolate only when profiling shows a
  blocking workload and the message/copy cost is justified.
- Prefer platform channels for structured host API calls; consider FFI for
  suitable C-compatible libraries after validating memory, thread, packaging,
  and security ownership.
- Measure shader/asset behavior and image cache pressure on target devices
  before adding warm-up or custom cache policy.

### Native and Shared-Code Options

Use Swift Package Manager, Gradle configuration cache, code shrinking, asset
thinning, dynamic feature delivery, Kotlin Multiplatform, Compose
Multiplatform, Metal/Vulkan, or other platform features only when compatible
with the existing stack and supported targets. Preserve reproducible builds and
measure their actual effect.

## Build a Risk-Based Test Matrix

Use the layers that can fail independently:

- unit tests for domain rules, validation, reducers/view models, conflict
  policy, and serialization;
- component/widget tests for rendering, state transitions, accessibility
  semantics, and error states;
- native integration tests for module/channel/FFI contracts, lifecycle,
  permissions, and failure mapping;
- contract tests for backend/API and stored schema compatibility;
- end-to-end tests for critical user journeys on each divergent platform path;
- platform-native suites for extensions, services, entitlements, and APIs not
  exercised by the cross-platform harness;
- performance benchmarks and regression thresholds for measured journeys;
- manual exploratory checks for assistive technology, hardware, store, and
  system UI behavior that automation cannot prove.

Jest, Flutter test/integration_test, Detox, Maestro, Patrol, XCTest, Android
instrumentation, or another tool may fit the project. Reuse installed,
maintained tooling instead of adding a parallel harness by default.

Cover relevant transitions:

- fresh install, migration, rollback-compatible data, and restore;
- cold/warm/hot start and process death;
- foreground/background and interruption;
- permission grant, limited access, denial, revocation, and settings changes;
- offline, reconnect, slow/lossy network, timeout, duplicate, reorder, and
  partial response;
- low memory/storage, thermal pressure, and background restrictions;
- account switch, token expiry, logout, and protected-data lock;
- locale, right-to-left, text scaling, theme, rotation/window resize, and
  supported form factors;
- missing hardware, unsupported OS API, and degraded external service;
- native crash, JavaScript/Dart error, ANR/hang, and recovery.

Use fault injection in a controlled test environment. Do not perform destructive
"chaos" actions against devices, accounts, stores, or services outside explicit
test scope.

## Monitor Production Quality

Define:

- crash and ANR collection with symbols/mappings available under controlled
  access;
- startup and interaction metrics with version/device segmentation;
- memory-pressure, background-work, network, and battery indicators;
- release health gates based on the store's current definitions;
- privacy-preserving analytics with documented purposes and retention;
- alerts, ownership, triage, staged rollout, and rollback decision rules.

Sentry, Firebase Crashlytics, another crash system, Amplitude, Mixpanel,
Firebase Analytics, another analytics system, remote configuration, A/B
experiments, and feature flags are optional implementation choices. Review
their SDK data practices, permissions, consent, failure behavior, size, and
current platform support before adoption.

Do not call browser Core Web Vitals a complete native-mobile monitoring model.
Use platform and framework metrics that correspond to actual mobile journeys.
