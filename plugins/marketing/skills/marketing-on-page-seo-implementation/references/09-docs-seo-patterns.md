# Docs SEO Patterns

Use this file when a docs page, docs section, or developer-facing knowledge base is supposed to rank.

## Goal

Help docs rank for implementation intent without letting docs accidentally steal commercial intent that belongs to product or solution pages.

## When Docs Should Rank

Docs are often the right owner when the searcher wants:

- setup instructions
- API or SDK usage
- troubleshooting
- integration steps
- task-level implementation help
- reference material paired with real task framing

Docs are usually the wrong primary owner when the searcher wants:

- product evaluation
- pricing
- feature comparison at a buying stage
- solution selection

## Docs SEO Page Shape

A ranking docs page usually needs:

- short intro that frames the problem or task
- prerequisites
- implementation steps or reference guidance
- examples, screenshots, or code when helpful
- troubleshooting or edge cases
- next-step links

Raw reference-only pages can rank, but they are much stronger when they still explain the task context.

## Product And Docs Handoff Rules

### Product To Docs

Link from product or integration pages when the docs prove that the feature can actually be implemented.

### Docs To Product

Link back to product pages when:

- the docs page helps evaluate the capability
- the user may need feature context, pricing, or capability explanation

Do not force a hard sell on every docs page. Use product links as context, not as clutter.

## Docs Pages That Often Should Not Rank

Consider noindex for:

- changelog entries with no enduring value
- duplicate generated references
- preview or internal-only docs
- near-duplicate locale or version pages without distinct value
- weak stub pages that only say a feature exists

## Metadata And Headings

- title and H1 should describe the user task clearly
- avoid titles that are only endpoint names or internal labels when broader task framing is needed
- do not reuse the same title pattern across many docs pages without variation

## Internal Linking Expectations

- docs hubs link to important task pages
- task pages link to prerequisites and next steps
- docs pages link to product or integration context when relevant
- orphan docs pages are usually a sign of poor information architecture

## Schema Suggestions

- `TechArticle` for task-oriented documentation
- `Article` for broader conceptual docs
- `BreadcrumbList` when breadcrumbs reflect true hierarchy

## QA Questions

- Does the page solve a clear implementation task?
- Is the introduction understandable without prior product knowledge?
- Does the page link to the right next step?
- Is this page competing with another docs page or a product page for the same query?
