# Target Skill Structure and Context Budgets

Use this reference when reorganizing a skill, splitting a large entrypoint, or deciding where new material belongs.

## Contents

- Standard shape
- Placement rules
- Entrypoint budgets
- Resource budgets
- Structural review checklist

## Standard Shape

Create only directories that have a real consumer. Do not add empty scaffolding.

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
- the shortest complete core workflow;
- resource selection rules;
- completion and stop criteria;
- links that state exactly when each conditional resource must be read.

Move out:

- provider- or framework-specific variants;
- long schemas, catalogs, lookup tables, and domain references;
- repeated examples and large output samples;
- setup manuals and troubleshooting catalogs;
- deterministic code better expressed and tested as a script.

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

## Entrypoint Budgets

Measure both lines and words because dense prose can evade a line-only limit.

| Surface | Goal | Structural review threshold | Completion limit |
|---|---:|---:|---:|
| Frontmatter description | 80–500 characters | Above 500 characters | 1024 characters |
| Complete `SKILL.md` | 80–180 lines and 600–1500 words | Above 250 lines or 2000 words | 500 lines |
| Default loaded guidance | At most 3000 words | Above 4000 words | Must be justified by the active task |

Do not complete an improvement with `SKILL.md` above 500 lines. Move conditional detail into resources while preserving required behavior.

An entrypoint below the goal is acceptable when it remains complete. Never add filler to hit a minimum.

The total package has no fixed size limit. A large skill is healthy when:

- its entrypoint stays within budget;
- each task loads only relevant resources;
- large references are navigable and topic-focused;
- scripts and assets do not consume context unless needed.

## Resource Budgets

- Reference goal: one topic, normally no more than 300 lines or 2500 words.
- Reference split threshold: 500 lines, multiple independent topics, or repeated irrelevant loading.
- Example goal: no more than 120 lines per scenario.
- Scripts and tests: no prose-size target; control complexity through modularity and focused tests.
- Assets: no context-size target because they are loaded only when needed.

These are decision thresholds, not quality scores. Exceed a goal only when evidence shows splitting would reduce correctness or usability.

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
