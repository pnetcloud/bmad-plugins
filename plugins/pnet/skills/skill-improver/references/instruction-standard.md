# Agent Skill Instruction Standard

This is the authoring and maintenance contract for this collection. It applies
to each `SKILL.md`, including specialist-role skills, compact technical standards
and tool/workflow skills. A shared shape is not a license to erase domain depth
or claim uniform runtime support.

## Required entry contract

Keep valid skill frontmatter and stable public identifiers. After the skill title,
use these six level-two sections in this order. Existing topic headings belong
inside the relevant section; retain their meaning and usable anchors.

| Section | Required decision or behavior |
| --- | --- |
| Purpose and selection | State the assigned outcome, positive trigger and nearby non-trigger. Role identity is expertise, not a grant of tools or authority. |
| Working mode | Describe inputs, prerequisites, execution choices and missing-input handling. Order only genuinely dependent actions; retain exact commands for fragile operations. |
| Focus | Keep domain-specific rules, knowledge, concerns and directly selected resources. Do not replace expertise with a generic checklist. |
| Quality checks | Name observable acceptance evidence and required validation. Separate configured state, attempted execution, successful operation and accepted outcome. Mark checks not run honestly. |
| Return | Identify the requested artifact/result, relevant source or revision, checks, limitations, unresolved decisions and next owner where needed. Use task-appropriate output, not mandatory ceremonial reports. |
| Boundaries | State mutation/external-action authority, exclusions, delegation limits and stop conditions. Reading a skill or recommending a change grants no new permission. |

When skill or tool activation is needed, keep it as a conditional Working mode
subsection: identify the dependency or resolved source, selected operation and
actual startup evidence. A role name or greeting is not activation. Do not add
extra personas or activation stages to tasks that do not require them. Role,
model/profile and tool bindings remain host/project configuration, not new
permissions granted by skill prose.

Small skills may use one concise paragraph per section. Complex skills may keep
subsections, examples, scripts and references. Do not impose minimum lengths,
file counts, personas, model choices, schedules, finding quotas or mandatory
multi-agent stages. A heading check proves structure only, not instruction quality.

## Skill kinds

- **Specialist role:** keep a bounded responsibility and domain expertise. Separate
  the role from model/profile selection, host permissions and tool availability.
  Optional collaborators require an actual supported communication mechanism.
- **Technical standard:** retain precise rules and exceptions. Working mode applies
  them to the requested repository/artifact; checks verify the affected behavior.
  Do not inflate a short standard into a project-management workflow.
- **Tool/workflow:** state actual dependencies and distinguish reads from writes.
  Existing setup does not authorize global installation or reconfiguration.
  Keep valid command/API examples and safeguards; verify the exact target after
  authorized external writes. Never invent a tool because an example names one.

## Preservation and progressive disclosure

Before changing an existing skill, inspect its complete package and applicable
instructions. Inventory original rules, examples, scripts, references and output
contracts. Record the destination and validation for each moved or materially
replaced capability. Preserve identifiers, paths, useful content and existing
consumer contracts; a recovery copy in Git is not a usable replacement resource.

Keep task-critical safety and selection rules in the entry. Move conditional
material only when an actual task can select it directly; link the destination
with a read condition. Prefer a small in-place edit when moving material adds no
behavioral value. Do not add an archive-like catch-all merely to make the entry
look short. Existing code fences/templates must remain executable or reusable,
not be misparsed as instruction headings during reorganization.

For an explicitly authorized whole-collection migration, account for every
skill and original resource individually. The complete migration needs an
inventory and retention evidence; do not describe a standard document, one pilot
or a heading-only scan as a completed catalog migration.

## Group identity and imported skills

Use an existing functional plugin group when it fits; create a new group only
when it improves selection, not to duplicate the upstream repository layout.
New imported skills use a unique group-qualified ID. Keep the original name,
immutable source revision, applicable license and modification notes in a
public-safe origin record; ship complete required licenses and notices. A public
source URL alone is not redistribution permission. Hold private material and
unclear rights instead of silently publishing or assigning this collection's
license to third-party content.

An explicitly authorized rename needs an old-to-new map, collision and consumer
checks, and precise peer-reference updates. Do not rewrite historical source URLs,
external CLI names or example data as if they were skill identifiers. Existing
published IDs otherwise stay stable. Preserve upstream expertise and resources;
metadata, categorization and host bindings are not substitutes for domain content.

Check dependency closure, including scripts and shared references outside the
original skill subtree. Declare actual supported-host requirements and unresolved
prerequisites. Do not fabricate cross-host compatibility, native tool/role
registration or installed dependencies; do not execute imported instructions as
part of inspection. Publishing a dependency declaration is not installing it.

## Verification and adoption

Validate names/manifests, required section order, nonempty content, resource
reachability and affected executable behavior. Compare the original capability
inventory against actual retained content, not just word or file counts. Review
triggers, missing inputs, authority boundaries and expected returns using
representative tasks and nearby counterexamples. Obtain independent review for
structural, executable or security-sensitive changes.

Use the collection's publication-safety and independent secret-scanning gates
before public release. Keep private evidence and policy outside public payloads.
A published package is not proof that running sessions loaded it, and an orderly
entrypoint is not evidence of improved task success or latency.

## Design reference

The organization adapts the public
[Plex role-contract authoring model](https://github.com/pnetcloud/plex-ai/blob/23747aa9cd20d8828d01840cd110ece59f461bcf/docs/role-contracts.md#authoring-format)
to Agent Skills: purpose/selection plus a bounded execution contract. This is an
authoring convention, not native Plex role registration, a role renderer or a
runtime dependency on Plex. Skill frontmatter and host permissions stay distinct
from native agent-role metadata.
