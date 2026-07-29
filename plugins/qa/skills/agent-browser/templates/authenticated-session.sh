#!/usr/bin/env bash
# Template: Reuse an explicitly authorized agent-browser state file.
# Usage: ./authenticated-session.sh <start-url> <allowed-domains> <state-file> <authenticated-url-pattern> <non-sensitive-marker-text>
#
# This template does not collect credentials, perform fresh login, save state,
# clear cookies, or delete an expired state file. Provision authentication
# through the installed CLI's approved vault or a user-completed headed flow.
# The marker is passed in process arguments: use only static public UI text that
# appears after authentication, never an account name, identifier, or secret.

set -euo pipefail

start_url="${1:?Usage: $0 <start-url> <allowed-domains> <state-file> <authenticated-url-pattern> <non-sensitive-marker-text>}"
allowed_domains="${2:?Usage: $0 <start-url> <allowed-domains> <state-file> <authenticated-url-pattern> <non-sensitive-marker-text>}"
state_file="${3:?Usage: $0 <start-url> <allowed-domains> <state-file> <authenticated-url-pattern> <non-sensitive-marker-text>}"
authenticated_url_pattern="${4:?Usage: $0 <start-url> <allowed-domains> <state-file> <authenticated-url-pattern> <non-sensitive-marker-text>}"
public_marker_text="${5:?Usage: $0 <start-url> <allowed-domains> <state-file> <authenticated-url-pattern> <non-sensitive-marker-text>}"

if [[ ! -f "$state_file" || -L "$state_file" ]]; then
    printf '%s\n' "state file must be an existing regular non-symlink file" >&2
    exit 2
fi

if ! command -v agent-browser >/dev/null 2>&1; then
    printf '%s\n' "agent-browser is required but was not found" >&2
    exit 2
fi

session_name="$(agent-browser session id --scope worktree --prefix auth-reuse)"
cleanup() {
    agent-browser --session "$session_name" close >/dev/null 2>&1 || true
}
trap cleanup EXIT

agent-browser --session "$session_name" \
    --allowed-domains "$allowed_domains" \
    --content-boundaries \
    --state "$state_file" \
    open "$start_url"
agent-browser --session "$session_name" wait --load networkidle
agent-browser --session "$session_name" \
    wait --url "$authenticated_url_pattern"
agent-browser --session "$session_name" \
    wait --text "$public_marker_text"

printf '%s\n' "authorized session state restored"
agent-browser --session "$session_name" get url
agent-browser --session "$session_name" get title
