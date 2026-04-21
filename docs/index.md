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

### `pnet-marketing`

This packaged plugin ships marketing-oriented SEO implementation skills for search-ready product surfaces.

### `pnet-business-product`

This packaged plugin ships grouped business, product, planning, research, and documentation skills.

### `pnet-core-development`

This packaged plugin ships grouped software development and architecture skills.

### `pnet-infrastructure`

This packaged plugin ships a grouped set of infrastructure and DevOps skills as one installable plugin.

### `pnet-language-specialists`

This packaged plugin ships grouped language and framework specialist skills for Go, React, and TypeScript.

### `pnet-qa`

This packaged plugin ships QA-oriented skills for browser automation and Playwright workflows.

## Repository Scope

This repository contains the public distribution artifacts for installable BMad plugins.
