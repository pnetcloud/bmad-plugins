# pNet BMad Plugins

Public distribution repository for installable BMad plugins maintained in [`pnetcloud/bmad-plugins`](https://github.com/pnetcloud/bmad-plugins).

This repository is focused on publishable plugin payloads, grouped skill packages, and the marketplace manifest consumed by the BMad installer.

## What This Repo Contains

- Installable plugin packages under `plugins/`
- Public marketplace metadata in `.claude-plugin/marketplace.json`
- Lightweight public docs in `docs/`
- Ready-to-install grouped skill bundles for local or remote BMad installs

## Current Layout

```text
bmad-plugins/
├── .claude-plugin/                     # Marketplace manifest for all public plugins
├── docs/                               # Public docs
├── plugins/
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

### Canonicalized Skills

The repository has been normalized so skill folders now use the canonical prefixed IDs everywhere.

- `business-product-confluence`
- `business-product-jira`
- `core-development-data-pipeline-go`
- `core-development-implement-design`
- `qa-agent-browser`

### Validation

Run the repository validator before publishing or adding new skills:

```bash
python3 scripts/check_skill_names.py
```

The validator enforces the canonical convention for every packaged skill.

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

- `pnet-business-product`
- `pnet-core-development`
- `pnet-infrastructure`
- `pnet-language-specialists`
- `pnet-qa`

## Plugin Catalog

### `pnet-business-product`

Business, product, planning, research, and documentation skills grouped into one installable package.

- Publish path: `plugins/business-product`
- Packaged skill path: `plugins/business-product/skills/*`
- Included skills: 16
- Examples: `business-product-business-analyst`, `business-product-confluence`, `business-product-jira`

### `pnet-core-development`

Core software development skills across architecture, APIs, backend, frontend, databases, UI, and documentation.

- Publish path: `plugins/core-development`
- Packaged skill path: `plugins/core-development/skills/*`
- Included skills: 26
- Examples: `core-development-api-designer`, `core-development-data-pipeline-go`, `core-development-implement-design`

### `pnet-infrastructure`

Infrastructure and DevOps skills for cloud architecture, CI/CD, Kubernetes, Terraform, and platform operations.

- Publish path: `plugins/infrastructure`
- Packaged skill path: `plugins/infrastructure/skills/*`
- Included skills: 8
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
- Included skills: `qa-agent-browser`, `qa-playwright-skill`

## Repository Scope

This repository contains the public distribution artifacts for installable BMad plugins. It is intended to stay focused on packaged outputs rather than source authoring workflows.

## Notes

- Marketplace metadata is published from `.claude-plugin/marketplace.json`
- Installable payloads live under `plugins/*`
- Plugin-specific manifests live under `plugins/*/.claude-plugin/plugin.json`
- License: `MIT`
