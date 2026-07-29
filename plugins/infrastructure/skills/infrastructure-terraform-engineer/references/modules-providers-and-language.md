# Modules, Providers, and Terraform Language

Use this reference for configuration structure and language decisions. Current
repository and selected-version behavior override generic patterns.

## Contents

- Root and child modules
- Providers and versions
- Inputs, outputs, and locals
- Resource identity and meta-arguments
- Data sources, helpers, and provisioners
- Repository, registry, and composition strategies

## Root and Child Modules

- Keep a root module as the composition and operational boundary: backend,
  provider configurations, environment inputs, module wiring, and root outputs.
- Give a child module one coherent capability and an explicit ownership
  boundary. Reuse is an outcome of stable shared semantics, not a percentage.
- Prefer composition over deeply nested wrappers. A facade or composite module
  is useful only when it owns a stable cross-resource contract; factory-like
  repetition often hides distinct lifecycle and policy decisions.
- Data-only modules can package a stable lookup contract, but direct provider
  data sources may be clearer when no reusable policy exists.
- Document inputs, outputs, created resources, provider requirements,
  side-effects, upgrade/migration notes, examples, and support boundaries.
- Version published modules from their compatibility contract. Do not publish,
  tag, or update a registry without explicit authority.

## Providers and Versions

- Root modules own provider configurations and pass provider aliases explicitly to child
  modules. Child modules declare required provider source addresses and
  compatible constraints without embedding environment credentials.
- Add aliases only for real multi-region/account/project relationships. Track
  the provider instance for every resource and import/move.
- Constrain Terraform, providers, and external modules narrowly enough for
  compatibility and broadly enough for intended upgrades. Exact constraints
  are not universally safer; follow project release policy.
- Commit and review the dependency lock file according to repository policy.
  An initialization or upgrade that changes selections, checksums, sources, or
  platforms is a dependency change, not incidental noise.
- Inspect provider changelogs and schemas for default, validation, state,
  migration, sensitive-value, replacement, and deprecation changes before
  upgrade.
- Apply the same evidence rule to public-cloud, Kubernetes, Helm,
  secret-management, and other specialized providers; provider families do not
  share configuration, lifecycle, identity, or import semantics merely because
  Terraform can compose them.
- Custom provider development is a separate software project with protocol,
  schema/state migration, acceptance tests, release, signing, and supply-chain
  responsibilities. Do not improvise one to avoid configuration design.

## Inputs, Outputs, and Locals

- Use precise object, collection, optional-field, and nullability types. A
  default is a product decision; omit it when callers must choose.
- Validate stable domain constraints at module boundaries. Provider-dependent
  or frequently changing facts may need preconditions, checks, or runtime
  validation instead of hardcoded variable rules.
- Keep variable files environment-scoped and non-sensitive when committed.
  Use the approved credential/secret mechanism for runtime secrets.
- `sensitive` redacts selected UI output but can still leave values in state or
  plans. Use ephemeral values or provider write-only arguments only when the
  selected Terraform/provider versions support the full flow.
- Make outputs intentional contracts; avoid exporting entire resources or
  sensitive/high-churn implementation detail.
- Use locals to name and reuse expressions, not to build an opaque second
  programming language. Keep complex transformations tested and documented.

## Resource Identity and Meta-Arguments

- Choose `for_each` for stable domain keys and `count` for genuinely positional
  interchangeable instances. Changing between them or changing keys is an
  address migration.
- Use explicit references for real dependencies. Add `depends_on` only for a
  hidden behavioral dependency that cannot be expressed through data flow, and
  document why.
- Use lifecycle rules deliberately:
  - `create_before_destroy` needs quotas, names, cost, and coexistence support;
  - `prevent_destroy` is a guardrail, not backup or authorization;
  - `ignore_changes` requires an external owner and drift contract;
  - replacement triggers require availability and data review.
- Dynamic blocks reduce repeated nested syntax but can obscure shape and
  source. Prefer literal blocks or module decomposition when clearer.
- Keep conditionals type-consistent and make disabled-resource outputs safe.
  Test both branches and address changes.
- Use preconditions, postconditions, and check blocks for meaningful invariants
  supported by the selected version; understand whether failure blocks plan,
  apply, or only reports a warning.

## Data Sources, Helpers, and Provisioners

- Data sources are remote reads with credentials, availability, freshness, and
  sensitivity concerns. Bound ambiguous searches and avoid selecting resources
  by unstable “latest” behavior without an explicit contract.
- Prefer built-in functions and declarative resources. Time-based resources,
  null-like helper resources, and external data programs introduce lifecycle,
  nondeterminism, portability, input-validation, and supply-chain concerns.
- Provisioners are a last-resort bridge. Define interpreter, platform,
  credentials, idempotency, timeout, failure, retry, logs, cleanup, and
  replacement behavior. Never use a local provisioner to smuggle an
  unreviewed infrastructure mutation into apply.
- External programs and templates receive untrusted values. Use structured
  serialization and avoid shell interpolation.

## Repository, Registry, and Composition Strategies

Choose mono-repository, multiple repositories, module registry publication, and
environment roots from ownership, release cadence, permissions, discovery,
compatibility, and state blast radius. Do not copy modules merely to avoid a
release process.

For each shared module define owners, supported versions, upgrade policy,
examples/tests, deprecation window, security response, registry provenance, and
consumer migration evidence. Knowledge sharing and training should use current
verified examples rather than undocumented tribal procedure.
