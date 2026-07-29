# Kubernetes Delivery Review

Use only for Kubernetes manifests, cluster previews, deployments, or diagnosis.

## Contents

- Target identity and authority
- Manifest review
- Security and data boundaries
- Validation ladder
- Rollout and recovery

## Target Identity and Authority

For cluster-connected work, resolve and keep visible:

- current context and server identity;
- namespace and release or workload name;
- actor permissions;
- source of truth and active reconcilers;
- platform and API versions;
- maintenance, disruption, and rollback boundaries.

Cluster names, server addresses, object data, and command output may be private.
Keep them out of public artifacts. Read access does not authorize mutation, and
namespace mutation does not authorize cluster-scoped changes.

## Manifest Review

- Use API versions supported by the target and check deprecations.
- Make names, recommended labels, selectors, ports, and cross-resource
  references consistent.
- Review immutable fields and ownership before changing selectors, storage, or
  workload identity.
- Use an immutable image identity for release objects and set pull behavior to
  match the promotion contract.
- Separate startup, readiness, and liveness semantics. A liveness probe must not
  kill a process merely because a dependency is unavailable.
- Derive CPU, memory, ephemeral storage, replica, autoscaling, and disruption
  settings from measurements and service objectives, not a template.
- Define termination grace and lifecycle behavior so draining and rollout do
  not lose accepted work.
- Use topology, affinity, tolerations, and node selection only for demonstrated
  scheduling requirements.
- Disable automatic service-account token mounting when the workload does not
  call the API.
- Prefer non-root execution, no privilege escalation, a default seccomp
  profile, dropped capabilities, and read-only roots where the application
  contract supports them.

## Security and Data Boundaries

Kubernetes Secret values are not inherently encrypted merely because they use a
Secret object. Keep material out of source, generated examples, rendered charts,
diffs, command arguments, logs, and receipts. Follow the platform's approved
encryption and external delivery model.

RBAC must list only required API groups, resources, verbs, names, and scope.
Remember that permission to create workloads can enable indirect access to
namespace data or privileged service accounts.

NetworkPolicy behavior depends on the installed network implementation. Review
default ingress and egress stance, name resolution, external dependencies,
control-plane communication, monitoring, and emergency access. Prove enforced
behavior; a valid object alone is not a boundary.

Review host networking, host paths, devices, privileged execution, elevated
capabilities, unsafe sysctls, and node-level identities as high-risk exceptions.

## Validation Ladder

1. Format, schema, and policy checks using repository-pinned versions.
2. Render overlays or generators and inventory the exact resulting objects.
3. Compare against supported APIs for the intended platform.
4. With authorized cluster read access, confirm context, namespace, permissions,
   existing owners, immutable fields, quotas, policies, and admission behavior.
5. Use server-side dry run only against the reviewed target. It sends objects to
   the API and can invoke admission integrations.
6. Use a bounded diff only after protecting its output. A difference exit status
   is not the same as a command error, and rendered differences may expose data.
7. Classify creates, patches, replacements, deletions, hooks, and indirect
   effects before approval.

Do not apply an unresolved directory, pipe remote content into the client, or
change context inside a combined mutation command.

## Rollout and Recovery

Before mutation, record current generation, image identity, replica health,
events, and the rollback or forward-fix option. Apply exactly the reviewed
objects once and observe:

- API acceptance and ownership conflicts;
- rollout progress and timeout reason;
- scheduling, image pull, probe, and admission events;
- availability and disruption;
- application and dependency health;
- the requested external outcome.

On timeout, inspect current generation and replica state before retrying.
Rollback is itself a mutation and requires confirmation of the target revision
and any incompatible schema, state, or data changes.

Do not call a release healthy from client exit status, desired replica count,
or pod phase alone.
