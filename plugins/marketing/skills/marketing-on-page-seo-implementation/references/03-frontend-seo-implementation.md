# Frontend SEO Implementation

This document defines what frontend developers must implement so indexable pages are understandable, crawlable, and competitive in rendered output.

## Goal

Make sure ranking-critical signals are present in rendered HTML, not implied by design comps or injected too late by the client.

## Frontend Ownership

Frontend owns:

- rendered primary content
- heading structure
- metadata plumbing exposed by the framework
- visible internal links
- breadcrumbs when used
- media semantics
- the rendering strategy for ranking-critical content

If the page is meant to rank, frontend cannot treat SEO fields as optional garnish.

## 1. Render The Important Content On First Response

Critical elements should exist in rendered HTML:

- `title`
- `meta name="description"`
- canonical
- H1
- intro copy
- core explanatory sections
- breadcrumbs when shown
- structured data
- important internal links

Do not depend on:

- late hydration to inject primary body copy
- client-only fetches for the core descriptive block
- hidden tabs or accordions for the only meaningful content
- screenshots replacing explanatory text
- JS-only link rendering for important navigation between related pages

## 2. Choose The Right Render Mode

Pick the simplest render strategy that still makes the page reliable and fast.

### SSR

Use when content is dynamic and must be fresh on every request, but still needs full server-rendered HTML.

### SSG

Use when content is stable and can be shipped fully at build time.

### ISR Or Hybrid

Use when pages are mostly static but need controlled freshness. Define revalidation so metadata, schema, and canonical output stay in sync.

### Client-Heavy SPA Patterns

If the page should rank, provide SSR, SSG, or a server-rendered fallback for the primary value-bearing content. Do not assume bots or users should wait for the app shell to become meaningful.

## 3. Metadata Must Be Deterministic

Each indexable page should ship unique:

- `title`
- meta description
- canonical
- Open Graph and Twitter metadata when supported

Avoid:

- app-wide fallback titles on indexable pages
- repeated descriptions across page families
- canonicals computed from unstable client state
- framework hacks that mutate metadata after initial render

## 4. Heading Discipline

- one meaningful H1 per page
- H2 and H3 structure should reflect content structure, not styling convenience
- headings should describe the section’s actual content
- decorative UI headings do not replace semantic section headings

Bad patterns:

- hero slogan as H1 with no clue what the page solves
- multiple H1s because components were reused carelessly
- visual headings implemented as `div` elements while the real document outline stays weak

## 5. Visible Body Content Must Satisfy Intent

The page should answer the target query with visible, useful body content.

Good content blocks include:

- product or feature explanation
- setup or implementation guidance
- use cases
- compatibility details
- screenshots with captions
- proof or evidence blocks
- comparison tables
- FAQs that answer real objections

Thin-page warning signs:

- hero plus CTA plus testimonials only
- repeated marketing boilerplate across many URLs
- page body that becomes meaningful only after clicking UI controls
- layout cards and icon grids with almost no explanatory copy

## 6. Internal Links Must Be Useful, Not Decorative

Important pages need contextual body links.

Good:

- feature page links to pricing, related features, docs, and integrations
- docs page links back to feature or product pages when evaluation context matters
- comparison page links to migration, proof, and pricing

Bad:

- important pages discoverable only through nav, footer, or sitemap
- every page linking to every other page
- generic anchors like `learn more`
- keyword-stuffed footer blocks used as a ranking crutch

## 7. Media And Image Semantics

- use meaningful filenames when practical
- write alt text for informative images
- keep alt text descriptive, not stuffed
- add captions when the image proves a claim or explains a workflow
- never place the only useful explanation inside an image

If screenshots are central evidence, describe what the screenshot shows in nearby text.

## 8. Structured Data Rendering

- prefer JSON-LD
- render schema with the page, not after fragile client mutations
- ensure schema matches visible content and current route state
- validate that the final HTML contains the intended JSON-LD

## 9. UX And Performance Still Matter

Frontend SEO includes UX quality:

- protect LCP by optimizing hero assets and reducing server delay
- protect INP by limiting heavy client work on landing surfaces
- protect CLS with fixed dimensions and stable layout
- verify mobile readability, tap targets, and scanning flow

Slow, unstable pages can satisfy metadata requirements yet still underperform.

## 10. Review Patterns That Often Break SEO

Watch closely during:

- framework migrations
- design rewrites that move core content into tabs or carousels
- CMS refactors that centralize metadata defaults
- component abstraction that duplicates H1s or strips semantics
- personalization that changes the primary copy too aggressively

## Frontend Done Criteria

- rendered HTML contains the intended primary copy and metadata
- page has one clear H1 and a coherent heading structure
- important internal links appear in body content
- schema is present and valid
- primary explanatory content is not hidden behind client interaction
- mobile layout and Core Web Vitals have at least a sanity-pass review
