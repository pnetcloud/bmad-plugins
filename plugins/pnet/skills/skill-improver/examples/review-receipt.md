# Skill Improvement Receipt Example

```text
Improved: example-skill
Changed: tightened triggers; added an explicit failure path; made source selection conditional
Removed: duplicated examples and an unavailable tool assumption
Structure: SKILL.md 340 → 142 lines; moved provider details to references/provider.md
Evidence: structure validator; 12 tests; positive, negative, main, and permission-denied scenarios
Sources: adopted one retrieval rule from source/revision/license; rejected installer and credential handling
Security: 0 blocking findings; two heuristic warnings reviewed as defensive guidance
Review: one link finding patched; no unresolved blocking findings
Remaining: provider B behavior needs runtime evidence
```

The receipt reports behavioral evidence and unresolved uncertainty. It does not treat fewer lines or a scanner score as proof of improvement.
