---
name: business-product-confluence
description: Search and manage Confluence pages and spaces using confluence-cli. Read documentation, create pages, and navigate spaces.
metadata: {"clawdbot":{"emoji":"📄","primaryEnv":"CONFLUENCE_TOKEN","requires":{"bins":["confluence"],"env":["CONFLUENCE_TOKEN"]},"install":[{"id":"npm","kind":"node","package":"confluence-cli","bins":["confluence"],"label":"Install confluence-cli (npm)"}]}}
---

# Confluence

## Purpose and selection

[confluence-cli project](https://github.com/pchuri/confluence-cli)

Search and manage Confluence pages using confluence-cli.



Select for Confluence reads and explicitly requested management operations through this CLI; not for unrelated issue trackers or automatic account setup.

## Working mode

Inspect the installed CLI and active account first. Setup below is needed only when missing; installation and configuration require separate authorization. Ask for missing site or target identifiers rather than guessing. Keep tokens in approved credential handling and out of reports.

### REQUIRED: First-Time Setup

Before using this skill, complete these steps:

**Step 1: Install the CLI**

```bash
npm install -g confluence-cli
```

**Step 2: Get an API token**

1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Give it a label (e.g., "confluence-cli")
4. Copy the token

**Step 3: Configure the CLI**

```bash
confluence init
```

When prompted, enter:
- **Domain**: `yourcompany.atlassian.net` (without https://)
- **Email**: Your Atlassian account email
- **API token**: Paste the token from Step 2

**Step 4: Verify setup**

```bash
confluence spaces
```

If you see your spaces listed, you're ready to use Confluence.

---

## Focus

### Search Pages

```bash
confluence search "deployment guide"
```

### Read Page

```bash
confluence read <page-id>
```

Page IDs are in the URL: `https://yoursite.atlassian.net/wiki/spaces/SPACE/pages/123456/Title` → ID is `123456`

### Get Page Info

```bash
confluence info <page-id>
```

### Find Page by Title

```bash
confluence find "Page Title"
```

### List Spaces

```bash
confluence spaces
```

### Create Page

```bash
confluence create "Page Title" SPACEKEY --content "Page content here"
```

### Create Child Page

```bash
confluence create-child "Child Page Title" <parent-page-id> --content "Content"
```

Or from a file:

```bash
confluence create-child "Page Title" <parent-id> --file content.html --format storage
```

### Update Page

```bash
confluence update <page-id> --content "Updated content"
```

Or from a file:

```bash
confluence update <page-id> --file content.html --format storage
```

### List Child Pages

```bash
confluence children <page-id>
```

### Export Page with Attachments

```bash
confluence export <page-id> --output ./exported-page/
```

### Tips

- Domain in config should NOT include `https://` - just `yourcompany.atlassian.net`
- Use `--format storage` when content is in Confluence storage format (HTML-like)
- Page IDs are numeric and found in page URLs
- New installations use the platform configuration directory; existing `~/.confluence-cli/` installations remain supported.

## Quality checks

Confirm the active site, account and exact target before execution. Distinguish CLI availability from successful authentication and access. After an authorized write, read back the exact page or issue and verify requested fields, hierarchy or state. Report failures and checks not run; do not infer success from a submitted command.

## Return

Return the requested Confluence content or action result with actual page or issue identifiers, source links when available, verification and limitations. For local exports, report the authorized output path and observed files. Never return API tokens.

## Boundaries

Read access and this skill do not authorize writes, installation or reconfiguration. Confirm the exact site, target and final payload before creating or updating content; for Jira also confirm assignment, transition and comment operations. Preview bulk changes. Export only to an authorized location and minimize confidential data. Stop on ambiguous targets, missing permissions or uncertain write results; reconcile before retrying.
