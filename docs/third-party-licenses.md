# Third-party licenses and attribution

The root [LICENSE](../LICENSE) remains MIT for collection-owned material. It does
not relicense upstream contributions. Aggregate SPDX expressions describe a
collection of separately licensed components, not an option to apply MIT to all
files: marketplace `MIT AND Apache-2.0 AND CC-BY-4.0`; core-development and
infrastructure `MIT AND Apache-2.0`; marketing `MIT AND CC-BY-4.0`.
Other plugin license metadata is unchanged.

## Imported component scope

The [48-entry public migration map](imported-skill-map.json) identifies every
import, public package path, immutable source and component license expression.
Follow each package's `ORIGIN.md` for source revision and modification notices;
its complete `LICENSE`, original per-file notices and applicable `NOTICE` take
precedence over this navigation summary. Preserve those materials on redistribution.

| Component | Imported entries | License and retained attribution |
| --- | ---: | --- |
| Timescale pg-aiguide | 5 | Apache-2.0; full `LICENSE` and `NOTICE` in each package; Copyright 2025 Timescale, Inc., d/b/a Tiger Data |
| Redis agent-skills | 1 | MIT; Copyright (c) 2026 Redis, Inc.; package `LICENSE` |
| Stripe guides | 2 | MIT; Copyright (c) 2024–2025 Stripe; package `LICENSE` |
| Cloudflare skills | 1 | Apache-2.0; package `LICENSE` and `ORIGIN.md` |
| LinkedIn skills | 12 | MIT; Copyright (c) 2026 Sergey Bulaev; package `LICENSE` |
| Email Marketing Bible | 1 | MIT; Copyright (c) 2026 George Hartley; package `LICENSE` and author disclosures |
| claude-seo knowledge | 26 | MIT except the separately licensed FLOW material below; package `LICENSE`, original `LICENSE.txt` where present, origin and contributor notices retained |

claude-seo's repository MIT notice is Copyright (c) 2026 agricidaniel. Original
per-skill notices include AgriciDaniel and, for content-brief, puneetindersingh;
origin records retain additional credited contributors where supplied.

## FLOW mixed-license scope

In [marketing-seo-flow](../plugins/marketing/skills/marketing-seo-flow/ORIGIN.md),
the framework, bibliography, prompt index and all 41 prompt bodies are
© Daniel Agrici, licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Original source: [AgriciDaniel/flow](https://github.com/AgriciDaniel/flow), as embedded
in [the pinned claude-seo revision](https://github.com/AgriciDaniel/claude-seo/tree/6be93f45064ffbadced572b5d5c95f55fd263af0/skills/seo-flow).
Full legal code is packaged in
[LICENSE-CC-BY-4.0.txt](../plugins/marketing/skills/marketing-seo-flow/LICENSE-CC-BY-4.0.txt);
[NOTICE.md](../plugins/marketing/skills/marketing-seo-flow/NOTICE.md) records scope,
attribution and adaptations. Prompt bodies and source headers are retained
unchanged; entry organization, peer routing, runtime/authority guidance and the
framework SVG link were adapted. The relocated `assets/framework.svg` is the
claude-seo repository's MIT illustration, not relabeled CC BY content.
The package's aggregate expression is `MIT AND CC-BY-4.0`, not MIT-only.

Keep creator credits, source and license links, disclaimer notices and indications
of modifications when sharing CC BY material; consult the full legal code for
conditions and other rights. This guide is a rights-navigation aid, not legal
advice, a legal certification or release approval. Redistribution implies no
upstream sponsorship, endorsement, trademark grant or operational compatibility.
