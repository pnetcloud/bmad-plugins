# Public Skill Publication Safety

Read this reference only when the target skill will enter a public repository or
distribution.

## Contents

- Two-Layer Gate
- Policy Shape
- Blocking Surface
- Optional Operator-Reviewed PNG Exception
- Markdown Code and Link Checks
- Abstract the Origin, Not the Method
- Limits

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
  "allowed_email_domains": ["example.com"],
  "allowed_email_addresses": []
}
```

Use literals for exact names and regexes for identifier families. Keep domain
and environment allowlists narrow. Do not add private terms to tracked fixtures
or documentation merely to test the policy.

The optional `allowed_email_addresses` list defaults to empty and grants only
exact, case-sensitive mailbox matches, for example `author@example.com`. It does
not grant other mailboxes at that domain, subdomains, or substring matches.
Entries must be bare ASCII addresses with valid dotted DNS labels and a local
part of at most 64 characters; display names, wildcards, whitespace, empty or
non-string entries, malformed labels and addresses over 254 characters invalidate
the policy. Use this narrow field for independently verified public attribution
contacts instead of allowlisting an entire shared mail-provider domain. Existing
reserved-example and `allowed_email_domains` behavior remains unchanged; private
policy, secret and other content checks are not bypassed by an email approval.

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

## Optional Operator-Reviewed PNG Exception

By default, binary/opaque and oversized files remain blocking, including PNGs.
Only a trusted operator's private policy supplied through `--public-policy` may
add the optional `reviewed_assets` list. Never accept an imported package's
self-declared approval, generate approvals automatically, or trust a policy
supplied alongside an untrusted skill. Keep the required nonempty private-term
policy; asset approval does not replace it.

Example descriptor to add to that list (the all-zero hash is a placeholder,
not an approval; replace both hash and size with the reviewed file's values):

```json
{
  "skill": "example-skill",
  "path": "assets/icon.png",
  "sha256": "0000000000000000000000000000000000000000000000000000000000000000",
  "size": 1234,
  "format": "png"
}
```

Every descriptor must contain exactly these five typed fields. Use a lowercase
kebab-case skill ID and a skill-root-relative ASCII path with `/` separators,
no absolute paths, empty segments, `.` or `..`, and the exact `.png` suffix.
Paths accept only ASCII letters, digits, `_`, `-`, `.` and `/`. SHA-256 must be
64 hexadecimal characters. Size must be a positive integer (not a boolean) no
larger than the existing 2,000,000-byte scan limit. Only `png` is supported;
unknown fields/formats, duplicate skill/path pairs and malformed descriptors
invalidate the policy. Omitting the list is backward-compatible; an empty list
approves nothing.

Before approval, establish redistribution/source authority and independently
review the exact image, all chunks/metadata and embedded content. Record that
assessment privately. Visual inspection alone cannot establish metadata safety
or absence of secrets. Do not use path patterns, directory-wide binary
allowlists or hashes without skill/path context.

The scanner matches the directory's exact skill ID, relative path, SHA-256 and
byte count. Normal package path, private-term and symlink checks still apply
before the exception; text secret/environment checks remain unchanged.
Nonmatching opaque files stay blocking. Matching descriptors with changed bytes,
invalid structure or unsupported images produce a blocking finding.

PNG checks cover signature, bounded chunks and CRCs, first/unique IHDR, legal
color/bit-depth combinations, positive dimensions (at most 4096 per axis and
4,194,304 pixels), palette/IDAT ordering, bounded zlib scanlines and filters,
final IEND and absence of trailing file/compressed payload. Static PNG only:
APNG and unknown critical chunks fail closed. There may be at most 4096 chunks
and 33,558,528 decompressed image bytes. These checks are not a full image decoder,
ancillary-metadata sanitizer or proof of secret absence. Ancillary content is
covered by the operator's exact-byte review, not automatically labeled clean.

An accepted file emits `public-reviewed-asset` as a warning with its skill,
path, digest, size and dimensions. Retain and disposition that evidence during
review; it is a narrow manual-review exception, not a general publication verdict.

## Markdown Code and Link Checks

The scanner requires the maintained `markdown-it-py==3.0.0` CommonMark parser
and its `mdurl==0.1.2` dependency, pinned in `scripts/requirements.txt`. Use an
isolated environment; for example, with uv, run:

```bash
uv venv .venv
uv pip install --python .venv/bin/python -r <skill-improver-dir>/scripts/requirements.txt
.venv/bin/python <skill-improver-dir>/scripts/scan_skill.py <target-skill-dir>
```

Missing dependencies stop execution with a nonzero error, not a successful scan.
No vendored parser, external parser plugins or heuristic block fallback is used.
CommonMark block tokens decide fenced/indented code and actual inline contexts;
an observer delegates to the parser's unchanged backtick rule to record matched
code spans, including variable-length delimiters and multiline container content.
Original character/newline offsets are retained through an explicit source map.
If parsing or exact source mapping fails, `markdown-parse-error` blocks release;
unmasked legacy link checks and original-text security checks still run. Mapping
uncertainty is not a clean scan and may require manual review.

Legacy inline-link, local-target and undefined-reference checks are retained,
with parsed reference definitions also checked, including multiline labels and
continuation titles. The link recognizers remain a bounded static gate, not a
complete CommonMark link validator; parsed block/code handling does not certify
every possible link syntax. Undefined reference-style uses remain blocking even
when a renderer would leave them as literal text. HTML text is not code merely
because it contains backticks.
Code masking applies only to Markdown link interpretation: secret, private-term,
hidden-Unicode and environment-variable checks still inspect the original text,
including inline and fenced code.

## Abstract the Origin, Not the Method

A public skill may be specific to a public discipline, standard, framework, or
technology. It must remain abstract about the private organization, project,
customer, case, dataset, strategy, and implementation that produced the lesson.

Apply this boundary equally to chats, persistent memories, knowledge-base notes,
and summaries derived from them. Retrieval authorization is not publication
authorization. Keep personal preferences, project-specific policy, private source
locators, and provenance outside public artifacts, metadata, and commit messages.
Publish a rule only when it remains useful without the originating user's setup;
otherwise retain it privately rather than disguising it as universal guidance.

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
