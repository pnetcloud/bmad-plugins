# pnet-infrastructure

Installable BMad plugin package for infrastructure and DevOps related skills.

## Included Skills

9 skill entries.

- `infrastructure-cloud-architect`
- `infrastructure-container-orchestration`
- `infrastructure-devops-engineer`
- `infrastructure-devops-standards`
- `infrastructure-gitlab-ci-standards`
- `infrastructure-kubernetes-specialist`
- `infrastructure-makefile-standards`
- `infrastructure-terraform-engineer`
- `infrastructure-cloudflare`

## Contents

- `.claude-plugin/plugin.json` - plugin manifest
- `skills/` - packaged infrastructure skill directories

## Notes

This plugin directory is intended to stay focused on the installable package contents.

## Imported knowledge and rights

`infrastructure-cloudflare` adds product-selection knowledge and references,
not installed Wrangler/cf tools, credentials or provider bindings. Optional sibling
skills are not bundled by implication; use its documented fallback when absent.
Verify actual host interfaces and obtain scope-specific approval before network
or configuration operations. No live Cloudflare API operation is verified here.

Aggregate package license: `MIT AND Apache-2.0`. This describes separate
components, not a relicensing or a choice of license for every file. See the
[third-party rights guide](../../docs/third-party-licenses.md) and each imported
entry's `ORIGIN.md`, full `LICENSE` and applicable notices.
