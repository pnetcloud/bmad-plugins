# Helm Chart and Release Review

Use only for Helm chart authoring, rendering, packaging, or release operations.

## Contents

- Chart contract
- Local validation
- Cluster-aware preview
- Release mutation

## Chart Contract

- Detect the installed Helm major version and target Kubernetes compatibility.
- Preserve established chart naming, labels, ownership, dependency, and values
  conventions.
- Keep default values minimal and safe. Do not invent production sizing,
  ingress classes, storage classes, issuers, autoscaling, or disruption policy.
- Define a values schema for required fields, types, ranges, and mutually
  dependent settings.
- Keep selectors stable and centralize repeated names and labels in helpers.
- Quote strings deliberately and test false, zero, empty, and omitted values.
- Pin and review chart dependencies and repositories; update lock data through
  the project's controlled process.
- Treat hooks as executable cluster mutations with ordering, deletion, retry,
  and rollback consequences.
- Keep protected values out of chart defaults, checked-in values, command-line
  setters, release notes, tests, and rendered fixtures.

## Local Validation

Use the installed command help for syntax. Start with:

1. chart linting using each supported values variant;
2. local template rendering with debug output protected;
3. values-schema validation;
4. inventory of rendered kinds, names, namespaces, hooks, and cluster-scoped
   objects;
5. Kubernetes schema and policy checks using target-compatible tools;
6. semantic checks for selectors, ports, security, resources, probes, and
   immutable fields.

Local rendering does not contact the API, resolve all capabilities, execute
lookup behavior, or prove admission and rollout.

Rendered output can contain protected values even during a dry run. Do not print
or retain it broadly. Prefer redacted summaries and protected temporary
artifacts when full inspection is necessary.

## Cluster-Aware Preview

Cluster-aware dry runs, lookups, release reads, and diffs require exact context,
namespace, release, and read authority. They can invoke API or admission
behavior and reveal live or rendered data.

Before a release preview:

- confirm the current release revision, chart identity, and values sources;
- identify cluster-scoped resources and objects shared with other releases;
- classify hook execution behavior;
- distinguish create, patch, replacement, deletion, and ownership conflict;
- verify that another reconciler will not revert or duplicate the change.

## Release Mutation

Install, upgrade, rollback, and uninstall are separate mutating intents. Verify
the flags for the installed Helm major version; do not assume that wait,
atomicity, or rollback-on-failure semantics are identical across releases.

For an authorized install or upgrade:

1. bind the exact context, namespace, release, chart, dependency lock, values
   inputs, and immutable image identity;
2. protect values and rendered output;
3. review the bounded diff and hook effects;
4. define timeout, observation, and rollback criteria;
5. confirm the exact mutation;
6. observe release status, Kubernetes rollout, events, hooks, and application
   outcome;
7. verify the deployed revision and image identity.

Do not infer success from Helm's exit status alone. A release record can exist
while workloads are unavailable or the intended external behavior is broken.

For rollback or uninstall, review stateful resources, retention annotations,
hooks, persistent storage, shared objects, and application compatibility first.
