---
name: marketing-on-page-seo-implementation
description: Implement production-grade on-page SEO in product codebases, not just blogs. Use when building, refactoring, or reviewing indexable pages and page families such as homepages, feature pages, solution pages, pricing pages, docs pages, integration pages, comparison pages, alternatives pages, template pages, category pages, glossary pages, location/entity pages, and programmatic SEO surfaces. Covers page existence decisions, ownership, metadata, headings, rendered content, canonicalization, robots rules, schema, internal links, sitemap/indexation, pagination and facet control, framework rendering choices, and launch QA.
---

# On-Page SEO Implementation

Use this skill when SEO must be implemented in the product itself: routing, rendering, metadata, schema, internal links, sitemap policy, canonical rules, and launch validation.

This is a developer-facing implementation skill for real product codebases. It is not a blog-writing workflow, a backlink strategy, or a generic content marketing playbook.

## Use This Skill When

- a new page or page family is meant to rank
- an existing page is being rebuilt, migrated, or consolidated
- filters, pagination, locale routing, templates, comparisons, or programmatic pages may create crawl/index risk
- docs, product, and marketing surfaces compete for the same queries
- a team needs an SEO spec and implementation contract before coding
- launch QA must verify rendered HTML and production behavior

## Do Not Use This Skill As

- a substitute for off-page SEO or link acquisition
- a request to mass-produce pages before uniqueness and indexation rules exist
- a content-only writing brief detached from code, routing, and ownership

## What This Skill Must Produce

When invoked for implementation work, produce as many of these artifacts as the task needs:

- page inventory with keep, merge, redirect, canonicalize, noindex, or remove decisions
- one SEO spec per target URL or page family
- implementation requirements split by frontend, backend/platform, and product/marketing ownership
- schema plan with field sources
- internal linking plan with inbound and outbound expectations
- launch QA checklist with blockers, warnings, and production verification steps
- unresolved risks that could change whether the page should launch or remain indexable

## Operating Stance

1. Treat SEO as product architecture, not post-launch cleanup.
2. Every indexable URL must earn its place with a distinct intent, not just a new slug.
3. Critical SEO signals must be present in rendered HTML and align across metadata, canonicals, schema, links, and sitemap entries.
4. Product pages, docs pages, comparison pages, and programmatic page families follow different ranking rules; do not treat them as interchangeable.
5. If a page is weak, duplicative, or operationally unsafe, the correct answer is often to merge, noindex, or not build it yet.

## Ownership Model

Use these boundaries unless the repo explicitly defines another split.

### Product / Marketing Owns

- page existence and inventory decisions
- primary query cluster and search intent
- page purpose and conversion goal
- differentiation against overlapping surfaces
- whether a page family is strategically worth maintaining

### Frontend Owns

- rendered body content and heading structure
- title, meta description, canonical plumbing, and framework metadata APIs
- crawlable body links and breadcrumb rendering
- image semantics and media context
- render strategy for ranking-critical content

### Backend / Platform Owns

- route design and slug stability
- canonical rules and redirect lifecycle
- sitemap generation and exclusion rules
- robots, noindex, and crawl control
- pagination, parameter, and facet behavior
- status codes and stale page retirement

If ownership is unclear, call that out as a delivery risk. Ambiguous ownership is a common source of SEO regressions.

## Non-Negotiable Rules

1. Do not ship an indexable page without a clear primary query, a clear intent owner, and a justified canonical URL.
2. Do not let product, docs, blog, and comparison pages compete for the same intent without an explicit ownership decision.
3. Do not rely on client-only rendering for title, canonical, primary copy, schema, or important links on pages that are meant to rank.
4. Do not create comparison pages unless the page can make a real case, show honest tradeoffs, and route the user to the right next step.
5. Do not create programmatic page families until uniqueness rules, noindex criteria, link sources, and stale-page handling are defined.
6. Do not keep weak duplicates live behind canonicals when a redirect or removal is the cleaner solution.
7. Do not submit non-canonical, redirected, noindex, or parameter-variant URLs in sitemaps.
8. Do not mark up schema that the page cannot visibly support with real data.
9. Do not hide the only meaningful content in tabs, accordions, client fetches, screenshots, or gated UI.
10. Do not launch when rendered HTML, production behavior, and indexation policy disagree.

## Decision Rules The Skill Should Enforce

### Build Vs Do Not Build

- Build when the page owns a distinct query cluster, has durable value, and can be linked into the site architecture.
- Do not build when the only difference is a swapped keyword, city, template name, or competitor name with no meaningful substance.

### Redirect Vs Canonicalize Vs Noindex

- Redirect when the weaker URL should stop existing.
- Canonicalize when users still need alternate states but search should consolidate to one owner.
- Noindex when the page serves users operationally but should not compete in search.
- Merge when multiple pages dilute the same intent and the combined page will be stronger.

### Docs Vs Product Ownership

- Product pages should usually own commercial and solution-intent queries.
- Docs pages should rank when the searcher wants setup, troubleshooting, API, implementation, or technical depth.
- If docs are outranking product pages for transactional intent, either strengthen product intent ownership or reduce index emphasis on the docs surface.

### Comparison / Alternatives

- Build when the comparison is a real evaluation path and the page can explain fit, tradeoffs, proof, and migration or switching guidance.
- Do not build as thin doorway pages that merely restate the competitor query and push a CTA.

### Programmatic SEO

- Build only after defining data quality, uniqueness thresholds, template variability, and retirement rules.
- Delay launch when the family would mostly produce thin pages, orphaned pages, or pages that only differ by tokens.

## Required Workflow

Follow the phases in order. Skip only if the requested task truly starts later in the flow and the earlier decisions are already documented.

### Phase 1: Decide Whether The Surface Should Exist

Produce:

- page inventory
- overlap and cannibalization notes
- page-owner decision
- keep, merge, redirect, canonicalize, noindex, or remove decision per URL

Read first:
- `references/01-discovery-and-page-selection.md`

### Phase 2: Create The SEO Contract Before Coding

Produce:

- page spec per target URL
- content and metadata requirements
- schema and link requirements
- render mode and indexation rules

Read:
- `references/02-page-spec-template.md`

### Phase 3: Implement Rendering And Metadata Correctly

Produce:

- frontend implementation checklist
- render-mode decisions
- heading, body content, metadata, and media requirements

Read:
- `references/03-frontend-seo-implementation.md`
- `references/11-framework-notes.md` when framework-specific details matter

### Phase 4: Lock Routing, Canonicals, And Indexation

Produce:

- backend/platform checklist
- canonical, redirect, robots, sitemap, and parameter policy
- stale-page lifecycle rules

Read:
- `references/04-backend-routing-and-indexation.md`

### Phase 5: Add Only Truthful Schema

Produce:

- schema plan
- field-source map
- validation method

Read:
- `references/05-schema-and-serp-features.md`

### Phase 6: Wire The Page Into The Site

Produce:

- inbound and outbound link plan
- hub-and-spoke expectations
- orphan prevention notes

Read:
- `references/06-internal-linking-patterns.md`
- `references/09-docs-seo-patterns.md` for docs-heavy surfaces
- `references/10-comparison-and-alternative-pages.md` for comparison and alternative pages

### Phase 7: Gate The Launch

Produce:

- blocker list
- warning list
- production verification checklist
- post-launch monitoring notes

Read:
- `references/07-launch-qa-checklist.md`

### Phase 8: Validate Against The Right Page Type

Use the worked examples to sanity-check scope, blocks, linking, schema, and indexation choices.

Read:
- `references/08-examples-by-page-type.md`

## Page Types This Skill Covers

- homepage
- feature page
- product page
- pricing page
- solution page
- integration page
- docs page
- comparison page
- alternatives page
- template page
- category page
- glossary page
- location or entity page
- programmatic SEO page family

## Output Format

When responding with implementation guidance, use this order:

1. page or page-family goal
2. page ownership and go/no-go decision
3. implementation decisions by frontend, backend/platform, and product/marketing
4. schema and internal linking requirements
5. launch blockers, warnings, and validation checks
6. unresolved risks or assumptions

## Reference Files

- `references/01-discovery-and-page-selection.md`
- `references/02-page-spec-template.md`
- `references/03-frontend-seo-implementation.md`
- `references/04-backend-routing-and-indexation.md`
- `references/05-schema-and-serp-features.md`
- `references/06-internal-linking-patterns.md`
- `references/07-launch-qa-checklist.md`
- `references/08-examples-by-page-type.md`
- `references/09-docs-seo-patterns.md`
- `references/10-comparison-and-alternative-pages.md`
- `references/11-framework-notes.md`
