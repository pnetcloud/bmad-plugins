---
name: core-development-docs-general
description: General documentation structure, organization, and maintenance standards for the docs/ directory.
---

# Documentation Standards (General)

## Purpose

The `docs/` directory is the single source of truth for project documentation. It covers technical, business, operational, and compliance knowledge.

## Structure (canonical)

- `api/` — API reference, endpoints, schemas, authentication
- `architecture/` — system design, components, events, data flows, technologies
- `business/` — monetization, pricing, business model
- `compliance/` — regulations, GDPR, PCI DSS, ISO, audits, certifications
- `deployment/` — production setup, docker/k8s, CI/CD pipelines
- `development/` — coding standards, patterns, guidelines, testing
- `governance/` — ADR, RFC, decision-making, stakeholder management
- `integration/` — external systems, APIs, webhooks, SDKs
- `knowledge-base/` — onboarding, FAQ, glossary, how-to guides
- `marketing/` — strategy, positioning, go-to-market
- `operations/` — monitoring, runbooks, maintenance, incident response
- `security/` — security policies, threat models, checklists
- `testing/` — QA, automation, test plans
- `ui-ux/` — design, research, user/admin interfaces
- `planning/` — roadmap, tasks, requirements

Key documents:
- `README.md` — entrypoint, navigation guide
- `SUMMARY.md` — project summary and quick status
- `ARCHITECTURE.md` — architecture overview
- `API_DOCUMENTATION.md` / `API_EXAMPLES.md` — API quick access

## Usage Guidelines

- Each folder must have a `README.md` with overview and links.
- Keep documents short, structured, and cross-linked; avoid duplication.
- Use Markdown with headings, tables, and code blocks.
- File naming: `snake-case.md`.

## Best Practices

- Keep docs in sync with code changes.
- Use ADRs inside `architecture/` for major changes.
- Update OpenAPI schemas with each API change.
- Maintain security and compliance checklists.

## Reference

- `docs/README.md` (navigation guide)
- `docs/SUMMARY.md` (status overview)
