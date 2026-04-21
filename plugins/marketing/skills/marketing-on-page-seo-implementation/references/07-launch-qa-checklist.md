# Launch QA Checklist

Run this before and after launch. Validate the rendered result and the production behavior, not only the code diff.

## Goal

Use launch QA as a release gate for search-facing surfaces. This checklist separates blockers from warnings so teams can make deliberate decisions instead of shipping on vague optimism.

## Output Format

Record:

- URL checked
- environment checked
- date and time
- blocker list
- warning list
- evidence or screenshots when needed
- follow-up owner

## Blocking Failures

These should stop launch until fixed:

- wrong canonical or missing canonical on an indexable page
- wrong robots or noindex behavior
- page returns the wrong status code
- rendered HTML is missing primary explanatory content
- page is unintentionally thin relative to the declared intent
- title, H1, URL, and canonical point at different intents
- schema materially contradicts visible content
- important page has no meaningful internal link path
- replaced URLs do not redirect correctly
- sitemap includes the wrong URL state for the page

## Warnings

Warnings do not automatically stop launch, but should be explicitly accepted or queued:

- title or meta description could be stronger
- internal linking is present but still lighter than ideal
- proof blocks are thinner than competitors
- mobile UX or performance is acceptable but not strong
- schema is valid but conservative
- supporting sibling links are incomplete

## Pre-Launch Gate

### 1. Indexation And Canonical

- [ ] page returns intended status code
- [ ] canonical exists and points to the intended URL
- [ ] page is indexable only if it deserves to rank
- [ ] robots and noindex policy match the page plan
- [ ] sitemap inclusion or exclusion rule is defined

### 2. Metadata Alignment

- [ ] unique `title`
- [ ] unique meta description
- [ ] one meaningful H1
- [ ] URL, title, H1, and canonical align on the same intent

### 3. Rendered Content

- [ ] rendered HTML contains primary explanatory content
- [ ] page is not thin for its page type and target intent
- [ ] key proof, setup, comparison, or FAQ content is visible without relying on hidden interactions

### 4. Structured Data

- [ ] correct schema type selected
- [ ] JSON-LD validates
- [ ] schema matches visible content and real data

### 5. Internal Linking

- [ ] page has an inbound path from a relevant hub or stronger surface
- [ ] page includes useful outbound links where a next step exists
- [ ] important links appear in body content, not only nav or footer

### 6. Technical Quality

- [ ] mobile layout is sane
- [ ] major console or runtime issues do not block rendering
- [ ] critical assets are optimized
- [ ] there is at least a Core Web Vitals sanity check

## Production Verification

After deploy, re-check in production:

- [ ] final HTML matches expected title, description, H1, and body copy
- [ ] canonical and robots values are correct in production
- [ ] page appears in sitemap only if intended
- [ ] redirects behave correctly from replaced URLs
- [ ] parameter, locale, or facet variants follow the written policy
- [ ] monitoring paths are known for analytics and search console follow-up

## Re-Audit Triggers

Re-run QA after:

- framework migration
- route refactor
- metadata API change
- CMS or data-model change
- design rewrite that alters content order or visibility
- introducing filters, pagination, locale routing, or new programmatic variants

## Suggested Evidence

- rendered page source or HTML snapshot
- screenshot of the live page
- canonical and robots values checked
- redirect proof for replaced URLs
- brief pass/fail notes with owners
