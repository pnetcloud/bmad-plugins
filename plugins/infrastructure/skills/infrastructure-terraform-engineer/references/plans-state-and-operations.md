# Plans, State, and Operations

Use this reference for any task that contacts a backend/provider or changes
Terraform's mapping between configuration and remote objects.

## Contents

- Backends, state, and locks
- Plan review
- Apply and recovery
- Imports, moves, removals, and state operations
- Drift and exceptional options

## Backends, State, and Locks

- Treat each state as a concurrency, security, ownership, and blast-radius
  boundary. Record backend type, configuration source, key or workspace
  identity, lineage expectations, encryption/access controls, locking, backup,
  retention, and recovery procedure.
- Verify state locking for every backend that permits concurrent writers;
  backend selection alone does not prove it.
- Do not commit local state, backups, lock metadata, saved plans, crash logs, or
  sensitive variable files. A remote backend does not by itself prove
  encryption, locking, access control, versioning, or recoverability.
- Do not copy state for convenience. State can contain credentials and
  sensitive resource attributes even when CLI output is redacted.
- Investigate a lock before intervention: exact backend/state, holder,
  operation, timestamp, active process/run, and ownership. Force-unlock only
  with explicit authority and proof that no live writer owns the lock.
- Backend migration is a privileged state operation. Back up through the
  supported mechanism, exclude concurrent runs, validate destination access
  and locking, migrate once, verify lineage/resources, and retain a tested
  recovery path.
- Partial backend configuration or injected credentials may be appropriate to
  keep sensitive/runtime values out of source. Follow the repository and
  backend's current supported contract.

## Plan Review

A plan is evidence for one configuration, dependency selection, variable set,
state snapshot, provider view, identity, and time.

- A speculative plan previews intent but is not the executable artifact.
- A saved plan can later be applied, but its binary and JSON forms may contain
  cleartext sensitive values. Restrict access, retention, logs, and artifacts.
- Planning normally refreshes remote objects and evaluates data sources; it can
  contact services, acquire a state lock, incur API effects, or fail on access.
- Review resource addresses and action reasons, not only totals. Inspect create,
  update, delete, replace, read, unknown-after-apply, dependency, lifecycle,
  provider, output, and sensitive changes.
- Correlate replacements with data durability, availability, names/identities,
  quotas, sequencing, and external consumers.
- Resolve unexpected drift and provider changes rather than approving noise.
  Redacted or unknown values require targeted review, not automatic approval.
- In automation, bind approval to the final executable plan and its source
  revision, lock file, variables, state identity, and target. Re-plan after
  relevant drift or artifact invalidation.

## Apply and Recovery

An approval prompt is not a substitute for exact scope and human review.

Before apply, verify:

- saved-plan identity or the final generated plan;
- state/backend and environment identity;
- provider credentials and least-required authority;
- state lock and absence of competing automation;
- deletion/replacement and data-loss review;
- quotas, cost, maintenance window, dependencies, and external owners;
- observation, abort, incident, cleanup, and recovery ownership.

After apply, distinguish complete success, partial success, provider timeout,
interrupted client, uncertain remote result, and state-write failure. Inspect
state and remote reality through approved means before retrying.

Terraform has no general transactional rollback. A reverse configuration can
cause further replacement or data loss. Prefer a reviewed forward repair when
the prior state cannot be recreated safely. Preserve diagnostics and state
evidence without exposing sensitive contents.

## Imports, Moves, Removals, and State Operations

- Prefer configuration-declared import and move/remove mechanisms supported by
  the selected version when they make review and repetition safer.
- For import, define the exact remote identifier, destination address, provider
  alias, ownership, and expected configuration before execution. Import
  associates state; it does not author a complete correct configuration.
- For address moves, map every old instance key to its destination and validate
  a no-destroy plan. Stable `for_each` keys reduce positional churn but still
  require explicit migrations when keys change.
- Removing configuration may propose remote destruction. A supported removed
  declaration can separate “stop managing” from “destroy” only when its exact
  version semantics and ownership decision are verified.
- Treat `state mv`, `state rm`, provider replacement, taint/replacement, and
  direct state pull/push as privileged recovery tools. Capture lineage/serial,
  exact addresses, backup, lock, command, result, and full follow-up plan.
- Never edit state JSON manually as a routine workflow. If extraordinary
  recovery requires it, stop for specialist review, exact backups, isolated
  access, and a rehearsed validation/recovery procedure.

## Drift and Exceptional Options

- Define which drift Terraform should reconcile, preserve, import, or escalate.
  Do not add `ignore_changes` merely to make a plan quiet; name the external
  owner and test the remaining lifecycle.
- Use refresh-only planning only to inspect an intentional state-sync proposal;
  it refreshes data in memory but does not persist the refreshed state. A
  refresh-only apply persists the reviewed state changes and therefore requires
  explicit authority. Both modes can contact providers or the backend and need
  the same identity, target, lock, and sensitive-output safeguards.
- Use resource targeting only for exceptional recovery or documented Terraform
  limitations. Follow with a full plan because targeting can leave hidden
  inconsistency.
- Use forced replacement only with explicit address, replacement impact,
  dependency, data, availability, and cost review.
- Workspaces can select separate state instances but do not automatically
  isolate credentials, accounts, networks, permissions, or blast radius.

## Disaster Recovery

Verify the recovery objective, state backup/version accessibility, backend and
credential availability, provider/plugin versions, remote-object inventory,
restore procedure, concurrent-run exclusion, and post-restore full plan.
A backup that has never been restored is not proven recovery evidence.
