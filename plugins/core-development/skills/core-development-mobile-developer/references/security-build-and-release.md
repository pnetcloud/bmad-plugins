# Security, Build, and Release

Use this reference for mobile threat decisions, build variants, signing,
distribution, store preparation, telemetry, rollout, and handoffs.

## Contents

- Define the mobile threat model
- Protect data, identity, and platform boundaries
- Handle network trust and device-integrity signals
- Build and sign without exposing credentials
- Prepare truthful store and privacy metadata
- Release progressively and preserve rollback
- Coordinate cross-role contracts

## Define the Mobile Threat Model

Classify the app's assets, actors, data, operations, and exposure before adding
controls. Use current OWASP MASVS/MASTG guidance as a verification reference
across:

- storage;
- cryptography;
- authentication and authorization;
- network communication;
- platform interaction;
- code quality and dependency maintenance;
- resilience to reverse engineering or tampering;
- privacy.

Select requirements from risk, regulation, platform policy, and product
contracts. Do not claim "MASVS compliant" from a checklist; identify the
profile/controls, test evidence, version, scope, and unresolved exceptions.

Assume an attacker can inspect, modify, or automate a distributed client. Keep
authorization and high-value trust decisions on a verified server boundary.

## Protect Data, Identity, and Platform Boundaries

- Minimize collection, retention, local storage, logs, analytics, backups,
  screenshots, clipboard use, and notification content.
- Use platform-provided protected storage, such as Keychain or Android
  Keystore-backed mechanisms, for suitable small secrets or keys. Verify
  accessibility, backup, migration, invalidation, and device-lock semantics.
- Do not place service credentials in source, environment files bundled into
  the app, generated configuration, resource files, or remote configuration.
  Public client identifiers are not secrets; scope and monitor them.
- Use established platform and library cryptography. Define key ownership,
  rotation, loss, migration, and recovery; do not invent algorithms.
- Bind biometric prompts to a protected local operation or key. Keep server
  authentication and authorization explicit.
- Validate deep links, intents, URL schemes, exported components, paste/share
  input, file providers, and native callbacks as untrusted inputs.
- Apply least privilege to permissions, entitlements, capabilities, background
  modes, and inter-process interfaces.
- Remove sensitive values from crash reports, logs, traces, screenshots,
  analytics, and support exports.

Obfuscation and minification can increase reverse-engineering cost but do not
make embedded secrets or client-side authorization trustworthy.

## Handle Network Trust and Device-Integrity Signals

Use platform TLS validation and current secure transport defaults. Use pinning
only when the threat model justifies its
operational cost and the product owns:

- pin and backup-pin lifecycle;
- certificate/key rotation overlap;
- emergency recovery or remote disablement that cannot itself be abused;
- proxy/VPN/accessibility/enterprise compatibility;
- failure telemetry and user-safe error behavior;
- tests for expiration, rotation, clock, and offline cases.

Pinning without a recovery design can turn routine certificate rotation into an
outage. Do not present it as a universal API-call requirement.

Treat jailbreak/root detection and platform integrity/attestation services as
risk signals. They can raise assurance or drive step-up controls but are
bypassable and must not be the sole authorization boundary. Use the current
platform service supported by the repository; do not copy retired service names
from older examples.

## Build and Sign Without Exposing Credentials

Maintain explicit development, test, staging, and production build variants or
schemes only where the project needs them. Verify:

- bundle/package identifiers and application IDs;
- deployment targets, architectures, signing teams, and provisioning;
- entitlements, capabilities, exported components, URL/app links, and
  notification configuration;
- endpoint and feature configuration without embedded secrets;
- debug flags, logging, test endpoints, and development menus excluded from
  production;
- code shrinking/obfuscation rules with reflection/serialization/native
  compatibility;
- asset catalogs, image/vector optimization, app thinning, architecture splits,
  dynamic features, or on-demand resources as supported;
- reproducible dependency and toolchain resolution;
- software-bill-of-materials, license, and vulnerability review as required.

Use Apple-managed signing/provisioning or repository-approved explicit signing
according to the release process. Use Google Play App Signing where the
distribution contract requires it. Keep private keys, certificates, passwords,
API tokens, provisioning material, and signing-store files in an authorized
credential system; inject them only into the bounded build job.

Do not print signing values or persist them in artifacts beyond the required,
access-controlled retention. Define certificate expiry monitoring, rotation,
revocation, backup, and recovery ownership.

Fastlane, Codemagic, Bitrise, another CI service, or custom pipelines are
implementation choices. Review third-party actions/plugins, pin versions,
minimize permissions, isolate signing jobs, and keep release approval explicit.

## Prepare Truthful Store and Privacy Metadata

Derive metadata from the built artifact and actual product behavior:

- screenshots for required devices and localizations;
- name, subtitle/short description, long description, keywords or discovery
  metadata as supported by the store;
- localization and right-to-left review;
- support and publicly reachable privacy-policy information;
- age/content rating;
- export or encryption declarations;
- data collection, sharing, tracking, purpose, retention, deletion, and
  account-deletion behavior;
- third-party SDK data practices;
- Apple privacy manifests and required-reason APIs where applicable;
- Google Play Data safety and other current declarations;
- release notes and known limitations;
- entitlement/capability and review-note evidence;
- store API automation scoped to the minimum required role.

Reconcile permissions, SDKs, domains, manifests, compiled capabilities,
analytics events, backend behavior, and store answers. A copied or stale privacy
answer is a release defect.

App Store Optimization and keyword research may improve discovery, but they
must remain truthful and should not delay required functional, privacy,
accessibility, or policy work.

Store policies and SDK requirements change. Verify current official guidance
at release time instead of hardcoding a review-guideline version.

## Release Progressively and Preserve Rollback

Separate these states:

1. tests passed locally;
2. release-representative build produced;
3. signed artifact verified;
4. internal or beta distribution completed;
5. store submission accepted for review;
6. store review approved;
7. staged production rollout healthy;
8. full rollout healthy.

For each state, retain artifact identity, version/build number, source revision,
configuration class, test evidence, signing verification, and owner.

Use TestFlight, Firebase App Distribution, another beta service, or store tracks
according to the existing process. Do not distribute without authorization.

Before rollout:

- define health indicators and observation window;
- verify crash symbolication and Android mapping/native symbols;
- test server/API compatibility with old and new app versions;
- define data migration forward/backward constraints;
- choose staged percentages/cohorts from risk rather than a canned sequence;
- confirm feature-flag and remote-config defaults, ownership, and failure mode;
- define pause, rollback, forward-fix, and store-removal decisions;
- account for users who cannot immediately downgrade or update.

A binary rollback cannot undo an incompatible local-data migration or server
contract. Preserve compatibility or provide an explicit recovery design.

A/B testing and remote configuration require experiment integrity, consent and
privacy review, exposure logging, guardrails, and safe defaults. Do not use them
to bypass store review or deliver executable code where policy forbids it.

## Coordinate Cross-Role Contracts

Use concrete handoffs rather than assuming named agents exist:

- **Backend/API:** mobile payload shape, pagination, idempotency, retries,
  compatibility, offline sync, authorization, and rate limits.
- **Product/design:** platform parity/divergence, accessibility, permission
  rationale, empty/error/offline states, and supported devices.
- **QA:** device/OS matrix, lifecycle, native integrations, automation,
  performance journeys, and evidence storage.
- **Security/privacy/legal:** threat model, sensitive data, SDKs, disclosures,
  cryptography, attestation, regulated features, and exceptions.
- **Release/operations:** reproducible builds, signing, store roles,
  symbolication, rollout, monitoring, and rollback.
- **Performance:** budgets, representative devices, trace method, regression
  gate, and tradeoffs.
- **Analytics/experimentation:** event contract, consent, minimization,
  retention, experiment guardrails, and data-quality validation.

Report unresolved ownership explicitly. Coordination is not evidence that the
other side changed or validated its contract.
