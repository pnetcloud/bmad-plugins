# Playwright Test Design

Use this reference when creating or substantially changing test coverage.

## Contents

- Choose the browser boundary
- Build a scenario matrix
- Locators and assertions
- Isolation and data
- Network behavior
- Browser and visual coverage
- Maintainability

## Choose the Browser Boundary

Use Playwright when the risk depends on rendering, actionability, navigation,
browser storage, downloads, uploads, permissions, or an end-to-end user flow.
Prefer unit, component, contract, or API tests for behavior that does not require
the browser. Avoid duplicating the same assertion at every layer.

Start from an acceptance statement and name the observable evidence. If the
expected outcome cannot be observed, refine the contract before writing a test.

## Build a Scenario Matrix

For each important workflow, consider:

| Scenario | Evidence |
|---|---|
| Success | User-visible state and persisted effect |
| Validation failure | Clear feedback and no forbidden effect |
| Permission failure | Bounded denial and no data disclosure |
| Boundary | Empty, maximum, duplicate, expired, or concurrent state |
| Recovery | Retry, refresh, back navigation, or resumed state |
| Compatibility | Required browser, viewport, input mode, or locale |

Choose cases by impact and regression risk. Do not generate a combinatorial
matrix without a reason.

## Locators and Assertions

Locator preference:

1. role plus accessible name;
2. label, placeholder, alt text, title, or visible text;
3. an explicit test ID that represents a stable contract;
4. scoped CSS only when no user-facing contract exists;
5. XPath only for an unavoidable legacy boundary.

Strictness is useful evidence. When a locator matches multiple elements, scope
it to the meaningful region or improve the product's accessibility contract.
Do not select the first match merely to make the test run.

Use web-first assertions that retry against the browser state. Assert meaningful
outcomes such as visibility, enabled state, URL, accessible value, collection
contents, or a confirmed backend effect. Avoid reading a value and asserting it
later with a non-retrying generic assertion.

Wait on the condition the user needs. Fixed delays hide races. Generic network
idleness is unreliable for applications with polling, streaming, or analytics.

## Isolation and Data

Each test receives a fresh browser context, but server-side state still requires
isolation. Create unique synthetic records through approved fixtures or APIs,
keep ownership visible, and clean up only data created by that test.

Do not share a mutating account across parallel workers. If setup state can be
reused safely, keep authentication separate from mutable domain data and prove
that tests cannot affect one another.

Make time, randomness, locale, timezone, feature flags, and external responses
deterministic when they influence acceptance. Use the application's supported
control points rather than patching unrelated implementation details.

Retries start a fresh worker but do not erase external effects. Design setup and
cleanup so a failed first attempt cannot poison the retry.

## Network Behavior

Mock third-party services the team does not control. Keep the application-owned
request path real when it is the behavior under test.

When routing requests:

- scope the route narrowly;
- validate request method and relevant payload;
- return a realistic synthetic response;
- assert that the expected request occurred;
- remove broad catch-all routes that can mask unexpected traffic.

Recordings and archives may contain headers, cookies, bodies, and personal data.
Do not commit them without review and sanitization.

## Browser and Visual Coverage

Use configured Playwright projects rather than hand-written user-agent strings.
Add browsers and devices based on the support contract. A resized desktop
viewport is not equivalent to a real device profile.

For visual comparisons, control browser version, operating system, fonts,
animation, dynamic data, and viewport. Review baseline changes as product
changes, not automatic noise updates. Pair images with semantic assertions for
behavior that pixels cannot prove.

Accessibility scans supplement, but do not replace, role-based interaction,
keyboard paths, focus behavior, names, states, and human review.

## Maintainability

Keep tests independent, descriptive, and close to user terminology. Extract a
fixture or page object only when it removes stable repeated behavior without
hiding assertions or navigation.

Avoid helper names such as `safeClick` that retry side effects or suppress the
reason an action was impossible. Let Playwright actionability and assertions
fail at the first meaningful divergence.

Review changed shared fixtures and configuration against another consumer before
running the broader suite.
