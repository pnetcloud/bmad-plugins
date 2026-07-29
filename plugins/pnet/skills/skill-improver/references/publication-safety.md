# Public Skill Publication Safety

Read this reference only when the target skill will enter a public repository or
distribution.

## Two-Layer Gate

Use both:

1. generic detection for credential material, private paths and hosts, unsafe
   package files, hidden content, and structural failures;
2. an ignored private policy containing organization-specific product and
   architecture identifiers.

Keep the policy outside the target skill and public repository. Its absence,
invalidity, or lack of private terms is a blocking result.

## Policy Shape

Provide UTF-8 JSON:

```json
{
  "version": 1,
  "forbidden_literals": ["PRIVATE_PRODUCT_PLACEHOLDER"],
  "forbidden_regexes": ["\\\\binternal-codename-[0-9]+\\\\b"],
  "forbidden_domains": ["private.example"],
  "allowed_environment_variables": ["DOCUMENTED_PUBLIC_VARIABLE"],
  "allowed_email_domains": ["example.com"]
}
```

Use literals for exact names and regexes for identifier families. Keep domain
and environment allowlists narrow. Do not add private terms to tracked fixtures
or documentation merely to test the policy.

The validator reports policy entry numbers rather than matched values so private
terms do not leak into logs.

## Blocking Surface

Scan every file in the skill directory, not only `SKILL.md`. Resolve blocking
findings for:

- provider tokens, private keys, JWTs, non-placeholder credential assignments,
  and credential-bearing URLs or files;
- non-allowlisted environment variables;
- absolute workstation paths, private hosts and addresses, personal email, and
  private policy matches;
- non-ASCII package paths, symlinks, hidden Unicode, opaque files, oversized
  files, and broken or escaping references.

Use synthetic reserved domains and neutral placeholders in examples.

## Abstract the Origin, Not the Method

A public skill may be specific to a public discipline, standard, framework, or
technology. It must remain abstract about the private organization, project,
customer, case, dataset, strategy, and implementation that produced the lesson.

Do not pseudonymize a real example by changing only its names. Replace it with a
synthetic or composite example and alter identifying combinations of:

- names, terminology, roles, markets, products, and locations;
- exact numbers, dates, targets, thresholds, timing, and scale;
- topology, schemas, workflows, integrations, business rules, and chronology;
- incidents, prompts, payloads, reports, screenshots, and source phrasing.

Preserve the reusable decision, invariant, tradeoff, failure mode, authority
boundary, validation, and stop condition. This applies to engineering, product,
design, marketing, sales, finance, legal, research, operations, HR, and every
other skill domain.

Automated patterns cannot detect semantic or mosaic re-identification. Compare
the public artifact with its private source locally. If a knowledgeable outsider
could infer the source from the combination of details, generalize again. When
that would destroy the lesson, retain only the general rule or omit the example.
Keep a skill private when its value depends on the source-specific facts.

## Limits

Pattern scanning cannot prove absence of every encoded, fragmented, novel, or
historical secret. Pair this gate with the hosting platform's secret scanning or
a maintained independent scanner. If real credential material may have entered
version control, revoke or rotate it before separately authorized history
remediation.

Review plugin manifests, marketplace metadata, commit messages, staged changes,
licenses, and externally hosted assets because they may sit outside the skill
directory.
