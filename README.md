# pNet BMad Plugins

Public distribution repository for installable BMad plugins maintained in [`pnetcloud/bmad-plugins`](https://github.com/pnetcloud/bmad-plugins).

This repository is focused on publishable plugin payloads, grouped skill packages, and the marketplace manifest consumed by the BMad installer.

## What This Repo Contains

- Installable plugin packages under `plugins/`
- Public marketplace metadata in `.claude-plugin/marketplace.json`
- Lightweight public docs in `docs/`
- Grouped skill knowledge bundles for local or remote BMad installs; runtime dependencies remain separate

## Current Layout

```text
bmad-plugins/
├── .claude-plugin/                     # Marketplace manifest for all public plugins
├── docs/                               # Public docs
├── plugins/
│   ├── pnet/                           # pNet skill-maintenance meta-tools
│   ├── marketing/                      # Marketing and SEO implementation bundle
│   ├── business-product/               # Business and product skill bundle
│   ├── core-development/               # Core software development skill bundle
│   ├── infrastructure/                 # Infrastructure and DevOps skill bundle
│   ├── language-specialists/           # Language and framework specialist bundle
│   └── qa/                             # QA and browser automation bundle
└── scripts/                            # Repo helper scripts
```

Each plugin directory contains:

- `.claude-plugin/plugin.json` - installable plugin manifest
- `skills/` - packaged skill directories shipped to the installer
- `README.md` - package-specific notes

## Skill Naming

Canonical skill IDs should use the folder name, the `name:` field inside `SKILL.md`, and the manifest entry path as the same exact slug.

Standard format:

- `<plugin-slug>-<skill-slug>`

Examples:

- `business-product-business-analyst`
- `core-development-api-designer`
- `infrastructure-terraform-engineer`
- `language-specialists-react-specialist`
- `qa-playwright-skill`

This keeps the installed skill ID globally unique and makes it obvious which plugin owns the skill.

Named third-party or branded skills may stay unprefixed when the short public ID is the more stable identifier.

### Canonicalized Skills

The repository has been normalized so skill folders now use canonical prefixed IDs, except for branded IDs that are intentionally preserved.

- `business-product-confluence`
- `business-product-jira`
- `core-development-data-pipeline-go`
- `core-development-implement-design`
- `agent-browser`
- `skill-improver`

### Validation

Run the repository validator before publishing or adding new skills:

```bash
python3 scripts/check_skill_names.py
```

The validator enforces the canonical convention for packaged skills and allows a small explicit exception list for preserved branded IDs.

## Install

### 1. Install BMad

Install the base BMad toolchain first:

```bash
npx bmad-method install
```

If you want to target Claude Code explicitly:

```bash
npx bmad-method install --tools claude-code
```

### 2. Install This Repository as a Custom Source

Install directly from GitHub:

```bash
npx bmad-method install --custom-source https://github.com/pnetcloud/bmad-plugins --tools claude-code --yes
```

For local development, install from a local checkout:

```bash
npx bmad-method install --custom-source /path/to/bmad-plugins --tools claude-code --yes
```

The installer reads `.claude-plugin/marketplace.json` and exposes these plugin packages:

- `pnet`
- `pnet-marketing`
- `pnet-business-product`
- `pnet-core-development`
- `pnet-infrastructure`
- `pnet-language-specialists`
- `pnet-qa`

## Plugin Catalog

### `pnet`

pNet meta-skills for improving existing Agent Skills with minimal evidence-backed changes, quarantined external research, and bounded validation.

- Publish path: `plugins/pnet`
- Packaged skill path: `plugins/pnet/skills/*`
- Included skills: 1
- Examples: `skill-improver`

### `pnet-marketing`

Marketing knowledge for on-page SEO implementation, SEO assessment, LinkedIn workflows and email campaign safety. See the [complete marketing catalog](plugins/marketing/README.md) for all IDs and dependency boundaries.

- Publish path: `plugins/marketing`
- Packaged skill path: `plugins/marketing/skills/*`
- Included skills: 40
- Examples: `marketing-on-page-seo-implementation`

### `pnet-business-product`

Business, product, planning, research, and documentation skills grouped into one installable package.

- Publish path: `plugins/business-product`
- Packaged skill path: `plugins/business-product/skills/*`
- Included skills: 16
- Examples: `business-product-business-analyst`, `business-product-confluence`, `business-product-jira`

### `pnet-core-development`

Core software development skills across architecture, APIs, backend, frontend, PostgreSQL/TimescaleDB, Redis, Stripe, UI, and documentation. See the [complete development catalog](plugins/core-development/README.md).

- Publish path: `plugins/core-development`
- Packaged skill path: `plugins/core-development/skills/*`
- Included skills: 34
- Examples: `core-development-api-designer`, `core-development-data-pipeline-go`, `core-development-implement-design`

### `pnet-infrastructure`

Infrastructure and DevOps skills for cloud architecture, CI/CD, Kubernetes, Terraform, platform operations and Cloudflare product selection. See the [complete infrastructure catalog](plugins/infrastructure/README.md).

- Publish path: `plugins/infrastructure`
- Packaged skill path: `plugins/infrastructure/skills/*`
- Included skills: 9
- Examples: `infrastructure-cloud-architect`, `infrastructure-kubernetes-specialist`, `infrastructure-terraform-engineer`

### `pnet-language-specialists`

Language and framework specialist skills for focused implementation guidance.

- Publish path: `plugins/language-specialists`
- Packaged skill path: `plugins/language-specialists/skills/*`
- Included skills: 3
- Examples: `language-specialists-golang-pro`, `language-specialists-react-specialist`, `language-specialists-typescript-pro`

### `pnet-qa`

QA-oriented browser automation and testing skills.

- Publish path: `plugins/qa`
- Packaged skill path: `plugins/qa/skills/*`
- Included skills: 2
- Examples: `agent-browser`, `qa-playwright-skill`

## Catalog and migration boundaries

The seven existing plugin identities contain 105 top-level skill entries: the
57 existing IDs remain unchanged and 48 imports use group-qualified IDs.

| Plugin | Skills |
| --- | ---: |
| `pnet` | 1 |
| `pnet-marketing` | 40 |
| `pnet-business-product` | 16 |
| `pnet-core-development` | 34 |
| `pnet-qa` | 2 |
| `pnet-infrastructure` | 9 |
| `pnet-language-specialists` | 3 |

For migration from upstream skill names, use the public-only
[old-to-new skill map](docs/imported-skill-map.json). It lists only the 48 imports,
public package paths, immutable upstream sources and component license expressions.
Review consumer references and collisions before switching to the new IDs; this is
not an alias registry and does not remove old installations automatically.
In particular, upstream `stripe-best-practices` maps to
`core-development-stripe-integration-guidance`, not the existing
`core-development-stripe-best-practices` entry.

Imported entries are static knowledge with retained resources, not runtime
activation. The 26 claude-seo entries require a separately installed and checked
original claude-seo runtime and actual host/provider bindings for operations;
see their Working mode contracts and the marketing catalog. This plugin
does not install slash commands or native agents or grant tools and permissions.
`marketing-on-page-seo-implementation` owns code implementation; assessment
entries return findings and handoffs. Other imported tool workflows likewise
require their declared dependencies and task-specific authority.
Catalog, naming and Markdown checks do not certify runtime compatibility,
live APIs, deployment, release readiness or adoption by active sessions.

## Repository Scope

This repository contains the public distribution artifacts for installable BMad plugins. It is intended to stay focused on packaged outputs rather than source authoring workflows.

## Notes

- Marketplace metadata is published from `.claude-plugin/marketplace.json`
- Installable payloads live under `plugins/*`
- Plugin-specific manifests live under `plugins/*/.claude-plugin/plugin.json`
- Collection-owned material: `MIT`; mixed third-party components: `MIT AND Apache-2.0 AND CC-BY-4.0` (see [rights and attribution](docs/third-party-licenses.md))

## Instruction Contract

Packaged skills follow the [collection instruction standard](plugins/pnet/skills/skill-improver/references/instruction-standard.md):
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
