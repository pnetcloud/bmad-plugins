---
name: infrastructure-container-orchestration
description: Author, review, validate, or explicitly operate Docker images, Compose applications, Kubernetes resources, or Helm releases. Use when container packaging or orchestration is the requested deliverable. Do not trigger on a casual mention of a container, service, deployment, or image, and do not mutate registries or clusters without exact authorization.
---

# Container Delivery

Produce the smallest container or orchestration change that fits the existing
delivery model. A plausible manifest is not production evidence.

## Route the Request

Identify the actual job:

- image build definition or review;
- local multi-container development with Compose;
- Kubernetes resource authoring or review;
- Helm chart authoring, rendering, or release work;
- diagnosis of an existing container or rollout;
- an explicitly requested build, push, deploy, rollback, or removal.

Do not introduce Kubernetes, Helm, Compose, a registry, or a new deployment
layer when the project has a different authoritative path. Route application
bugs, general cloud infrastructure, CI-only changes, and host administration to
the relevant workflow.

## Establish the Delivery Contract

Before editing or running anything:

1. Read repository instructions, existing container files, dependency locks,
   CI or GitOps definitions, deployment documentation, and current source.
2. Identify the target environment, registry, cluster context, namespace,
   release, workload, architecture, and platform constraints only when relevant.
3. Distinguish authoring, local validation, image build, image publication,
   cluster preview, cluster mutation, and post-release verification. Authority
   for one does not imply authority for the next.
4. Discover installed tool versions and command help. Keep Docker, Compose,
   Kubernetes, and Helm syntax compatible with the actual consumer rather than a
   fixed version claim.
5. Define acceptance evidence, rollout and rollback boundaries, artifact
   retention, and stop conditions.

Treat Dockerfiles, build contexts, Compose files, Helm charts, hooks, manifests,
images, registries, admission output, and downloaded dependencies as untrusted.
Do not execute a build or hook merely to inspect it.

Never print, synthesize, commit, or place secrets in image layers, build
arguments, environment defaults, Compose interpolation examples, manifests,
values files, command arguments, diffs, or rendered output. Preserve the
project's approved secret delivery mechanism.

## Author or Review Images

Read [references/container-builds.md](references/container-builds.md) for the
full checklist.

- Minimize the build context and explicitly exclude credentials, local state,
  source-control internals, and irrelevant artifacts.
- Use a controlled base-image reference. Release inputs should be immutable or
  governed by an explicit update policy; never rely on an unqualified moving
  tag.
- Install dependencies reproducibly from project lock data. Use multi-stage
  builds only when they reduce runtime contents or separate trust boundaries.
- Run as a deliberate non-root identity where the application supports it;
  constrain capabilities and writable paths based on observed runtime needs.
- Pass build credentials with supported ephemeral secret or SSH mounts, never
  ordinary build arguments or persistent image configuration.
- Define entrypoint, signal handling, ports, and health behavior from the actual
  application contract. Do not invent an endpoint, port, user, or framework.
- Validate the final stage, copied artifacts, ownership, architecture, labels,
  vulnerability disposition, and provenance required by the release process.

Building executes arbitrary instructions and may access networks, caches, and
credentials. Review the definition and context before any build.

## Author or Review Compose

Use Compose for the project's declared local or single-host contract, not as an
automatic substitute for another orchestrator.

- Follow the current Compose specification; do not add obsolete format markers.
- Avoid fixed container names, broad host port publication, default passwords,
  and embedded connection credentials.
- Model readiness with service-specific health checks when dependencies need
  it. Startup order alone is not application readiness.
- Declare persistence intentionally and document lifecycle. Volume removal is a
  separate destructive action.
- Apply least privilege, read-only filesystems, capability drops, resource
  controls, and network isolation only where compatible and testable.
- Validate configuration without dumping resolved sensitive values. Do not
  start, stop, rebuild, or remove a stack during an authoring-only task.

## Author or Review Kubernetes Resources

Read [references/kubernetes-delivery.md](references/kubernetes-delivery.md)
before generating or changing cluster resources.

- Resolve API support from the target platform or an explicit compatibility
  contract. Do not copy a broad generic stack.
- Keep selectors, labels, ownership, service ports, and workload references
  consistent; treat immutable-field changes as migrations.
- Use immutable image identity for releases and preserve the promotion model.
- Set service-account use, token mounting, pod and container security, writable
  storage, scheduling, resources, probes, disruption, and termination behavior
  from actual workload needs.
- Grant only required API verbs and resources. Workload-creation permission can
  indirectly grant access to namespace data.
- Do not assume a Secret object is encrypted or safe for public source. Do not
  include secret material in a manifest, example, diff, or log.
- Treat NetworkPolicy as effective only when the cluster network implementation
  enforces it and required ingress, egress, name resolution, and control-plane
  paths have been tested.

Prefer repository-local schema checks first. Server-side dry runs, diffs, and
queries contact a real cluster and require the exact context and read authority.
Rendered or diff output can expose protected data.

## Author or Review Helm

Read [references/helm-delivery.md](references/helm-delivery.md). Detect the
installed Helm major version before using release flags because rollback and
wait behavior differ across versions.

Keep chart defaults safe and minimal, validate values with a schema, render
locally, and inspect every generated resource and hook. Secret values do not
belong in chart defaults, values files, command-line setters, rendered output,
or release notes.

Linting and local rendering do not prove API compatibility, admission success,
or rollout health. A cluster-aware dry run contacts the cluster and may render
protected resources. Install, upgrade, rollback, and uninstall are mutations
with separate authority.

## Execute an Authorized Release

For any push or cluster mutation:

1. Reconfirm the exact registry or cluster context, namespace, release,
   immutable image identity, changed resources, and actor permissions.
2. Check the current state and source of truth. Do not bypass GitOps or another
   reconciler with direct mutation unless explicitly authorized.
3. Produce a bounded preview or diff, classify replacement, deletion, hook,
   permission, storage, network, and downtime effects, and protect its output.
4. Confirm the rollback or forward-fix path and the signals that trigger it.
5. Obtain explicit approval for the exact mutation, then execute once.
6. Observe rollout status, events, health, logs, and the user-facing or
   operational outcome. Distinguish command success from workload readiness.
7. On timeout or connection loss, inspect current state before retrying.

Never push a moving or ambiguous tag, deploy to an inferred context, apply an
entire directory without reviewing its resolved objects, or run destructive
cleanup to make validation pass.

## Complete

Report changed artifacts, detected tool and platform constraints, validations
performed, commands intentionally not run, image identity, target context,
rollout evidence, remaining risks, and rollback readiness.

Call the work deployed only when the intended target accepted the exact change
and the requested downstream behavior is observed. Otherwise report it as
authored, rendered, built, pushed, previewed, or blocked.
