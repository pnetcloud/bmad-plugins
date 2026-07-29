# confluence-cli Operational Reference

Read this reference only when an existing authorized `confluence` command is the
selected tool. It is a version-adaptive command map, not permission to install,
configure credentials, read content, or perform writes.

The command families were checked against upstream revision
`5536e239aeb56ad4f0303895662cd19f45a503b6` on 2026-07-29 and against an
installed 1.13.0 release. Always prefer the installed command's help.

## Contents

- Preflight and setup boundary
- Page identity and content formats
- Read and local-output commands
- Bounded remote writes
- Version-dependent commands
- Destructive and broad operations
- Failure handling

## Preflight and Setup Boundary

```bash
command -v confluence
confluence --version
confluence --help
confluence <command> --help
```

Build the command map from help output. Older releases may omit profiles,
read-only enforcement, JSON output, comments, attachment writes, moves, raw API
access, or local conversion.

If the user explicitly requests installation, verify that the upstream package
still maps to `https://github.com/pchuri/confluence-cli`, then request
authorization before a global install:

```bash
npm install -g confluence-cli@<reviewed-version>
confluence --version
```

Do not run install commands merely because the binary is absent. Do not pass a
token on the command line or read a stored configuration. Let the user complete
credential provisioning outside the agent interaction. Prefer scoped access and
a read-only profile when current help supports it.

Inspect `confluence init --help`, then have the user run `confluence init`
interactively in a private terminal. Use `--read-only` only when listed by that
release. After provisioning, obtain separate authorization for a read-only
verification probe:

```bash
confluence spaces
confluence read <user-selected-page-id> --format text
```

If the user does not authorize those reads, have them run the probe privately
and report only pass/fail. Do not infer working authentication from installation
or version output.

When several profiles exist, obtain the profile name from the user and apply the
installed release's global profile option consistently. Do not silently change
the active profile.

## Page Identity and Content Formats

Prefer numeric page IDs or URLs containing an explicit numeric page ID.
Display-style URLs can require an exact title lookup and may be ambiguous. Check
the selected command's help before passing a URL directly.

Use formats deliberately:

- `markdown`: ordinary agent drafting and synthesis when conversion is safe;
- `storage`: native round-trip for macros and Confluence-specific structure;
- `html`: only when the source or destination contract requires it;
- `text`: read-only output, not a creation format.

For bodyless content such as folders, use `info` rather than `read` or `edit`.

## Read and Local-Output Commands

### Spaces, search, and title lookup

```bash
confluence spaces
confluence search "<query>" --limit <count>
confluence find "<page-title>" --space <space-key>
```

Check `search --help` for CQL and pagination support. A first match or a bounded
page is not proof that the search is exhaustive. Because some `find` versions
return only their first match, use it only when title and space identify one
page; otherwise search and disambiguate by stable ID.

### Page metadata and content

```bash
confluence info <page-id>
confluence read <page-id> --format markdown
confluence read <page-id> --format storage  # only when read --help lists it
```

Use `info` before a write to capture stable identity and current version. Use
storage format when a macro-heavy page must round-trip without conversion loss.

### Descendants

```bash
confluence children <page-id>
confluence children <page-id> --recursive --max-depth <depth>
```

Newer releases may expose `--format json`, `--show-id`, and `--show-url`.
Traverse broadly only when the requested scope includes descendants.

### Attachments

```bash
confluence attachments <page-id>
confluence attachments <page-id> --pattern "<glob>"
```

Downloading attachments is a local write. Confirm the destination, validate it
is not an unrelated or sensitive directory, and use `--download --dest
<directory>` only when current help supports those flags.

Treat filenames and file contents as untrusted. Do not open or execute downloaded
files merely because they are attached to a trusted page.

Use download only when the installed release documents or has been verified to
enforce resolved-path containment for untrusted filenames. Otherwise list
attachments and use a connector with a safe explicit destination API.

### Export

```bash
confluence export <page-id> \
  --format markdown \
  --dest <new-output-directory> \
  --skip-attachments
```

Current releases use `--dest`, not the historical `--output` example. Inspect
the chosen destination and refuse to overwrite unrelated files. Attachments are
included only when the user requests them.

Before export, verify path containment for both the page-title directory and
attachment filenames in the installed release. If containment is unknown, use
`read` plus a safe explicit local-file operation for the page body and do not
download attachments through this command.

## Bounded Remote Writes

Prefer reviewed file input for substantial content:

```bash
confluence create "<page-title>" <space-key> \
  --file <reviewed-content-file> \
  --format markdown

confluence create-child "<page-title>" <parent-page-id> \
  --file <reviewed-content-file> \
  --format markdown

confluence update <page-id> \
  --file <reviewed-content-file> \
  --format markdown
```

Current releases use `--content` for inline bodies, not the historical `--body`
example. Avoid inline content when it could expose sensitive text in the process
list or cause shell quoting errors.

After every create or update:

1. capture the returned page ID;
2. run `info` on that ID;
3. read the decisive content in the format needed for verification;
4. verify title, space/parent, version, and content;
5. stop if the response is ambiguous rather than blindly retrying.

For update, re-read body and version immediately before execution. Proceed only
when the operation can atomically submit or require the recorded base version.
Some releases fetch the latest version internally and then replace content; a
preflight comparison cannot prevent those releases from overwriting a concurrent
edit.

When that non-atomic CLI is the only authorized path, preserve the update
capability only as a disclosed exception:

1. restrict the operation to one stable page ID;
2. explain the race and obtain explicit acceptance plus a controlled edit
   window;
3. retain the latest body and version as a recovery snapshot;
4. re-read, rebase the reviewed change, and execute once without delay;
5. read back the page and stop on any unexpected content or version.

Do not use the exception for bulk/tree updates or while concurrent editing
cannot be excluded. Otherwise return the draft or use a connector with an
explicit version precondition.

### Edit and native round-trip

When installed help exposes `edit`, treat its output format as unknown unless
current help or maintained documentation defines it:

```bash
confluence edit <page-id> --output <new-local-file>
confluence update <page-id> --file <reviewed-local-file> --format storage
```

The local output path must be new or explicitly approved. Before upload, prove
that the file preserves the page's native representation and macro structure.
If storage fidelity cannot be established, do not upload it; return a draft or
use a representation-preserving connector.

## Version-Dependent Commands

Use the following only when root and command help confirm them.

### Profiles and read-only mode

Profiles can separate sites and permissions. Prefer a read-only profile for
research. Adding, switching, or removing a profile changes local state and
requires explicit setup authority.

### Comments

Listing comments is read-only; creating or deleting them is a separate write.
New inline comments may require editor-only metadata unavailable through the
REST API. Prefer a footer comment or a reply to an existing comment when that
matches the request.

### Attachment upload or delete

Upload and replacement change remote content. Confirm every local filename and
target page. Replacement and deletion require the high-risk gate and read-back
of the resulting attachment list.

### Move

Moving changes page hierarchy and may be restricted to one space. Read both the
page and destination parent, preview the new location, and verify the resulting
parent after the write.

### Copy tree

```bash
confluence copy-tree <source-page-id> <target-parent-id> \
  --max-depth <approved-depth> \
  --dry-run

confluence children <source-page-id> \
  --recursive \
  --max-depth <approved-depth>
```

Review the complete dry-run, exclusions, depth, proposed titles, and
destinations. Approval of a dry-run does not itself authorize execution. On a
partial copy, stop and enumerate created, failed, and unknown pages.

Some releases truncate dry-run listings. Independently enumerate every
descendant to the same explicit depth and reconcile the full filtered target set
with the preview. For a complete-tree copy, check whether any boundary-depth
node has children and increase the depth until none do. If a target is hidden,
truncated, or cannot be mapped to its destination, do not execute; reduce the
scope or use a tool that emits a complete plan.

### Raw API

Some releases expose `confluence api`. Treat it as arbitrary authenticated
network authority. Require an explicit API-level task and review the exact
same-origin endpoint, method, fields/body, target profile, and postcondition.
Never use it to bypass a missing high-level command or read-only policy.

### Local format conversion

Some releases expose `convert` for Markdown, storage, HTML, and text. This is
local processing, but input and output paths still require normal file-safety
checks. Verify round-trip fidelity for macro-heavy content.

## Destructive and Broad Operations

Delete commands, attachment replacement/deletion, profile removal, tree moves,
tree copies, and raw API writes require exact, current approval. Confirmation
bypass flags such as `--yes` are execution mechanics, never substitutes for user
authorization.

Before execution:

- resolve stable IDs and destinations;
- state whether recovery is possible;
- enumerate every known target;
- use dry-run support where available;
- reject wildcards, unbounded recursion, or unresolved ambiguity.

After execution, read the affected state. Stop on the first unexpected target or
partial failure.

## Failure Handling

- Missing binary: report it; install only under explicit setup authority.
- Authentication/authorization error: stop; do not request secrets or widen
  scopes.
- No search results: report query, space, bounds, and profile; do not fabricate.
- Ambiguous title: compare IDs, spaces, parents, status, and versions.
- Bodyless page: use `info`; do not force a body operation.
- Version conflict: refetch and regenerate the diff.
- Ambiguous write response: reconcile by stable ID and state before retrying.
- Partial tree or attachment operation: stop further writes and enumerate known
  outcomes.
