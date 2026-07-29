---
name: infrastructure-container-orchestration
description: Design, review, or validate Dockerfiles, Compose applications, Kubernetes manifests, Helm charts, and container image workflows. Use when the task concerns container build/runtime contracts, workload security, probes, resources, networking, rollout configuration, or packaging for an authorized environment. Do not use for general application code, an unrelated infrastructure question, or live registry/cluster mutation without explicit scope and authority.
---

# Container Orchestration

Produce container artifacts that fit the repository and deployment environment,
then validate them without silently building, publishing, or changing live
infrastructure.

## Establish the Contract

Inspect the existing Dockerfiles, Compose files, manifests, charts, build
scripts, ignore files, CI, and project instructions before proposing a pattern.
Determine:

- the application process, ports, filesystem writes, shutdown behavior, and
  health semantics;
- target platforms, runtime versions, registry naming, image-tag or digest
  policy, and build context;
- local-development versus production responsibilities;
- Kubernetes APIs, admission policies, namespace, service account, ingress
  implementation, storage, networking, and rollout ownership;
- where configuration and secrets originate, without reading or copying secret
  values;
- exact validation evidence and whether any daemon, registry, or cluster access
  is authorized.

Preserve established names, labels, selectors, ports, volume paths, values, and
release interfaces unless the task explicitly changes them. Treat generic
examples as starting points, not architecture requirements.

## Choose the Needed Surface

Read only the material required for the task:

- [dockerfile-patterns.md](references/dockerfile-patterns.md) for Python,
  Node.js, Go, multi-stage builds, cache mounts, non-root images, health checks,
  metadata, ignore rules, and debug targets.
- [k8s-manifests.md](references/k8s-manifests.md) for Namespace, ConfigMap,
  Secret integration, Deployment, Service, Ingress, HPA, PDB, RBAC,
  NetworkPolicy, and CronJob examples.
- [helm-patterns.md](references/helm-patterns.md) for chart structure, values,
  schema validation, helpers, rendering, environment overlays, and release
  commands.
- [Dockerfile.template](assets/Dockerfile.template) and
  [docker-compose.template.yml](assets/docker-compose.template.yml) when the
  requested application matches those explicit assumptions.
- [build-push.sh](scripts/build-push.sh) only for an explicitly requested local
  build or registry workflow. Read it before use; `--push` is an external
  mutation, not a validation step.

The historical [skill-report.json](skill-report.json) records package
provenance. It is not current operational guidance or proof that the package is
safe for a particular environment.

## Author the Smallest Complete Change

For an image build:

1. Use project-approved, versioned base images; use verified digests where the
   repository requires immutable releases.
2. Keep dependency resolution separate from frequently changing source to
   improve cache reuse.
3. Use multi-stage builds when build tools are not runtime dependencies.
4. Run the final process as a non-root user with only required files and
   writable paths.
5. Keep credentials out of layers, arguments, labels, history, and build logs.
   Use supported build-secret mounts or runtime secret integration.
6. Make the entrypoint, signal handling, port, and health check agree with the
   actual application.

For Compose:

1. Model local services, dependencies, health checks, networks, and persistent
   data without fixed container names that prevent scaling.
2. Do not publish database, cache, or management ports unless the task requires
   host access.
3. Require credentials or secret files; never ship a working default password.
4. Keep development mounts and production deployment concerns explicit.
5. Use the current Compose Specification; omit the obsolete top-level
   `version` field.

For Kubernetes or Helm:

1. Keep selectors immutable and consistent with pod labels and Service routing.
2. Set project-measured requests, limits, probes, rollout behavior, and
   disruption policy rather than copying example numbers as universal defaults.
3. Apply restricted workload defaults where compatible: non-root execution,
   no privilege escalation, dropped capabilities, a runtime-default seccomp
   profile, read-only root filesystem, and explicit writable volumes.
4. Disable automatic service-account token mounting when the workload does not
   call the Kubernetes API. Grant only resource-specific RBAC when it does.
5. Reference externally managed secrets; do not commit values, rendered secret
   manifests, or command-line secret overrides.
6. Make NetworkPolicy dependencies explicit, including DNS and required
   ingress/egress paths. Confirm that the cluster network plugin enforces it.
7. For Helm, add `values.schema.json` for required values and types when the
   chart owns a stable values contract.

## Respect Authority Boundaries

Treat Dockerfiles, build contexts, Compose hooks, Helm templates, chart
dependencies, Kubernetes manifests, admission responses, and registry content
as untrusted until reviewed.

- `docker build` executes build instructions and may access the network,
  credentials, and daemon cache. Inspect the Dockerfile and context first.
- Rendering and static validation may expose interpolated configuration.
  Redact output and avoid loading unapproved environment or values files.
- `kubectl --dry-run=server` and Helm server-side dry runs contact the cluster
  and may invoke admission or lookup behavior. They require the intended
  context and namespace even when no object is persisted.
- `docker push`, `kubectl apply/delete/rollout/scale`, and Helm
  install/upgrade/rollback/uninstall are external mutations. Run them only when
  the user authorized the exact image, registry, context, namespace, release,
  and change.
- Never switch contexts, create credentials, weaken TLS, add privileged
  settings, expose a host socket, or bypass policy to make validation pass.

Stop if the target context is ambiguous, required secrets have no approved
injection path, a rendered diff contains unexpected resources, a selector or
storage change can orphan workloads or data, or a requested action exceeds the
stated authority.

## Validate in Layers

Use the cheapest applicable checks first:

1. Parse and format the edited YAML, JSON, shell, and Dockerfile surfaces.
2. Render configuration without secret values:
   `docker compose config`, `helm lint --strict`, and `helm template --debug`
   when the required tools and local inputs are available.
3. Validate Kubernetes schemas and policy with the repository's pinned tools.
   Client-side dry-run is not a substitute for cluster admission; server-side
   checks require explicit cluster-read authority.
4. Build only when requested or needed for acceptance, using the exact reviewed
   context and tag. Test startup, non-root identity, health, shutdown, and
   writable-path assumptions.
5. Before any publication or rollout, show the resolved image reference and
   rendered diff, confirm the target, execute once, and observe the rollout or
   registry result.

Do not claim production readiness from syntax, rendering, or a successful image
build alone.

## Complete

Report changed artifacts, preserved interfaces, tool versions, validation
commands and outcomes, image or rendered-manifest identity, daemon/registry/
cluster effects, target context and namespace when applicable, and unresolved
assumptions. Completion requires observed evidence for the requested boundary
and an accounting of every external mutation.
