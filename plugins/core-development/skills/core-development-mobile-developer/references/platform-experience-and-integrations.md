# Platform Experience and Integrations

Use this reference for native-quality interaction, adaptive layout,
accessibility, permissions, and system capabilities.

## Contents

- Follow current platform conventions
- Make layouts and input adaptive
- Build accessibility into the contract
- Request permissions and sensitive capabilities safely
- Validate links and notifications
- Handle background and optional platform surfaces

## Follow Current Platform Conventions

Consult the current Apple Human Interface Guidelines and Android app-quality,
Material, and accessibility guidance for the supported deployment targets.
Use repository-selected design systems and platform components before inventing
new behavior.

Preserve familiar platform semantics for:

- navigation hierarchy, back/dismiss behavior, and state restoration;
- system bars, safe areas, keyboard/insets, and focus;
- destructive actions, confirmations, undo, and error recovery;
- menus, sheets, dialogs, selection, sharing, and search;
- gestures, haptics, motion, and reduced-motion settings;
- light/dark appearance, contrast, Dynamic Type or font scaling, and locale;
- loading, empty, partial, stale, offline, and unavailable states.

Do not imitate the visual appearance of another platform when doing so breaks
native navigation, accessibility, or system expectations. Share design intent
while permitting native expression.

## Make Layouts and Input Adaptive

Design for the supported device matrix rather than one nominal phone:

- compact and expanded windows;
- orientation and resizable/multitasking windows;
- phones, tablets, foldables, desktop modes, and external displays when in
  scope;
- touch, keyboard, pointer, switch, voice, and assistive input;
- camera cutouts, safe regions, hinges, and system UI;
- long translations, right-to-left layout, larger text, and zoom;
- reduced motion, increased contrast, and other system preferences.

Keep task continuity when layout changes. Avoid treating a tablet or unfolded
device as a scaled-up phone when a list/detail or multi-pane arrangement serves
the task better.

Profile dense lists and media on realistic data. Use the framework's
virtualization and lazy-loading primitives before adopting a third-party list.
Preserve accessibility ordering and restoration when recycling items.

## Build Accessibility Into the Contract

For every interactive surface:

- expose a meaningful role, label, value, state, and action;
- keep focus order and reading order intentional;
- provide an accessible alternative to gesture-only or motion-only behavior;
- use sufficiently large controls and spacing per current platform guidance;
- support text scaling without clipping, overlap, or loss of function;
- avoid color as the only signal and meet applicable contrast requirements;
- announce important asynchronous changes without excessive interruption;
- respect reduced motion and avoid harmful flashing or sustained oscillation;
- test with VoiceOver and TalkBack, not only static inspection;
- test keyboard/switch/voice paths when those inputs are in scope.

Validate the built screen with the platform accessibility inspector and a
representative manual task. Automated checks do not prove usable focus,
descriptions, or gesture alternatives.

## Request Permissions and Sensitive Capabilities Safely

Apply this sequence to camera, photo library, location, biometrics, sensors,
Bluetooth Low Energy, health/fitness data, microphone, contacts, and similar
capabilities:

1. Confirm the capability is necessary for an explicit user-facing feature.
2. Request the narrowest scope and timing the platform supports.
3. Explain the benefit in context without coercion or misleading UI.
4. Handle not-determined, granted, limited, denied, restricted, revoked, and
   capability-unavailable states.
5. Avoid repeated prompts after denial; provide a usable fallback and a
   deliberate route to settings when appropriate.
6. Stop listeners, sessions, scanning, and background use when no longer
   needed.
7. Minimize, classify, retain, disclose, and protect resulting data.
8. Test interruption, process restoration, account change, and device
   capability variation.

Use platform biometric APIs to authorize access to protected operations or
locally held keys. Do not treat a successful device biometric prompt as a
server identity proof unless the protocol explicitly binds and verifies it.

For health, location, children, financial, or other regulated/sensitive data,
confirm the applicable legal, store, product, and retention requirements with
the responsible owner before implementation.

## Validate Links and Notifications

Treat deep links, universal/app links, custom schemes, notification payloads,
shared items, and shortcuts as untrusted input.

- Parse with a strict route and parameter schema.
- Reject unknown routes, malformed identifiers, dangerous schemes, path
  traversal, and unexpected nested URLs.
- Require current authentication and authorization at the destination; never
  use possession of a link as sufficient access.
- Avoid placing secrets or sensitive personal data in URLs and notification
  bodies.
- Make replay and duplicate delivery safe.
- Verify claimed-domain/app association files and platform package/bundle
  identity.
- Handle cold start, warm start, foreground, background, logged-out, expired
  session, and unsupported-version cases.
- Provide a safe fallback when an associated service or destination is
  unavailable.

For push notifications:

- separate registration identity from user identity;
- update or revoke tokens across reinstall, logout, account switch, and token
  rotation;
- minimize payload data and fetch authorized content after activation when
  appropriate;
- respect notification permission and user preference;
- test rich media and extension failures without blocking delivery;
- deduplicate actions and track outcomes without sensitive payloads.

## Handle Background and Optional Platform Surfaces

Background execution is constrained by platform scheduling, power, network,
and user settings. Use the platform-supported mechanism, such as an Android
scheduled-work API or the corresponding Apple background capability, only for
eligible work.

- Make work resumable, idempotent, time-bounded, and cancellation-aware.
- Declare required constraints such as connectivity, charging, or storage.
- Persist only enough state to resume safely.
- Do not emulate an unrestricted service when the platform does not promise
  one.
- Test delayed execution, duplicate invocation, termination, timeout, and
  upgrade.

Treat widgets, Live Activities, app shortcuts, share/action extensions, Siri or
assistant integrations, watch companions, Wear OS, CarPlay, Android Auto, and
other system surfaces as separate clients:

- define their limited data and action contract;
- account for independent lifecycle, caching, authentication, privacy, and
  version skew;
- use shared domain rules without assuming the main app process is alive;
- verify platform entitlement, store, distraction, and review requirements;
- provide a degraded state when the main service is unavailable.
