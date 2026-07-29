---
name: business-product-jira
description: Manage Jira issues, boards, sprints, and projects via the jira-cli. Search, create, update, and transition issues directly from the command line.
metadata: {"clawdbot":{"emoji":"🎫","requires":{"bins":["jira"]},"install":[{"id":"brew","kind":"brew","formula":"jira-cli","bins":["jira"],"label":"Install jira-cli (brew)"}]}}
---

# jira

[jira-cli project](https://github.com/ankitpokhrel/jira-cli)

Use `jira` to manage Jira issues, sprints, and boards. Requires API token setup.

## Setup (once)

1. Generate an API token: https://id.atlassian.com/manage-profile/security/api-tokens
2. Export it for the current shell: `export JIRA_API_TOKEN="<API_TOKEN>"`. Do not put tokens in shell startup files, tracked configuration, or command history.
3. Run `jira init`, then select the installation type and provide the server and account details when prompted.

## Common commands

### Issues
- List issues: `jira issue list -p PROJECT`
- View issue: `jira issue view PROJ-123`
- Create issue: `jira issue create -p PROJECT -t "Task" -s "Summary" -b "Description"`
- Edit issue: `jira issue edit PROJ-123 -s "New summary"`
- Assign issue: `jira issue assign PROJ-123 "assignee@example.com"`
- Transition issue: `jira issue move PROJ-123 "In Progress"`
- Comment: `jira issue comment add PROJ-123 "My comment"`
- Search (JQL): `jira issue list -q "project = MKT AND status = 'To Do'"`

### Sprints
- List sprints: `jira sprint list -p PROJECT`
- View active sprint: `jira sprint list -p PROJECT --state active`
- Sprint issues: `jira sprint list -p PROJECT --state active --plain`

### Boards
- List boards: `jira board list -p PROJECT`

### Epics
- List epics: `jira epic list -p PROJECT`
- View epic: `jira epic view PROJ-100`

### Projects
- List projects: `jira project list`

## Output formats
- `--plain` — Tab-separated, no colors (best for scripting)
- `--columns key,summary,status` — Select columns
- `--no-truncate` — Don't truncate long fields

## Tips
- Set default project in config: `~/.config/.jira/.config.yml`
- Use JQL for complex queries: `-q "assignee = currentUser() AND status != Done"`
- Open in browser: `jira open PROJ-123`

## Notes
- Confirm with user before creating/editing/transitioning issues
- For bulk operations, show what will change before executing
