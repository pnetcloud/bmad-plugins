# Delivery Artifacts And Handoffs

Use this reference when the task is not only to reason about SEO, but to hand the work off in a form that frontend, backend, product, and QA can execute without reinterpreting the strategy.

## Goal

Turn SEO decisions into operational artifacts:

- audit notes that explain what should exist, change, merge, or disappear
- implementation handoffs with explicit ownership
- launch receipts that record pass, fail, and follow-up items
- page-family rollout notes for scalable surfaces

## Artifact Selection

Use the smallest artifact set that can move the work forward.

| Situation | Required artifact |
|---|---|
| deciding whether a page should exist or which page owns intent | audit note |
| handing implementation to engineers | implementation handoff |
| validating a launch or migration | QA receipt |
| launching templates, locations, entities, or other repeated page families | page-family rollout note |

If the task spans multiple phases, produce an artifact pack instead of one giant narrative.

## 1. Audit Note Template

Use this when reviewing current inventory, overlap, or cannibalization risk.

```md
# SEO Audit Note

## Scope
- Surface reviewed:
- URLs reviewed:
- Review date:

## Intent Ownership Summary
- Primary query cluster:
- Recommended owner:
- Why this owner should win:

## Decisions
| URL | Page type | Current role | Decision | Why |
|---|---|---|---|---|
| /example | feature | weak duplicate | merge + 301 | parent page already owns the intent |

## Findings
- Blockers:
- Warnings:
- Pages that should link to the chosen owner:
- Pages that should be redirected, canonicalized, noindexed, or removed:

## Recommended Next Step
- Create new page / improve existing page / merge / retire:
- Owner:
- Follow-up risks:
```

### Audit Rules

- state one winning owner for the intent
- make every URL decision explicit
- name the operational consequence, not only the SEO theory
- call out ownership gaps when nobody can maintain the page

## 2. Implementation Handoff Template

Use this when the page or page family is approved and engineering work needs to start.

```md
# SEO Implementation Handoff

## Page Goal
- URL:
- Page type:
- Primary query cluster:
- Search intent:
- Canonical owner:
- Conversion goal:

## Must Ship
- Render mode:
- Indexation rule:
- Canonical rule:
- Required content blocks:
- Required schema:
- Required internal links:

## Frontend Requirements
- Metadata implementation:
- Heading/body content requirements:
- Body-link requirements:
- Media and image requirements:
- Rendered HTML checks:

## Backend / Platform Requirements
- Route pattern:
- Redirect requirements:
- Sitemap rule:
- Parameter / facet / locale rule:
- Status code rule:
- Retirement rule:

## Product / Marketing Requirements
- Proof or claims needed:
- Source of comparisons or FAQs:
- Required CTA and next-step logic:
- Ongoing maintenance owner:

## Launch Gate
- Blocking checks:
- Warning checks:
- Production checks:

## Assumptions / Open Risks
- Risk:
- Owner:
- What changes the decision:
```

### Handoff Rules

- separate requirements by owner instead of mixing them into one checklist
- convert abstract advice into implementation-level requirements
- include blockers up front so launch risk is visible before coding starts
- if an item lacks an owner, mark it as unresolved instead of burying it

## 3. QA Receipt Template

Use this after implementation, migration, or launch QA.

```md
# SEO QA Receipt

## Verification Context
- URL:
- Environment:
- Checked by:
- Checked at:

## Result
- Launch status: pass / pass with warnings / fail

## Blocking Failures
- Issue:
- Evidence:
- Owner:

## Warnings
- Issue:
- Evidence:
- Owner:

## Verified Signals
- Status code:
- Canonical:
- Robots / noindex:
- Title and H1:
- Rendered body content:
- Schema:
- Inbound path:
- Sitemap state:

## Follow-Up
- Recheck date:
- Monitoring owner:
- Related migration or rollout note:
```

### QA Receipt Rules

- record evidence, not only opinion
- distinguish “not ideal” from “must stop launch”
- verify production behavior, not only preview or local output
- keep a receipt for migrations and framework changes so regressions are comparable later

## 4. Page-Family Rollout Note

Use this for template libraries, integration directories, location/entity surfaces, or programmatic SEO families.

```md
# Page-Family Rollout Note

## Family Summary
- Family name:
- URL pattern:
- Search intent type:
- Canonical owner:

## Publish Rules
- Minimum data required to publish:
- Uniqueness threshold:
- Required visible blocks:
- Required hub links:

## Noindex / Exclusion Rules
- Variants that stay noindex:
- Variants excluded from sitemap:
- Variants that return 404 or 410:

## Lifecycle Rules
- Refresh trigger:
- Stale-page retirement rule:
- Redirect rule for retired winners:

## Monitoring
- Sample URLs to review:
- Failure signals:
- Re-audit trigger:
```

### Rollout Rules

- never launch a page family without written publish and retirement rules
- define noindex criteria before scale, not after low-quality pages accumulate
- identify the hubs that will supply crawlable inbound links

## Packaging Guidance

When the task is large, deliver artifacts in this order:

1. audit note
2. implementation handoff
3. QA receipt

For page families, include the rollout note between the handoff and QA receipt.

## Minimum Deliverable Standard

A complete artifact pack should let another agent or engineer answer these questions without re-reading the whole analysis:

- should the page exist
- which surface owns the intent
- what frontend must render
- what backend must control
- what blocks launch
- what happens if the page or family goes stale
