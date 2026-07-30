---
name: core-development-openapi-standards
description: OpenAPI documentation standards for schema-first APIs and validation.
---

# OpenAPI Standards

- Keep API schemas as the source of truth.
- Pin the OpenAPI feature version supported by the active validators,
  generators, and consumers; do not mix Schema Object or JSON Schema semantics
  from different minor versions.
- Document all endpoints, params, request/response bodies, and error codes.
- Provide examples for each endpoint.
- Use tags to organize endpoints logically.
- Generate docs and clients automatically from schemas.
- In CI, validate the fully resolved description and its examples, then compare
  it with the approved compatibility baseline. For a new API, establish that
  baseline explicitly; otherwise a missing baseline makes compatibility
  unverified and must not pass the compatibility gate. Reject breaking changes
  unless an approved versioning and migration decision updates that contract.
