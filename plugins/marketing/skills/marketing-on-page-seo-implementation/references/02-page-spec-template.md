# Page Spec Template

Write one spec per indexable URL or page family before implementation. The spec is the SEO contract between product, frontend, backend, and whoever validates the launch.

## Required Outcome

The finished spec should make these questions deterministic:

- should this page exist and be indexable
- who owns the intent
- what must render in HTML
- what the canonical and indexation rules are
- what schema and links are required
- what would block launch

## Full Template

```md
# Page SEO Spec

## 1. Identity
- URL:
- Canonical URL:
- Page type:
- Surface owner:
- Maintenance owner:
- Page family, if any:

## 2. Search Target
- Primary query:
- Supporting queries:
- Search intent:
- Why this page should own the intent:
- Competing existing URLs:
- Keep / merge / redirect / canonicalize / noindex decisions:

## 3. Audience And Conversion
- Primary audience:
- User problem to solve:
- Primary conversion goal:
- Secondary conversion goal:
- Next step after this page:

## 4. Metadata Contract
- Title tag:
- Meta description:
- H1:
- Optional OG title:
- Optional OG description:
- Breadcrumb trail:

## 5. Content Contract
- Intro block:
- Core sections:
- Required proof blocks:
- Required comparison/spec/table blocks:
- FAQ block:
- CTA block:
- Must-have visible copy:
- What must not be hidden behind interaction:

## 6. Rendering And Technical Rules
- Render mode: SSR / SSG / ISR / hybrid
- Why that render mode is acceptable:
- Indexation rule: index / noindex
- Canonical rule:
- Hreflang rule:
- Pagination / facet / parameter rule:
- Sitemap inclusion rule:
- Status code expectations:
- Retirement rule if the page goes stale:

## 7. Structured Data
- Schema types:
- Required properties:
- Field source for each property:
- Validation method:

## 8. Internal Linking
- Pages that must link to this page:
- Pages this page must link to:
- Hub or parent page:
- Child or sibling pages:
- Preferred anchor themes:

## 9. Media Requirements
- Hero image or preview requirement:
- Required alt text strategy:
- Captions or annotations needed:

## 10. Launch QA
- Blocking checks:
- Warning checks:
- Production verification steps:
- Known risks:
```

## Rules For Filling The Spec

1. The URL, canonical, title, H1, and primary query must align on the same intent.
2. The spec must say why this page exists instead of a nearby page.
3. “Render mode” is not a framework preference field; it must justify how ranking-critical content reaches rendered HTML.
4. Every schema field should name its real data source.
5. Every page family must define what makes one page unique from its siblings.
6. Launch QA must list true blockers, not generic reminders.

## Guidance By Section

### 1. Identity

Use one canonical owner. If multiple teams claim the page, the spec is incomplete.

### 2. Search Target

This section should explain:

- what user need brought the searcher here
- why the chosen surface owns that need
- which current URLs become stronger, weaker, or obsolete because of this page

### 3. Audience And Conversion

Do not define conversion only as “CTA click.” For docs pages, activation or successful implementation may be the real conversion.

### 4. Metadata Contract

- Title: usually 50 to 60 visible characters, query early when natural.
- Meta description: sell the click with value, not repetition.
- H1: close to title but written for the page, not the SERP only.
- Breadcrumbs: include only if they reflect real site hierarchy.

### 5. Content Contract

This section should answer what must be visible in HTML for the page to deserve ranking.

Examples of valid required blocks:

- feature explanation
- supported integrations or compatibility details
- migration guidance
- setup prerequisites
- template preview and customization notes
- comparison table
- proof points tied to the page claim

### 6. Rendering And Technical Rules

Specify:

- whether primary copy renders on first response
- whether filter or locale variants are indexable
- whether weak programmatic pages default to noindex
- how stale or removed pages are retired

### 7. Structured Data

List only schema that the page can support truthfully. “Optional FAQ” is not enough; say when it qualifies and where the answers come from.

### 8. Internal Linking

Name concrete parent, sibling, supporting, and next-step pages. A page that “should get links later” is not ready.

### 9. Media Requirements

If screenshots or previews are core evidence, require captions or surrounding text so the meaning is not image-only.

### 10. Launch QA

Separate:

- blockers: issues that should stop launch
- warnings: non-ideal issues that may launch with explicit acceptance
- production checks: things that must be re-verified after deploy

## Page-Family Addendum

For templates, locations, entities, or other repeated page families, append:

- uniqueness rule
- minimum data required to publish
- noindex rule for weak variants
- internal link source hubs
- stale-page retirement rule

## Use This Spec For

- new product pages
- page refactors
- migrations and framework rewrites
- programmatic SEO families
- comparison and alternative pages
- docs pages intended to rank
