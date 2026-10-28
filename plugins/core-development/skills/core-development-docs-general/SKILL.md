---
name: core-development-docs-general
description: Organize and maintain project documentation while preserving repository-specific paths, generators, and navigation. Use when creating a documentation layout, adding a documentation category, or reviewing documentation organization. Do not use for prose-only editing that needs no organization, navigation, naming, or maintenance decision.
---

# Documentation Standards (General)

## Purpose and selection

Use for documentation organization, navigation, naming, and maintenance; not prose-only editing with no structural decision.

### Purpose

First follow the repository's existing documentation contract, generators, and
navigation. When none exists, use `docs/` as the source of truth for technical,
business, operational, and compliance knowledge.

## Working mode

Inspect current documentation paths, generators, navigation, and intended readers. Ask for missing audience or ownership decisions only when they block the requested organization.

### Usage Guidelines

- Each folder must have a `README.md` with overview and links.
- Keep documents short, structured, and cross-linked; avoid duplication.
- Use Markdown with headings, tables, and code blocks.
- Follow established file naming; for new projects without a convention, use
  lowercase kebab-case names.

## Focus

### Default Structure

Treat this layout as a menu: create only categories required by current content
and project needs, never empty scaffolding. Preserve established paths and
links, and propose any migration separately.

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

### Reference

- `docs/README.md` (navigation guide)
- `docs/SUMMARY.md` (status overview)

## Quality checks

Verify changed links, navigation, generated/source boundaries, and consistency with the affected code or specification. State checks not run.

### Best Practices

- Keep docs in sync with code changes.
- Use ADRs inside `architecture/` for major changes.
- Update OpenAPI schemas with each API change.
- Maintain security and compliance checklists.

## Return

Return the requested documentation change or layout proposal, affected paths, navigation/check results, and unresolved ownership or migration decisions.

## Boundaries

Do not relocate established documentation, overwrite generated output, or publish a site merely to apply the default layout. A proposed migration requires separate authority.
