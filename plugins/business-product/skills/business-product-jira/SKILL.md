---
name: business-product-jira
description: Manage Jira issues, boards, sprints, and projects via the jira-cli. Search, create, update, and transition issues directly from the command line.
metadata: {"clawdbot":{"emoji":"🎫","requires":{"bins":["jira"]},"install":[{"id":"brew","kind":"brew","formula":"jira-cli","bins":["jira"],"label":"Install jira-cli (brew)"}]}}
---

# jira

## Purpose and selection

[jira-cli project](https://github.com/ankitpokhrel/jira-cli)

Use `jira` to manage Jira issues, sprints, and boards. Requires API token setup.



Select for Jira reads and explicitly requested management operations through this CLI; not for unrelated issue trackers or automatic account setup.

## Working mode

Inspect the installed CLI and active account first. Setup below is needed only when missing; installation and configuration require separate authorization. Ask for missing site or target identifiers rather than guessing. Keep tokens in approved credential handling and out of reports.

### Setup (once)

1. Generate an API token: https://id.atlassian.com/manage-profile/security/api-tokens
2. Export it for the current shell: `export JIRA_API_TOKEN="<API_TOKEN>"`. Do not put tokens in shell startup files, tracked configuration, or command history.
3. Run `jira init`, then select the installation type and provide the server and account details when prompted.

## Focus

### Common commands

#### Issues
- List issues: `jira issue list -p PROJECT`
- View issue: `jira issue view PROJ-123`
- Create issue: `jira issue create -p PROJECT -t "Task" -s "Summary" -b "Description"`
- Edit issue: `jira issue edit PROJ-123 -s "New summary"`
- Assign issue: `jira issue assign PROJ-123 "assignee@example.com"`
- Transition issue: `jira issue move PROJ-123 "In Progress"`
- Comment: `jira issue comment add PROJ-123 "My comment"`
- Search (JQL): `jira issue list -q "project = MKT AND status = 'To Do'"`

#### Sprints
- List sprints: `jira sprint list -p PROJECT`
- View active sprint: `jira sprint list -p PROJECT --state active`
- Sprint issues: `jira sprint list -p PROJECT --state active --plain`

#### Boards
- List boards: `jira board list -p PROJECT`

#### Epics
- List epics: `jira epic list -p PROJECT`
- View epic: `jira epic view PROJ-100`

#### Projects
- List projects: `jira project list`

### Output formats
- `--plain` — Tab-separated, no colors (best for scripting)
- `--columns key,summary,status` — Select columns
- `--no-truncate` — Don't truncate long fields

### Tips
- Set default project in config: `~/.config/.jira/.config.yml`
- Use JQL for complex queries: `-q "assignee = currentUser() AND status != Done"`
- Open in browser: `jira open PROJ-123`

## Quality checks

Confirm the active site, account and exact target before execution. Distinguish CLI availability from successful authentication and access. After an authorized write, read back the exact page or issue and verify requested fields, hierarchy or state. Report failures and checks not run; do not infer success from a submitted command.

## Return

Return the requested Jira content or action result with actual page or issue identifiers, source links when available, verification and limitations. For local exports, report the authorized output path and observed files. Never return API tokens.

## Boundaries

### Notes
- Confirm with user before creating/editing/transitioning issues
- For bulk operations, show what will change before executing

Read access and this skill do not authorize writes, installation or reconfiguration. Confirm the exact site, target and final payload before creating or updating content; for Jira also confirm assignment, transition and comment operations. Preview bulk changes. Export only to an authorized location and minimize confidential data. Stop on ambiguous targets, missing permissions or uncertain write results; reconcile before retrying.
