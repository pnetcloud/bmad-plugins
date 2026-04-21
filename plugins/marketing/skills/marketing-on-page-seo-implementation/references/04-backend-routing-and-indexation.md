# Backend Routing And Indexation

This document covers the backend and platform rules that decide which URLs search engines discover, consolidate, ignore, or retire.

## Goal

Ensure the platform exposes one clean canonical surface per intent and does not leak duplicate, stale, or low-value URLs into crawl and index workflows.

## Backend / Platform Ownership

Backend or platform owns:

- route design
- canonical consistency
- redirect lifecycle
- robots and noindex controls
- sitemap generation
- parameter, facet, and pagination policy
- locale routing
- status codes and stale-page retirement

## 1. Stable URL Design

- use readable lowercase hyphenated slugs
- prefer subfolders over subdomains for related content families unless there is a strong operational reason not to
- keep patterns consistent within a page family
- avoid canonical URLs that include unnecessary parameters
- do not let CMS or router convenience create multiple public paths for the same page

If two URLs can serve the same page, define which one is canonical and why.

## 2. Canonical Rules

Each indexable page should have one canonical URL.

Canonical signals should agree with:

- router output
- rendered canonical tag
- sitemap entry
- internal links
- redirect rules
- hreflang targets when used

### Use Canonicals When

- alternate states must remain accessible to users
- small variants exist but should consolidate to one owner
- filtered or sorted views have UX value but not search value

### Prefer Redirects When

- the weaker URL should stop existing
- a migration replaced one route with another
- legacy duplicates are still reachable

Weak canonical setups often hide page inventory problems instead of solving them.

## 3. Redirect Lifecycle

- moved page: `301`
- temporarily moved experience: use a temporary redirect only when truly temporary
- permanently removed page with no replacement: `410` when appropriate, otherwise `404`
- avoid redirect chains
- avoid redirecting every retired page to the homepage

If a page family is regenerated regularly, define what happens when a page no longer meets quality or data thresholds.

## 4. Robots And Indexation Policy

Explicitly classify pages as:

- canonical and indexable
- user-accessible but noindex
- blocked from crawl
- excluded from sitemap

Common non-indexable candidates:

- internal search results
- faceted filter combinations
- sort states
- session or preview URLs
- empty taxonomies
- weak programmatic variants

Do not confuse “blocked from crawl” with “should not be indexed.” Use the correct control for the goal.

## 5. Sitemap Rules

Sitemaps should include only URLs that are:

- canonical
- indexable
- `200`
- intended to rank

Do not include:

- redirects
- `404` or `410`
- noindex pages
- parameter variants
- canonicalized duplicates

For larger sites, split sitemaps by page family so failures are easier to inspect.

## 6. Pagination, Facets, And Parameters

This is where many product sites lose index control.

Define rules for:

- filter states
- sort orders
- tracking parameters
- page-size parameters
- search result URLs
- experimental query params

### Practical Defaults

- canonicalize low-value filtered variants to the base category or parent page
- noindex low-value combinations that still need to exist for users
- allow indexation only for intentionally curated facet landing pages
- strip tracking parameters from canonical logic

If a parameter can create infinite crawl space, the policy is incomplete.

## 7. Programmatic Page Families

Before generating a family, define:

- allowed URL pattern
- source data contract
- minimum uniqueness threshold
- index vs noindex criteria
- internal link source hubs
- stale-page retirement path
- what returns `404` or `410`

### Programmatic Failure Modes

- pages published with insufficient source data
- pages that stay indexable after becoming empty or stale
- hubs that do not link to spokes
- thousands of low-value `200` pages competing with a few good ones

## 8. Hreflang And Locale Routing

If the site is multi-language or multi-region:

- keep locale URL patterns consistent
- ensure reciprocal hreflang relationships
- do not canonicalize all locales to one language
- localize meaningfully; shallow translation clones can still be weak pages

Locale pages need their own ownership and quality rules, not just translated metadata.

## 9. Status Codes And Soft 404 Prevention

Do not return `200` for:

- empty entity pages
- expired records with no valid content
- placeholder integrations
- programmatic pages below the minimum quality threshold

Soft 404 behavior often comes from product convenience, not malicious intent. Fix it anyway.

## 10. Production Guardrails

Validate in production:

- canonical tag values
- robots and noindex behavior
- sitemap entries
- redirect behavior
- parameter handling
- removed-page responses

Indexation policy is not done when it works locally.

## Backend Done Criteria

- canonical rules are documented and implemented
- sitemap contains only valid canonical URLs
- redirects are direct and intentional
- facet and parameter behavior is controlled
- stale, removed, and moved URLs have lifecycle handling
- production behavior matches the written policy
