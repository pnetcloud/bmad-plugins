# Skill Improvement Receipt Example

```text
Improved: example-skill
Changed: tightened triggers; added an explicit failure path; made source selection conditional
Retired: one exact generated duplicate; retained the authoritative example
Preserved: provider workflows moved to references/provider.md; output template retained in assets/
Structure: SKILL.md 176 → 164 lines; provider details remain reachable in references/provider.md
Retention: 9 capabilities accounted for; large-deletion gate not triggered
Evidence: structure validator; 12 tests; baseline capability scenarios plus positive, negative, main, and permission-denied cases
Sources: adopted one retrieval rule from source/revision/license; rejected installer and credential handling
Security: 0 blocking findings; two heuristic warnings reviewed as defensive guidance
Review: one link finding patched; no unresolved blocking findings
Remaining: provider B behavior needs runtime evidence
```

The receipt reports behavioral evidence, preservation, and unresolved
uncertainty. It does not treat fewer lines, fewer files, or a scanner score as
proof of improvement. When the large-deletion gate triggers, attach the
capability-retention matrix and the separate information-loss review.
