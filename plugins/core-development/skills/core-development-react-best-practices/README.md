# React Best Practices

This package preserves a public React and Next.js performance-rule collection
and adds an evidence-first entrypoint for applying it safely.

## Packaged Surfaces

- `SKILL.md` — trigger, authority, selection workflow, and completion contract.
- `rules/` — 51 authoritative rule units plus section metadata and a rule
  template.
- `AGENTS.md` — preserved expanded compatibility snapshot.
- `metadata.json` — source and reference metadata.
- `tests/` — package-integrity and regression checks.

The package does not include the upstream build workspace, package manifest, or
test-case generator. Do not run the historical package-manager commands from an
upstream checkout against this published skill. Edit and validate the packaged
files directly.

## Using the Rules

Start with `SKILL.md`, identify the measured problem, then load only the relevant
rule files. Treat category impact labels and numeric examples as prioritization
hints; applicability depends on the current React/Next.js versions, compiler,
bundler, runtime, workload, and supported clients.

`AGENTS.md` remains useful for broad reading and compatibility. When it differs
from an individual rule file, the rule file and current official documentation
take precedence.

## Rule File Convention

Use `rules/_template.md` when adding a rule. Select the prefix by category:

- `async-` — eliminating waterfalls;
- `bundle-` — bundle-size optimization;
- `server-` — server-side performance;
- `client-` — client data and browser APIs;
- `rerender-` — rerender optimization;
- `rendering-` — browser rendering;
- `js-` — JavaScript hot paths;
- `advanced-` — narrowly applicable React patterns.

Keep each rule focused on one decision. Include assumptions, an incorrect and
correct example when useful, compatibility or security caveats, and an official
source for version-sensitive behavior. Do not add unsupported universal
benchmarks.

## Maintenance Checks

When changing the package:

1. preserve every unrelated rule and stable path;
2. update `SKILL.md` routing when the rule inventory changes;
3. keep the compatibility snapshot clearly labeled and safe;
4. run the focused tests;
5. run repository naming, skill-structure, and public-release validation;
6. classify warnings and review the diff for information loss.

## Attribution

The original collection is attributed to Vercel Engineering and distributed
under the package's declared MIT license. This public package is an adapted
snapshot; it must not imply that later local refinements are maintained or
endorsed by the upstream authors.

The original collection credits [@shuding](https://x.com/shuding) at
[Vercel](https://vercel.com). These links are retained as source provenance,
not as an endorsement of this adapted package.
