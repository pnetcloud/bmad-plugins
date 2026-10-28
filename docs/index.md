# pnet BMad Plugins

`pnet-bmad-plugins` is the public distribution repository for installable BMad plugins.

## Public Scope

- Published plugin payloads
- Public marketplace manifest
- Public documentation

## Install

Install BMad first:

```bash
npx bmad-method install
```

Then install this repository as a custom plugin source:

```bash
npx bmad-method install --custom-source https://github.com/pnetcloud/bmad-plugins --tools claude-code --yes
```

For local development:

```bash
npx bmad-method install --custom-source /path/to/bmad-plugins --tools claude-code --yes
```

## Current Plugins

### `pnet`

This packaged plugin ships the `skill-improver` meta-skill for bounded, security-aware improvement of existing Agent Skills.

### `pnet-marketing`

This package contains 40 entries: on-page SEO implementation, 26 claude-seo knowledge imports, 12 LinkedIn workflows and one email-marketing manual. See the [marketing catalog](../plugins/marketing/README.md) for IDs and host/runtime prerequisites.

### `pnet-business-product`

This packaged plugin ships grouped business, product, planning, research, and documentation skills.

### `pnet-core-development`

This package contains 34 development and architecture entries, including eight imported PostgreSQL/TimescaleDB, Redis and Stripe guides. See the [development catalog](../plugins/core-development/README.md).

### `pnet-infrastructure`

This package contains nine infrastructure and DevOps entries, including Cloudflare product-selection knowledge. See the [infrastructure catalog](../plugins/infrastructure/README.md).

### `pnet-language-specialists`

This packaged plugin ships grouped language and framework specialist skills for Go, React, and TypeScript.

### `pnet-qa`

This packaged plugin ships QA-oriented skills for browser automation and Playwright workflows.

## Repository Scope

This repository contains the public distribution artifacts for installable BMad plugins.

## Instruction Contract

Packaged skills follow the [collection instruction standard](../plugins/pnet/skills/skill-improver/references/instruction-standard.md):
Purpose and selection, Working mode, Focus, Quality checks, Return, and Boundaries.
The shared entry contract preserves specialist roles, concise technical standards
and tool workflows rather than replacing them with one generic procedure.
Stable skill IDs and packaged resource paths remain the installation contract.

Repository format check and parser regression tests:

```bash
python3 scripts/check_instruction_contracts.py
python3 -m unittest discover -s scripts/tests -p 'test_*.py'
```

Format validation is not proof of domain correctness or adoption by live sessions.

## Catalog, dependencies and migration

The registry has seven plugins and 105 top-level skills (57 existing stable IDs
plus 48 group-qualified imports). Unchanged groups contain 16 business/product,
three language-specialist, two QA and one pNet entry. See the
[root catalog](../README.md#catalog-and-migration-boundaries) for the full count table.

Use [the public migration map](imported-skill-map.json) to review old-to-new
consumer references and collisions; it is not native alias registration and
never deletes old installations. Only imported public IDs, package paths,
immutable upstream URLs and license expressions are included.

Imports are static knowledge/resources, not installed runtimes or permissions.
The 26 claude-seo entries require a separately installed, checked original runtime
and actual host/provider bindings before operations. They do not register native
agents or slash commands. SEO assessment hands code changes to
`marketing-on-page-seo-implementation`. LinkedIn, email, database, Stripe and
Cloudflare workflows retain their own dependency and approval requirements.
Catalog validation does not verify live API behavior or certify a release.

## Rights and attribution

The root MIT license covers collection-owned material, not every imported file.
Aggregate component expression: `MIT AND Apache-2.0 AND CC-BY-4.0`.
Consult the [third-party rights guide](third-party-licenses.md), per-entry origins,
full licenses and notices before redistribution; no upstream endorsement or
legal certification is implied.
