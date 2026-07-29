# Electron Decisions

Use only the sections relevant to the selected change and supported platforms.
Repository contracts and the exact installed Electron, Chromium, Node.js,
packager, updater, and native-module versions take precedence.

## Trust Boundaries and Renderer Security

- Stay on a supported Electron release and assess Chromium, Node.js, V8, and
  Electron advisories together. A fixed minimum version is not enduring proof
  of support or security.
- Load privileged application code from reviewed local packages. Never enable
  Node.js integration for remote or untrusted content. Keep context isolation
  enabled for every renderer; refactor incompatible legacy bridges rather than
  weakening that boundary. Keep renderer sandboxing enabled unless an exact
  compatibility constraint has a compensating design, owner, tests, and
  removal plan. Do not disable `webSecurity`.
- Avoid loading application pages through broad `file://` privileges. Where
  the installed Electron version supports it, register a narrow custom
  standard and secure protocol with canonical bounded path mapping, explicit
  MIME handling, traversal and symlink resistance, CSP, and tests. Any retained
  `file://` exception requires documented scope and adversarial XSS/path tests.
- Define a restrictive Content Security Policy for the actual content and
  resource model. Avoid `eval`, dynamic code construction, unsafe inline
  execution, and executable remote code. ASAR packaging is not encryption and
  must never be treated as secret storage or a trust boundary.
- Expose a small typed preload capability surface through `contextBridge`.
  Never expose raw `ipcRenderer`, generic send/invoke/on primitives, Node.js
  objects, powerful mutable globals, or unrestricted filesystem/network access.
  Validate values again in the privileged receiver.
- For every IPC channel, define sender frame/origin/webContents eligibility,
  capability and authorization, schema and size bounds, timeout/cancellation,
  error disclosure, idempotency, concurrency, lifecycle cleanup, and audit or
  telemetry needs. Capture and validate `event.senderFrame` synchronously,
  fail closed for detached, null, navigated, or destroyed frames, and route
  responses with `event.reply` or an equivalent origin-frame mechanism rather
  than sending them implicitly to the main frame. Channel allowlists without
  sender and lifecycle validation are incomplete.
- Configure both permission request and permission check handling where the
  installed Electron APIs require them. Deny by default, bind decisions to the
  requesting origin/frame and user journey, minimize duration and scope, and
  handle revocation, navigation, session partition, and destroyed contents.
- Review Electron fuses for the exact version and threat model before signing.
  Disable unused command-execution surfaces such as `RunAsNode`, Node options,
  and CLI inspect arguments; when supported and compatible, pair embedded ASAR
  integrity validation with loading the app only from ASAR. Record justified
  compatibility exceptions and verify actual fuse and ASAR-integrity values in
  the packaged artifact rather than trusting source configuration.

## Navigation, External Inputs, and OS Integration

- Deny unexpected navigation, window creation, webview attachment, downloads,
  and external protocol opening by default. Parse URLs canonically and allow
  exact schemes, origins, paths, and actions; do not use prefix checks.
- Treat `shell.openExternal` and custom-protocol targets as code-execution or
  authority boundaries. Reject embedded credentials, control characters,
  unsafe schemes, ambiguous encodings, and overlong input. Never forward
  untrusted arguments to a shell.
- Validate deep links and command-line arguments on cold start and
  single-instance handoff. Define authentication, replay, duplicate delivery,
  focus, locked-session, and unsupported-version behavior.
- Register protocol handlers, file associations, login items, notifications,
  shortcuts, tray actions, and registry or desktop integration only with
  explicit authority and platform-specific install/uninstall ownership. Verify
  stale-registration cleanup and multi-install/channel coexistence.
- Bound clipboard, drag/drop, notification, and native callback data. Avoid
  logging user content, tokens, filesystem paths, or sensitive payloads.

## Filesystem, Windows, and Lifecycle

- Resolve user-selected paths through approved dialogs or scoped capabilities.
  Validate path type and ownership, canonicalize safely, resist traversal and
  symlink races, use least privilege, avoid predictable temporary names, and
  define atomic write, overwrite, backup, cleanup, cancellation, and failure
  behavior.
- Keep app code, user data, caches, logs, credentials, and temporary artifacts
  in their platform-appropriate owned locations. Encrypting or storing secrets
  requires an OS-backed credential boundary and a rotation/deletion design;
  permissions and encryption claims need platform evidence.
- Model every window and webContents owner, parent, modal relationship,
  partition, visibility, focus, bounds, display change, fullscreen, crash,
  suspend/resume, and destruction path. Persist only validated safe state and
  recover windows that are off-screen after display changes.
- Keep blocking or CPU-heavy work out of the main process. Bound workers,
  subprocesses, shared memory, and IPC queues; propagate cancellation and clean
  resources on navigation, window destruction, app shutdown, update, and crash.
- Preserve keyboard, focus, zoom, reduced motion, high contrast, screen-reader,
  and platform menu conventions. A web accessibility check does not prove
  native menu, dialog, tray, notification, or OS accessibility behavior.

## Packaging, Signing, Updates, and Recovery

- Inspect lockfiles, native dependencies, build hooks, packager plugins,
  downloaded binaries, entitlements/capabilities, installer scripts, and
  generated manifests as supply-chain inputs. Build in an isolated no-secret
  environment with bounded network and filesystem access; expose signing
  credentials only to the smallest authorized signing step.
- Build and test each materially distinct OS, architecture, package format, and
  native-module path. Cross-compilation or one platform's artifact is not proof
  of another. Verify artifact hashes, included files, debug surfaces, source
  maps, ASAR contents, permissions, signatures, notarization, and installer
  identity.
- Choose the updater and feed contract for the exact platform and packaging
  stack. Define signed artifact and metadata verification, channel and cohort,
  downgrade policy, compatibility window, proxy/offline behavior, retries,
  partial download, disk space, metered network, cancellation, restart consent,
  and recovery from interrupted install.
- Treat check, availability, download, verification, installation, restart,
  first launch, migration, health observation, and rollout as separate states.
  Test clean install, same-version repair, upgrade from every supported source
  version, downgrade denial or recovery, corrupt/tampered update, revoked
  signing identity, offline/proxy failure, crash loop, and rollback or forward
  repair where the chosen platform actually supports it.
- Signing, notarization, installer trust, and update requirements differ by OS,
  package format, store, and updater. Resolve current platform rules and never
  generalize one platform's guarantee to another.

## Performance, Diagnostics, and Native Modules

- Derive startup, installer, memory, CPU, GPU, frame pacing, power, disk, and
  network budgets from supported hardware and journeys. Measure cold/warm
  startup and representative idle/active/background states in a release-like
  build; report device, OS, display, power/thermal state, data set, repetitions,
  percentiles, revision, and trace location.
- Profile before optimizing. Inspect main and renderer long tasks, process
  count, preload and bundle cost, IPC rate/payload, native modules, image/font
  work, GPU behavior, timers, hidden windows, leaks, and cleanup. Do not disable
  background throttling or GPU behavior globally without a measured need and
  power/accessibility tradeoff.
- Keep production DevTools, remote debugging, inspect ports, verbose logs,
  source maps, crash dumps, and diagnostics behind explicit policy. Redact and
  bound logs and crash data, define consent, retention, access, deletion,
  offline buffering, upload endpoints, and proof of symbol/mapping ownership.
- Pin native modules and verify provenance, license, ABI/N-API compatibility,
  rebuild inputs, signatures or hashes, platform/architecture coverage,
  sandbox impact, failure fallback, update compatibility, and cleanup. Never
  run a downloaded rebuild or postinstall script merely because a module asks.

## Handoffs and Validation

- Align renderer UI and accessibility behavior with frontend/design owners.
- Align API, authentication, offline, synchronization, and conflict contracts
  with backend/data owners.
- Align Electron hardening, supply chain, signing, update, telemetry, and
  privacy boundaries with security owners.
- Align performance budgets, profiling method, representative hardware,
  measurement variability, and optimization acceptance with performance owners.
- Align matrix builds, credentials, artifact retention, distribution, staged
  rollout, monitoring, and recovery with release/operations owners.
- Align representative hardware, platform, install/upgrade, accessibility,
  native integration, and interruption coverage with test owners.

Validation sequence:

1. Parse the complete process/trust graph, Electron configuration, preload and
   IPC surface, sessions, windows, navigation, permissions, filesystem and
   protocol handlers, native modules, packager, signing, updater, and release
   configuration for the exact versions.
2. Run repository-pinned lint, type, unit, integration, security, package, and
   artifact checks in an already-clean isolated checkout, worktree, or
   temporary copy. Never clean, reset, overwrite, or switch the user's active
   tree.
3. Exercise malicious renderer and IPC inputs, sender/frame confusion,
   navigation and popup denial, permission grant/deny/revoke, hostile deep
   links/files/paths/URLs, window and process crashes, suspend/resume,
   multi-display changes, offline/proxy behavior, and resource exhaustion.
4. Observe release-like artifacts on every materially different platform path.
   Check install/uninstall, protocol/file registration, native menus and
   notifications, accessibility, signing/notarization, updates, migration,
   recovery, performance, logs, and crash data.
5. If distribution is authorized, confirm active identity, exact artifact,
   channel/cohort/target, staged observation, pause criteria, rollback or
   forward-repair readiness, and ownership before each remote mutation.

Report exact source and artifact revisions, platform matrix, trust and process
boundaries, IPC/preload changes, native integrations, security and
accessibility evidence, measured performance conditions, signing/update and
distribution states, warnings, remaining risks, and owner actions.

## Primary Sources

- Electron security checklist:
  <https://www.electronjs.org/docs/latest/tutorial/security>
- Electron process sandboxing:
  <https://www.electronjs.org/docs/latest/tutorial/sandbox>
- Electron context isolation:
  <https://www.electronjs.org/docs/latest/tutorial/context-isolation>
- Electron process model:
  <https://www.electronjs.org/docs/latest/tutorial/process-model>
- Electron fuses:
  <https://www.electronjs.org/docs/latest/tutorial/fuses>
- Electron ASAR integrity:
  <https://www.electronjs.org/docs/latest/tutorial/asar-integrity>
- Electron application updates:
  <https://www.electronjs.org/docs/latest/tutorial/updates>
- Electron code signing:
  <https://www.electronjs.org/docs/latest/tutorial/code-signing>
