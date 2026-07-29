# Playwright Security and Evidence

Use this reference for authenticated, stateful, file, network, production, or
artifact-heavy tests.

## Contents

- Target and authority
- Authentication state
- External effects
- Files and network
- Evidence artifacts
- Execution and completion

## Target and Authority

Bind the exact environment and application before execution. Do not infer a
target from an open port, browser history, default URL, or similarly named
service. Confirm whether the run may create, update, delete, publish, notify, or
charge.

Prefer a disposable local or test environment. A read-only production smoke
check requires explicit authorization and must avoid form input, account state
changes, broad crawling, and load generation.

Do not test a third-party site merely because the browser can reach it. Mock or
contract-test dependencies outside the user's control.

## Authentication State

Browser state can contain impersonation-capable cookies and headers.

- Never request secrets in conversation or embed them in test source, command
  arguments, fixtures, snapshots, or reports.
- Use the repository's approved secret injection and setup project.
- Keep authenticated state in the established ignored location with restricted
  access and bounded retention.
- Do not commit state even to a private repository.
- Use least-privileged synthetic accounts and separate accounts for parallel
  workers when tests mutate server data.
- Confirm the visible account and role before sensitive assertions or actions.
- Do not bypass multi-factor checks, CAPTCHA, consent, or access controls.

## External Effects

Treat these as explicit gates:

| Effect | Preferred test boundary |
|---|---|
| Message or notification | Captured test sink |
| Payment or purchase | Provider sandbox or deterministic fake |
| Permission or membership | Disposable tenant and exact cleanup |
| Publication | Draft or isolated test namespace |
| Deletion | Test-owned record with precondition and postcondition |
| Bulk action | Bounded fixture set and exact count assertions |

Before a mutating action, assert the exact account, target, values, and starting
state. After it, assert both the visible response and the material persisted
effect. On timeout, inspect current state before retrying.

Retries must not repeat a non-idempotent external effect blindly.

## Files and Network

Uploads disclose local content. Resolve and inspect the exact synthetic fixture;
never substitute an arbitrary user file or upload a directory.

Downloads are untrusted. Save them to the configured test output, validate name,
type, size, and content safely, and do not execute or open them with a privileged
application.

Network routes and mocks change observed behavior. Keep them narrow and report
which dependencies were simulated. Global header injection can disclose
authorization data to redirects and asset origins; scope headers to the intended
origin and avoid putting secrets in logs.

Do not disable the browser sandbox, ignore certificate errors, grant broad
permissions, spoof location, or force actions simply to make a test pass.

## Evidence Artifacts

Screenshots, videos, traces, HTML reports, console output, downloads, and network
archives can contain page text, personal data, tokens, headers, cookies, source
fragments, and response bodies.

- Capture on failure or first retry unless continuous capture is required.
- Minimize page area, duration, and network scope.
- Redact before sharing and do not publish raw protected artifacts.
- Store under the project-approved output path, not a predictable shared
  temporary filename.
- Set retention and cleanup behavior explicitly.
- Treat trace viewers and reports as sensitive local applications.

Do not log complete request or response bodies by default. Prefer a minimized
diagnostic with status, safe identifiers, timing, and the first divergence.

## Execution and Completion

Review the selected test and all setup, teardown, fixtures, package scripts, and
reporter code that it invokes. They are executable host code.

Run the focused test first. Record the initial outcome separately from retries.
If a retry passes, report a flaky result and preserve the first-failure evidence.

Stop when the target differs, protected data appears, the account is wrong, an
effect exceeds the fixture boundary, or cleanup would touch data not created by
the test.

Completion requires the requested observable assertion on the intended target,
plus any material downstream state verification. Artifact creation alone is not
proof.
