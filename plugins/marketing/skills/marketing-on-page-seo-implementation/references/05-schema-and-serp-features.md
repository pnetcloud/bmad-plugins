# Schema And SERP Features

Use schema to clarify the page, not to inflate it. Good schema reflects real page content and trustworthy data sources.

## Goal

Choose only truthful schema, wire it to real data, and validate the final rendered output.

## Core Rules

1. Mark up only what is visible or genuinely true.
2. Prefer JSON-LD.
3. Every important field should have a named data source.
4. Validate before shipping and after deploy.
5. If the page content changes meaningfully, the schema plan must be reviewed too.

## Schema Selection Matrix

| Page type | Common schema | Notes |
|---|---|---|
| Homepage | `Organization`, `WebSite` | Use for real organization and site-level signals |
| Product or pricing page | `Product`, `Offer`, sometimes `FAQPage` | Only if the page truly represents a product or offer |
| SaaS feature or landing page | `SoftwareApplication`, `Organization`, sometimes `FAQPage` | Do not force `Product` markup onto vague marketing pages |
| Docs page | `TechArticle` or `Article`, `BreadcrumbList` | Best for implementation-heavy docs |
| Comparison or alternatives page | `Article`, `FAQPage`, `BreadcrumbList`, sometimes `ItemList` | Keep comparison claims grounded in visible content |
| Category or collection page | `CollectionPage`, sometimes `ItemList`, `BreadcrumbList` | Use `ItemList` only when the list is real and stable |
| Local page | `LocalBusiness` plus subtype, `BreadcrumbList` | Only for real local entities |

## Recommended Baseline

For many product-facing pages, the practical baseline is:

- one primary page-content schema type
- `BreadcrumbList` when breadcrumbs are real
- homepage-level `Organization` or `WebSite` where appropriate

Do not stack multiple schema types just to look sophisticated.

## When Not To Use Specific Schema Types

### FAQPage

Do not use when:

- the page does not visibly expose FAQs
- the answers are thin filler added only for markup
- the questions duplicate collapsible UI with no meaningful substance

### Product

Do not use when:

- the page is a generic feature overview without a true product or offer representation
- pricing and offer data are not actually present or trustworthy
- the page is really an article, comparison, or documentation page

### Review Or AggregateRating

Do not use when:

- ratings are not sourced from a real review system
- the rating is not visible and supportable
- the data is stale, incomplete, or selectively represented

### LocalBusiness

Do not use when:

- there is no real local presence
- the page is just a geo-modified clone with no local substance

## Field Source Expectations

For every schema block, specify:

- schema type
- required fields
- exact data source
- team or system that owns the source
- validation method

Example planning table:

| Field | Source |
|---|---|
| `headline` | page title and H1 spec |
| `description` | page summary or meta description source |
| `offers.price` | billing config or commerce backend |
| `softwareVersion` | release metadata or docs source |
| `aggregateRating` | reviews system |

If a field source is “manual copy paste,” treat that as fragile.

## Page-Type Guidance

### Product / Pricing

Use `Product` or `Offer` only when the page truly represents the offer and the source data is accurate.

### Docs

Prefer `TechArticle` when the page teaches implementation, usage, or troubleshooting with real structure.

### Comparison / Alternatives

Use `Article` for the core page and add `FAQPage` only if the FAQs are real, visible, and useful.

### Collections / Categories

Use `CollectionPage` or `ItemList` when the page really curates a set, not when it is an empty shell.

## Validation Process

Before launch:

- validate JSON-LD syntax
- validate chosen schema types in a schema tool
- inspect rendered HTML to confirm the final JSON-LD is present
- confirm field values match visible content and current route state

After deploy:

- verify production HTML, not just local output
- confirm revalidation or CMS updates do not leave stale schema

## Rich Result Caution

Schema improves clarity and eligibility. It does not guarantee rankings or rich results. Treat schema as implementation hygiene first, optional enhancement second.
