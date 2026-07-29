# Container Build and Compose Review

Use only for Dockerfile, image-build, or Compose work.

## Contents

- Evidence to collect
- Dockerfile decisions
- Build validation
- Compose decisions
- Publication gate

## Evidence to Collect

- Existing build and runtime definitions, ignore files, lockfiles, and CI calls.
- Supported target architectures and runtime platform.
- Required runtime files, user identity, ports, signals, writable paths, and
  health semantics.
- Registry naming, immutable versioning, signing, provenance, SBOM, and
  vulnerability policy.
- Build-network and credential needs.
- Compose purpose, service dependencies, persistence, host exposure, and
  cleanup expectations.

Do not select a base image, package manager, port, health endpoint, or user ID
from a generic template.

## Dockerfile Decisions

- Use a current frontend syntax only when required by used features.
- Pin release base images by digest or enforce an equivalent controlled update
  policy. Record how security updates reach that pin.
- Copy dependency declarations before frequently changing source only when it
  improves caching without omitting generated or workspace dependencies.
- Use deterministic dependency installation and fail on lock drift.
- Keep compilers, package caches, credentials, and test-only dependencies out of
  the runtime stage.
- Use `COPY` by default. Review remote sources and automatic archive extraction
  before using broader add behavior.
- Use ephemeral BuildKit secret or SSH mounts when a build must authenticate.
  Ordinary arguments and image environment configuration persist or leak.
- Ensure the runtime identity owns only required files. Avoid recursive
  ownership changes over large copied trees when ownership can be set at copy.
- Prefer exec-form startup, deliberate signal handling, and an init process only
  when the application needs one.
- Add a health check only when the command exists in the final image and the
  endpoint represents the intended health dimension.
- Do not install diagnostic tools in the runtime image solely to support a
  health check.
- Make read-only root filesystems and temporary mounts an orchestrator decision
  when the image cannot express required writable paths alone.

## Build Validation

Validation should advance deliberately:

1. Parse or lint using the repository's pinned tooling.
2. If supported by installed help, run build checks that do not execute stages.
3. Review the exact context and Dockerfile before a real build; build steps are
   executable code.
4. Build the required target and architecture without publishing it.
5. Inspect the resulting configuration, layers, user, entrypoint, copied
   artifacts, and health command.
6. Run focused application and shutdown tests in a contained environment.
7. Generate or verify the required vulnerability, SBOM, signature, and
   provenance evidence with project-approved tools.

A successful build does not prove runtime correctness, supply-chain safety, or
publish success.

## Compose Decisions

- Use the current `compose.yaml` model and repository naming conventions.
- Let Compose scope resource names unless a stable external contract requires
  an explicit name.
- Publish only host ports the user must reach. Bind local-only services to the
  narrowest interface and avoid publishing databases or caches by default.
- Use internal service discovery rather than host-loopback assumptions.
- Do not provide usable default credentials. Integrate the project's approved
  secret source and keep values out of resolved output.
- Health checks should validate the dependency condition the consumer needs;
  a running process is not necessarily ready.
- Mark bind mounts, named volumes, and ephemeral data distinctly. Document what
  survives recreation and what removal deletes.
- Keep development source mounts and debug commands out of the production
  profile unless explicitly selected.
- Review privilege, device, host namespace, socket, capability, and host
  filesystem access as high-risk exceptions.

Use quiet configuration validation when supported. Avoid printing the fully
interpolated model because it can reveal protected values. Starting services
executes image entrypoints; stopping or recreating them changes local state;
removing volumes deletes data.

## Publication Gate

Before pushing:

- Resolve the exact registry, repository, immutable tag, and local image digest.
- Confirm authentication exists without reading or printing it.
- Ensure the tag does not overwrite a protected or ambiguous release.
- Confirm multi-architecture manifest contents when applicable.
- Run required signing, attestation, SBOM, and scanning gates.
- Push once, then verify the remote digest and required metadata.

Do not infer remote publication from a successful local build or a zero exit
code alone.
