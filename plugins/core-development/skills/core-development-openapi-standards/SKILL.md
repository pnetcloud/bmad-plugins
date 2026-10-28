---
name: core-development-openapi-standards
description: OpenAPI documentation standards for schema-first APIs and validation.
---

# OpenAPI Standards

## Purpose and selection

Use for schema-first OpenAPI descriptions, documentation, generated clients, and contract compatibility review. Do not use it to redesign an API or migrate specification versions without a requested contract change.

## Working mode

Locate the authoritative description, reference-resolution inputs, selected OpenAPI version, generators, consumers, and approved compatibility baseline. Use repository tooling; ask for a missing authority or version decision rather than inventing a baseline.

- Generate docs and clients automatically from schemas.

## Focus

- Keep API schemas as the source of truth.

- Within OpenAPI 3.x, pin the feature version supported by the active
  validators, generators, and consumers; do not mix Schema Object or JSON
  Schema semantics from different minor versions.

- Document all endpoints, params, request/response bodies, and error codes.

- Provide examples for each endpoint.

- Use tags to organize endpoints logically.

## Quality checks

- In CI, validate the fully resolved description and its examples, then compare
  it with the approved compatibility baseline. For a new API, establish that
  baseline explicitly; otherwise a missing baseline makes compatibility
  unverified and must not pass the compatibility gate. Reject breaking changes
  unless an approved versioning and migration decision updates that contract.

## Return

Return the schema or review findings, applicable OpenAPI and baseline revisions, validation and generation results, and any unresolved compatibility or consumer impact.

## Boundaries

Changing a published contract, replacing a compatibility baseline, regenerating externally consumed clients, or publishing docs requires the corresponding approval. A validator passing is not permission to accept an incompatible API change.
