# Examples By Page Type

Use these as implementation patterns, not copy templates. The goal is to help teams choose the right page shape, required blocks, linking behavior, schema, and indexation posture.

## 1. Feature Page

### Best For

- `[feature] software`
- `[feature] tool`
- `[feature] for [audience]`

### Search Intent

Usually commercial or solution intent. The searcher wants to evaluate whether the feature solves a real problem.

### Minimum Content Blocks

- clear feature explanation above the fold
- who the feature is for
- how it works
- supported workflows or use cases
- proof, screenshots, or evidence
- links to pricing, docs, integrations, and related features
- FAQ or objection handling

### Common Failure Modes

- page is just a hero and CTA with no implementation depth
- feature page duplicates the parent product page
- screenshots exist without surrounding explanation
- docs actually own the implementation query, but the feature page tries to cover it weakly

### Internal Linking Expectations

- inbound from product hubs, solution pages, and relevant comparisons
- outbound to pricing, docs, integrations, and related features

### Schema Suggestions

- `SoftwareApplication` when the page truly describes the software capability
- `BreadcrumbList`
- `FAQPage` only if FAQs are visible and useful

### Indexation Cautions

- do not index if the feature cannot sustain distinct intent from a stronger parent page
- if multiple near-duplicate feature pages exist, merge or redirect weaker variants

## 2. Integration Page

### Best For

- `[product A] [product B] integration`
- `[tool] connect to [platform]`

### Search Intent

Usually commercial plus implementation intent. The searcher wants to confirm the integration exists and understand how it works.

### Minimum Content Blocks

- what connects and why it matters
- setup requirements
- sync behavior or supported workflows
- limitations or prerequisites
- links to installation or configuration docs
- CTA tied to using the integration

### Common Failure Modes

- placeholder integration page for a non-functional or barely maintained integration
- no explanation of what actually syncs
- no path to setup docs
- dozens of integration pages with nearly identical copy

### Internal Linking Expectations

- inbound from feature pages, integration hubs, and partner directories when available
- outbound to setup docs, relevant feature pages, and related workflows

### Schema Suggestions

- `SoftwareApplication` or `Article`, depending on page shape
- `BreadcrumbList`

### Indexation Cautions

- noindex or do not publish placeholder integrations
- retire or redirect pages when integrations are deprecated

## 3. Docs Page Intended To Rank

### Best For

- setup, troubleshooting, API usage, and implementation queries

### Search Intent

Informational or implementation-depth intent. The searcher wants task completion, not only product positioning.

### Minimum Content Blocks

- concise intro that frames the user task
- prerequisites
- steps or implementation details
- examples, snippets, or screenshots when they help
- troubleshooting or edge cases
- next steps and related docs
- product handoff link when evaluation context matters

### Common Failure Modes

- raw reference page with no contextual intro
- docs page trying to rank for a transactional query that product should own
- no next-step links
- sidebar-only discoverability with no contextual body links

### Internal Linking Expectations

- inbound from docs hubs, relevant feature pages, and integration pages when the relationship is real
- outbound to prerequisite docs, next-step docs, and product pages that clarify the capability

### Schema Suggestions

- `TechArticle` or `Article`
- `BreadcrumbList`

### Indexation Cautions

- noindex thin changelog or duplicate reference pages
- do not let multiple docs pages compete for the same implementation query without an ownership decision

## 4. Comparison / Alternative Page

### Best For

- `[your product] vs [competitor]`
- `[competitor] alternative`

### Search Intent

High-intent evaluation. The searcher is comparing options and needs honest decision support.

### Minimum Content Blocks

- clear summary or TL;DR
- comparison table with real dimensions
- honest strengths and tradeoffs
- who each option fits best
- migration or switching path
- proof links and CTA

### Common Failure Modes

- doorway page with shallow competitor mentions
- biased claims without evidence
- no migration guidance or next step
- dozens of low-effort competitor pages generated from a template only

### Internal Linking Expectations

- inbound from competitor or alternatives hubs, feature pages, and migration resources
- outbound to pricing, proof pages, migration help, and relevant features

### Schema Suggestions

- `Article`
- `BreadcrumbList`
- `FAQPage` only when the FAQs are visible and real

### Indexation Cautions

- do not index if the page cannot make an honest and substantive case
- merge or noindex low-value competitor pages that only swap brand names

## 5. Template Page

### Best For

- `[type] template`
- `[workflow] example`

### Search Intent

Mixed informational and commercial intent. The searcher wants a concrete starting point, preview, or reusable artifact.

### Minimum Content Blocks

- immediate answer or preview
- what the template includes
- who it is for
- setup or customization guidance
- related templates or examples
- product CTA tied to using the template

### Common Failure Modes

- template page has no preview, explanation, or customization guidance
- template family pages are near-identical
- page exists only to catch long-tail keywords with no real utility

### Internal Linking Expectations

- inbound from template hubs, feature pages, and related workflow pages
- outbound to related templates, setup docs, and product capability pages

### Schema Suggestions

- `Article` in many cases
- `BreadcrumbList`
- sometimes `CollectionPage` for template hubs

### Indexation Cautions

- define uniqueness and noindex rules before scaling the family
- retire or redirect stale templates that no longer reflect the product

## 6. Programmatic Page Family

### Best For

- entity, location, compatibility, catalog, or other repeatable high-intent surfaces with real unique data

### Search Intent

Varies, but the page must solve a distinct task with meaningful data or content, not merely a token swap.

### Minimum Content Blocks

- unique intro or summary
- distinctive data or attributes
- contextual proof, support, or comparison information
- links back to a hub and to nearby relevant pages
- clear CTA or next step

### Common Failure Modes

- token-swapped copy with no unique value
- no hubs or inbound links
- all pages indexed regardless of quality
- stale or empty pages left live as `200`

### Internal Linking Expectations

- strong hub-and-spoke structure
- representative hubs link to spokes
- spokes link back to hubs and selectively to related siblings

### Schema Suggestions

- depends on the family: `CollectionPage`, `ItemList`, `Article`, `LocalBusiness`, or another truthful type

### Indexation Cautions

- define noindex rules for weak variants before launch
- define stale-page retirement rules before scaling
- do not ship the family until data quality and uniqueness thresholds are operational

## 7. Category Or Collection Page

### Best For

- category intent, curated solution groups, or high-value list pages

### Search Intent

Informational or commercial browsing intent. The searcher wants help choosing among a grouped set.

### Minimum Content Blocks

- category explanation
- selection or buyer guidance
- featured children with summaries
- FAQs or curation logic
- body links to important child pages

### Common Failure Modes

- empty shell with cards only
- child pages exist but the category gives no decision help
- faceted states outrank the real category owner

### Internal Linking Expectations

- inbound from higher-level hubs
- outbound to priority children and relevant supporting pages

### Schema Suggestions

- `CollectionPage`
- sometimes `ItemList`
- `BreadcrumbList`

### Indexation Cautions

- noindex empty or low-value category states
- keep curated landing pages distinct from generic filter combinations

## 8. Location / Entity Page

### Best For

- real local intent or real entity-driven discovery

### Search Intent

Usually local or entity-specific intent. The searcher expects location or entity details, not generic company copy.

### Minimum Content Blocks

- localized or entity-specific details
- meaningful differentiators
- proof, data, or operational specifics
- related nearby or sibling entities when useful

### Common Failure Modes

- city-name swaps with identical body content
- no unique proof or local specifics
- local schema with no real local presence

### Internal Linking Expectations

- inbound from location or entity hubs
- outbound to relevant nearby or related entities and supporting product pages

### Schema Suggestions

- `LocalBusiness` only for real local entities
- `BreadcrumbList`

### Indexation Cautions

- noindex or avoid publishing token-swapped local clones
- retire empty or unsupported entity pages instead of leaving soft 404s
