# Authentication Patterns

Login flows, session persistence, OAuth, 2FA, and authenticated browsing.

**Related**: [session-management.md](session-management.md) for state persistence details, [SKILL.md](../SKILL.md) for quick start.

## Contents

- [Import Auth from Your Browser](#import-auth-from-your-browser)
- [Persistent Profiles](#persistent-profiles)
- [Session Persistence](#session-persistence)
- [Basic Login Flow](#basic-login-flow)
- [Saving Authentication State](#saving-authentication-state)
- [Restoring Authentication](#restoring-authentication)
- [OAuth / SSO Flows](#oauth--sso-flows)
- [Two-Factor Authentication](#two-factor-authentication)
- [HTTP Basic Auth](#http-basic-auth)
- [Cookie-Based Auth](#cookie-based-auth)
- [Token Refresh Handling](#token-refresh-handling)
- [Security Best Practices](#security-best-practices)

## Import Auth from Your Browser

Importing cookies from an existing browser grants the automation the same
account authority as that browser. Use it only when the user explicitly
authorizes the exact profile, sites, state destination, and retention period.
Prefer a dedicated test profile; never attach to an unrelated personal browser.

**Step 1: Prepare an isolated browser**

Have the user start a dedicated browser profile with loopback-only remote
debugging according to the installed browser's current documentation, then
complete login themselves. Do not choose a profile or enable debugging without
authorization. A debugging endpoint permits cookie access and JavaScript
execution; keep it local, short-lived, and closed after capture.

**Step 2: Grab the auth state**

```bash
# Auto-discover the authorized browser and save its state to a task-owned path.
agent-browser --auto-connect state save .browser-state/imported.json
```

**Step 3: Reuse in automation**

```bash
# Load auth at launch
agent-browser --state .browser-state/imported.json open https://app.example/dashboard

# Or load into an existing session
agent-browser state load .browser-state/imported.json
agent-browser open https://app.example/dashboard
```

Verify the account identity and expected origin after loading. Imported state
may include more sites or authority than the target task; domain restrictions
remain required.

> **Security note:** State files can contain bearer-equivalent cookies and
> storage. Keep them outside version control with restricted permissions. If
> the installed version supports encryption, provide
> `AGENT_BROWSER_ENCRYPTION_KEY` through an approved secret manager rather than
> a command or transcript.

**Tip:** Combine with a scoped session and installed-version restore:

```bash
session_name="$(agent-browser session id --scope worktree --prefix imported)"
agent-browser --session "$session_name" --restore \
  --state .browser-state/imported.json open https://app.example
```

## Persistent Profiles

Use `--profile` only with a dedicated task-owned Chrome user-data directory.
Profiles persist cookies, IndexedDB, service workers, cache, history, and
possibly downloads across restarts:

```bash
# First run: login once
agent-browser --profile .browser-profile/role-a open https://app.example/login
# ... complete login flow ...

# All subsequent runs: already authenticated
agent-browser --profile .browser-profile/role-a open https://app.example/dashboard
```

Use different paths for different projects or test users:

```bash
agent-browser --profile .browser-profile/role-a open https://app.example
agent-browser --profile .browser-profile/role-b open https://app.example
```

Do not point `--profile` or `AGENT_BROWSER_PROFILE` at the user's everyday
browser profile. Keep profile ownership, permissions, and cleanup explicit.

## Session Persistence

Use the installed version's scoped session and restore mechanism to auto-save
and restore cookies and storage:

```bash
session_name="$(agent-browser session id --scope worktree --prefix account)"
agent-browser --session "$session_name" --restore open https://app.example
# ... login flow ...
agent-browser --session "$session_name" --restore close

# Next time: state is automatically restored
agent-browser --session "$session_name" --restore open https://app.example
```

Encrypt state at rest:

Provide `AGENT_BROWSER_ENCRYPTION_KEY` through the user's approved secret store
before starting the process. Never generate, print, or persist the key inside a
public template or task transcript.

## Basic Login Flow

Prefer an already provisioned auth-vault profile:

```bash
agent-browser auth list
agent-browser auth login AUTH_PROFILE
```

If no profile exists, do not ask the user to paste a password into chat or place
it in shell source. Have the user provision the vault through an approved
secret-input channel, or open a headed isolated session so they can complete
credentials themselves. Snapshot only after protected fields are no longer
exposed, then verify the account and destination.

## Saving Authentication State

After logging in, save state for reuse:

```bash
# After user-authorized login, verify destination and save to an owned path.
agent-browser get url
agent-browser state save .browser-state/auth.json
```

## Restoring Authentication

Skip login by loading saved state:

```bash
# Load saved auth state
agent-browser state load .browser-state/auth.json

# Navigate directly to protected page
agent-browser open https://app.example/dashboard

# Verify expected identity and page state without exposing protected content
agent-browser snapshot -i
```

## OAuth / SSO Flows

Do not automate identity-provider credentials, consent, or account selection
unless the user explicitly authorizes the exact action and an approved
credential channel exists. Prefer user completion in a headed isolated browser:

```bash
# Start OAuth flow
agent-browser --headed open https://app.example/auth/provider

# Let the user complete provider authentication and consent.
agent-browser wait --url "**/app.example/**" --timeout 120000
agent-browser snapshot -i

# Save only after verifying the returned account and requested scope.
agent-browser state save .browser-state/oauth.json
```

Stop on an unexpected provider, consent scope, tenant, or redirect domain.

## Two-Factor Authentication

Handle 2FA with manual intervention:

```bash
# Open a headed authorized session and let the user complete credentials and MFA.
agent-browser --headed open https://app.example/login
agent-browser wait --url "**/dashboard" --timeout 120000

# Verify identity, then save only if persistence was explicitly authorized.
agent-browser state save .browser-state/mfa.json
```

Never request, read, store, or solve a one-time code, push approval, CAPTCHA, or
hardware-key challenge on the user's behalf.

## HTTP Basic Auth

For sites using HTTP Basic Authentication:

The current lower-level command accepts positional values:

```bash
agent-browser set credentials "$basic_user" "$basic_password"
agent-browser open https://protected.example/resource
```

Confirm `agent-browser set credentials --help` for the installed version. The
documented command has no stdin secret flag, so both values may be visible in
process inspection. Populate the lowercase shell variables only through an
approved runtime secret injector, never with literals in chat or shell source,
and use this path only when the user accepts that residual exposure in the
execution environment. Otherwise use an approved wrapper or stop. Clear the
local variables after the browser has consumed them.

## Cookie-Based Auth

Manually set authentication cookies:

Inspect `agent-browser cookies set --help`, verify the target origin and cookie
scope, and obtain the value through an approved secret channel. Setting,
exporting, clearing, or displaying an authentication cookie is an account-level
mutation and requires explicit authorization.

## Token Refresh Handling

For sessions with expiring tokens, load only the authorized state and navigate
to a harmless account-identification page. If the browser is redirected to
login or the expected identity is absent, close the session and invoke the
approved vault or user-completed login path. Do not implement a hidden password
fallback or silently overwrite the previous state. Save replacement state only
after identity and scope verification.

## Security Best Practices

1. **Keep state and profiles outside version control.** Verify ignore behavior
   and permissions without editing unrelated repository files implicitly.
2. **Prefer the auth vault or user-completed login.** Never put credential
   literals in chat, shell source, logs, screenshots, or saved examples. If an
   installed command supports only positional secrets, disclose the process-
   argument risk and require an approved runtime injector and environment.
3. **Restrict authority.** Apply allowed domains and action policies, then
   verify account identity after every restore.
4. **Encrypt authorized persistent state.** Supply the documented encryption
   key through an approved secret manager and retain it separately.
5. **Clean up precisely.** Close owned sessions and remove only exact
   task-owned artifacts after confirming retention requirements. Clearing all
   cookies or deleting a profile is destructive and needs explicit authority.
6. **Use short-lived CI sessions.** Do not persist state unless the CI secret,
   artifact, and cleanup policies explicitly permit it.

## Primary References

- [agent-browser security documentation](https://agent-browser.dev/security)
- [agent-browser sessions documentation](https://agent-browser.dev/sessions)
