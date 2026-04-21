# Internal Linking Patterns

Internal links are how the site declares importance, relationships, and next steps. They are not decoration. A page without meaningful links is usually a weak page, no matter how polished the metadata looks.

## Goal

Make sure important pages are discoverable through crawlable body links from the right hubs, and that each page points users and search engines to the next relevant step.

## Core Principles

1. Important pages need relevant inbound links from other important pages.
2. Links should exist in body content where they help the reader, not only in chrome.
3. Anchor text should describe the destination naturally.
4. The link graph should reflect site architecture, not arbitrary cross-promotion.
5. Page families need deliberate hub-and-spoke patterns.

## What Makes A Link Useful

A useful link does at least one of these:

- helps the reader complete the next step
- proves the page belongs in a real topic cluster
- connects product, docs, or comparison surfaces that support each other
- establishes hierarchy between hub pages and child pages

A decorative link does not. Examples of decorative linking:

- stuffing exact-match anchors into a footer block
- linking every page to every sibling
- hiding important links in JS-only widgets
- dropping a long “related pages” list with no contextual introduction

## Site-Level Linking Rules

- every indexable page should have at least one meaningful inbound path from a stronger page
- every page family should have at least one hub or parent surface
- important links should be visible in rendered HTML
- do not rely on XML sitemaps to compensate for poor internal linking
- nav and footer links are support signals, not enough on their own for deeper surfaces

## Tactical Patterns By Surface

### Product To Docs

Use when the product page makes an implementation claim that the docs validate.

Recommended links:

- feature page -> setup guide
- feature page -> API or implementation docs
- integration page -> install or configuration doc

Why it matters:

- product pages gain credibility and task completion support
- docs gain relevant inbound traffic from evaluators

### Docs To Product

Use when a docs page helps users evaluate or adopt a product capability.

Recommended links:

- setup doc -> feature page
- API guide -> product capability page
- troubleshooting doc -> product or status/help surface when appropriate

Do not turn docs into CTA spam. Link back when it genuinely helps the user understand the capability or next step.

### Feature Pages

Minimum expectations:

- link to pricing when relevant
- link to related features
- link to implementation docs or setup pages
- link to integrations or use cases that prove applicability

Failure mode:

- feature page exists in isolation and only links to generic top-nav destinations

### Integration Pages

Minimum expectations:

- link to integration setup docs
- link to the relevant product feature that uses the integration
- link to related integrations or workflows when the relationship is real
- link to limits, requirements, or migration help when appropriate

Failure mode:

- placeholder integration page with no route to actual setup or usage

### Docs Pages

Minimum expectations:

- link sideways to prerequisite and next-step docs
- link upward to a parent docs hub or section page
- link back to product or feature pages when product evaluation context matters
- link to templates, examples, or integrations when they complete the task

Failure mode:

- docs page can be reached only by search or sidebar filtering and never from relevant product surfaces

### Comparison / Alternatives Pages

Minimum expectations:

- link to pricing
- link to proof pages, feature pages, or customer evidence
- link to migration or onboarding help
- link to a comparison hub when a competitor family exists

Failure mode:

- page names a competitor but never links to the evidence or next step that justifies the claim

### Template Pages

Minimum expectations:

- link to related templates
- link to the product feature that powers the template
- link to setup, customization, or export guidance
- link back to the template hub or category

Failure mode:

- huge template library where pages are discoverable only through faceted browsing or sitemap inclusion

### Programmatic Pages

Minimum expectations:

- each page links to its hub
- hubs link to representative spokes
- sibling links exist only when the relationship is real
- weak pages are not left orphaned simply because they exist in a sitemap

Failure mode:

- programmatic pages have no meaningful inbound links and are effectively index-only inventory

### Glossary / Educational Pages

Minimum expectations:

- link to related concepts
- link to product pages when the concept becomes actionable
- link to docs when implementation depth is the natural next step

Failure mode:

- glossary content stays isolated from the product journey and never hands off to useful surfaces

## Anchor Text Rules

Good anchors:

- describe the destination clearly
- reflect the user’s likely next step
- vary naturally across contexts

Weak anchors:

- `click here`
- `learn more`
- repeated exact-match anchors everywhere
- vague “resources” language when the destination is specific

## Orphan Prevention

Every indexable page should have:

- an obvious parent or hub
- at least one meaningful inbound link path
- at least one useful outbound link when a next step exists

### Orphan Checks For Docs

- can the page be reached from a docs hub
- can the page be reached from at least one relevant product or integration surface when appropriate
- does the page point to next-step docs or product context

### Orphan Checks For Programmatic Pages

- does the hub actually link to representative pages
- do the pages have any contextual inbound links beyond sitemap exposure
- are weak pages being noindexed or retired instead of left isolated

## Common Anti-Patterns

- footer keyword dumps
- large related-link blocks with no editorial judgment
- every page linking to every other page in a cluster
- hidden JS-only links for important destinations
- links that exist visually but not as crawlable anchors
- programmatic pages discoverable only through sitemaps

## Linking Review Checklist

- What page or hub should naturally link to this page?
- Does that link exist in body content or a real sectional context?
- Does this page link to the next relevant step?
- Are the anchors descriptive without becoming manipulative?
- Are product, docs, comparison, and template surfaces connected where the journey genuinely crosses surfaces?
