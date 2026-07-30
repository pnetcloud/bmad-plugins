# Target Skill Structure and Context Budgets

Use this reference when reorganizing a skill, splitting a large entrypoint, or deciding where new material belongs.

## Contents

- Available shape
- Placement rules
- Entrypoint review signals
- Resource review signals
- Structural review checklist

## Available Shape

These directories are options, not a target every skill should reach. Create a
directory only when a real task will use it. Do not add empty scaffolding,
scenario catalogs, generic references, or contract tests to normalize a
collection. Treat the existing shape as the default contract.

```text
skill-name/
├── SKILL.md                   # Required trigger and core workflow
├── agents/
│   └── openai.yaml            # Optional provider/UI metadata
├── references/                # Conditional knowledge and detailed guidance
├── scripts/                   # Deterministic repeatable operations
├── examples/                  # Small golden inputs, outputs, or diffs
├── assets/                    # Templates or files copied into produced output
└── tests/                     # Executable checks for non-trivial scripts/contracts
```

Prefer `assets/templates/` for reusable output templates. Preserve a legacy `templates/` directory when consumers require that path; do not rename public paths merely for cosmetic uniformity.

## Placement Rules

### `SKILL.md`

Keep:

- `name` and trigger-rich `description` frontmatter;
- operating boundaries and authority gates;
- the complete core workflow at the minimum detail needed for safe, successful
  execution;
- resource selection rules;
- completion and stop criteria;
- links that state exactly when each conditional resource must be read.

Consider moving a coherent topic only when task evidence, routing analysis, or
structural review shows that it is conditional and unnecessary on the main path:

- provider- or framework-specific variants;
- long schemas, catalogs, lookup tables, and domain references;
- repeated examples and large output samples;
- setup manuals and troubleshooting catalogs;
- deterministic code better expressed and tested as a script.

Moving material is a structural change, not a synonym for shortening. Obtain
approval for the structural proposal before editing. Then add and route the
destination, verify its consumer and retained meaning, and only afterward
consider removing the original path.

### `references/`

Store detailed information the agent may need in context. Keep references one link away from `SKILL.md`; avoid chains where one reference is discoverable only through another.

Give every reference one clear topic. For a reference longer than 100 lines, add a short contents list. Split it when unrelated topics would cause an agent to load irrelevant context.

### `scripts/`

Store repeated or fragile deterministic operations. Scripts must:

- accept explicit inputs;
- avoid hidden environment mutation;
- fail clearly;
- be read and tested before being trusted;
- never turn quarantined third-party code into an executable dependency.

### `examples/`

Store discriminating golden examples, not long transcripts. Prefer one scenario per file and show only the input, decisive behavior, and expected output shape.

Examples are evidence, not instructions with higher authority than the active task.

### `assets/`

Store files intended for produced output and not normally loaded as instruction context: templates, boilerplate, images, fonts, and sample documents.

### `tests/`

Add focused tests for non-trivial scripts, validators, parsers, and safety gates. Do not create tests that merely assert exact prose.

## Entrypoint Review Signals

Measure both lines and words because dense prose can evade a line-only limit.

| Surface | Review signal | Hard format limit |
|---|---:|---:|
| Frontmatter description | Above 500 characters | 1024 characters |
| Complete `SKILL.md` | Above 250 lines or 2000 words | None |
| Default-loaded guidance | Evidence of irrelevant loading in real tasks | None |

These signals trigger a question, not a rewrite: would moving one coherent,
conditionally used topic reduce loaded context without weakening the active
workflow? If the answer is unproven, keep the entrypoint unchanged.

There is no minimum line or word count. Never expand a concise skill to satisfy
a size band. There is also no automatic maximum: retain a large entrypoint when
splitting would make the workflow harder to follow or risks losing knowledge.

The total package has no fixed size limit. A large skill is healthy when:

- its entrypoint stays within budget;
- each task loads only relevant resources;
- large references are navigable and topic-focused;
- scripts and assets do not consume context unless needed.

Do not use progressive disclosure as a synonym for deleting detail. Move valid
knowledge into directly reachable, topic-focused resources. A source cache or
Git history is provenance and recovery evidence, not part of the installed
skill's usable capability.

Default to zero deleted or renamed files and zero retired capabilities. Any
such structural change requires the complete pre-approval proposal and
retention matrix defined in `review-prompt.md`. Semantic replacement counts as
removal. Package reduction is incidental and never a quality goal.

## Resource Review Signals

- A reference should serve one coherent conditional topic. Split only when
  tasks repeatedly load unrelated material.
- Keep examples discriminating and reusable; do not turn every local review
  scenario into a published file.
- Add scripts for repeated or fragile deterministic operations, then test them.
- Add tests for executable behavior or stable machine contracts, not for exact
  prose, heading presence, or a desired file count.
- Assets have no context-size target because they are loaded only when needed.

Size is diagnostic evidence only. A large, useful resource can remain large; a
small, unused resource should not be created.

## Structural Review Checklist

- Does the description contain all trigger and non-trigger information?
- Can an agent execute the main path after loading only `SKILL.md`?
- Is every conditional resource linked directly with a read condition?
- Does each fact or procedure have one authoritative home?
- Are deterministic operations scripts rather than repeatedly generated code?
- Are examples small, discriminating, and free of placeholder claims?
- Are templates treated as assets instead of instruction prose?
- Do tests cover parsers, scripts, safety gates, and important edge cases?
- Does the active path stay within the context budget?
- Did the refactor preserve public paths and valid behavior?
- Does the before/after manifest explain every missing or renamed file?
- Does the retention matrix account for every removed file and capability?
- If a structural change was approved, was information loss reviewed separately?
