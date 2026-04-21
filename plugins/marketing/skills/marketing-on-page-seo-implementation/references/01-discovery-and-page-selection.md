# Discovery And Page Selection

Run this before implementation. SEO debt usually starts before code is written: the wrong page gets approved, the wrong surface owns the query, or multiple teams publish overlapping URLs.

## Goal

Decide whether a page should exist, whether it should be indexable, which surface should own the intent, and what should happen to overlapping URLs.

## Required Outputs

Before coding, produce:

- target page inventory
- page owner per URL or page family
- overlap and cannibalization notes
- keep, merge, redirect, canonicalize, noindex, or remove decision per overlapping URL
- final list of pages that deserve implementation

## Step 1: Identify The Surface

For each requested page or page family, capture:

- page type: feature, integration, docs, comparison, alternative, template, glossary, pricing, category, location, entity, programmatic family
- business goal: signup, demo, trial, purchase, activation, qualified traffic, implementation success, expansion
- primary audience: evaluator, buyer, implementer, existing customer, researcher
- canonical owner: product, docs, marketing, support, marketplace
- expected maintenance owner: who will keep the page accurate after launch

If no team can own the page after launch, treat that as a warning. Unowned pages go stale fast.

## Step 2: Define The Query Cluster And Intent

Every indexable page needs one primary query cluster.

Document:

- primary query
- 3 to 8 supporting queries
- search intent: informational, commercial, transactional, navigational, mixed
- why this page is the right destination for that intent
- why another existing surface should not own it instead

If the team cannot explain the intent in one sentence, the page is not ready.

## Step 3: Identify The Intent Owner

Do not skip this when product, docs, blog, or comparison pages overlap.

### Typical Ownership Rules

- Product page owns solution and commercial intent.
- Docs page owns setup, API, troubleshooting, and implementation-depth intent.
- Comparison page owns evaluation intent only when the comparison is substantive.
- Template page owns intent only when the template itself is the answer, not merely a CTA wrapper.
- Programmatic page owns intent only when the page can deliver distinct value at scale.

### Common Ownership Conflicts

| Conflict | Default resolution |
|---|---|
| Product page vs docs page for a buying query | Product page should own it |
| Docs page vs glossary page for a definitional query | Choose the page with the better user task fit |
| Comparison page vs feature page for branded competitor intent | Comparison page can own it if it is honest and complete |
| Template page vs generic feature page | Template page should own only template-seeking intent |

If ownership is unclear, do not create a second indexable page yet.

## Step 4: Audit Existing Coverage

Inspect the current site for pages already targeting the same or adjacent intent.

Flag:

- duplicate targeting
- keyword cannibalization
- thin legacy pages that should redirect
- pages that should become hubs and link to the new surface
- pages that should be merged into the new surface
- docs pages that unintentionally outrank product pages
- parameter, locale, or facet variants masquerading as unique pages

## Step 5: Choose The Right Outcome

Use the strongest clean solution. Do not hide weak inventory behind soft canonicals if the page should not survive.

| Situation | Correct action |
|---|---|
| Existing page already satisfies intent | Improve the existing page |
| Two pages target the same intent and only one should remain | Merge and `301` the weaker page |
| Alternate state is useful for users but not for search | Canonicalize or noindex the alternate state |
| Page serves product UX but is poor search inventory | Keep usable and noindex |
| New intent has no strong owner yet | Create one canonical page |
| Page has low unique value and no strong recovery path | Remove or never build |

### Redirect Vs Canonicalize Vs Noindex

- Redirect when the alternate URL should stop existing.
- Canonicalize when users still need the alternate experience but search should consolidate elsewhere.
- Noindex when the page should exist for users yet not compete in search.
- Merge when two pages dilute each other and the combined page will be better.

## Step 6: Decide Whether The Page Deserves Indexation

Indexable pages should have all of the following:

- clear intent match
- enough unique content, data, or utility to satisfy that intent
- stable URL pattern
- a defined place in site architecture
- inbound and outbound internal links
- a measurable business or topical role
- a realistic plan to keep the page accurate

Do not index pages that are only:

- thin filtered states
- empty taxonomies
- placeholder integrations
- city or entity clones with swapped tokens only
- search result pages without durable value
- one-paragraph templates with no preview, explanation, or implementation help

## Page-Type-Specific Go/No-Go Heuristics

### Feature Pages

Build when the feature solves a search-visible problem and the page can go beyond generic marketing copy.

Do not build if the feature is only a subsection of a stronger parent page and cannot sustain its own intent.

### Integration Pages

Build when the integration is real, maintained, and can explain setup, sync behavior, and limits.

Do not build placeholder “coming soon” integrations as indexable pages.

### Docs Pages

Build as indexable when the query clearly seeks instructions, APIs, troubleshooting, or implementation steps.

Do not force docs to own commercial queries that should land on product pages.

### Comparison / Alternatives Pages

Build when the page can explain differences, tradeoffs, proof, and next steps honestly.

Do not build doorway pages that simply repeat “X alternative” with a CTA.

### Template Pages

Build when the template has a distinct use case, preview, explanation, and meaningful differentiation from sibling templates.

Do not build large template sets before defining uniqueness and noindex rules.

### Programmatic Pages

Build only after defining:

- data source
- uniqueness threshold
- page template variability
- index vs noindex criteria
- internal link sources
- stale-page retirement policy

If those rules do not exist yet, delay the family.

## Common Failure Modes

### SaaS

- feature and pricing pages competing for the same query
- thin alternatives pages with no proof or switching guidance
- docs pages outranking product pages for solution intent

### E-commerce / Catalog

- facet combinations creating duplicate indexable URLs
- empty category pages returning `200`
- manufacturer-copy clones

### Docs / Developer Tools

- raw API references trying to rank without task framing
- changelog pages competing with docs or product intent
- duplicated guidance across docs, blog, and marketing

### Programmatic SEO

- shipping page families before validating uniqueness
- relying on sitemaps instead of real internal links
- giving weak pages `200` and full indexation by default

## Review Questions

- What exact query cluster does this page own?
- Why should this surface own it instead of product, docs, or another section?
- What existing URLs must be merged, redirected, noindexed, or de-emphasized?
- What makes the page uniquely valuable beyond template tokens?
- If traffic arrives here, what is the intended next step?
