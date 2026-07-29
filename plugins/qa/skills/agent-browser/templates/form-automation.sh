#!/usr/bin/env bash
# Template: Discover and verify an authorized form without submitting it.
# Usage: ./form-automation.sh <form-url> <allowed-domains> [output-dir]
#
# Adapt a reviewed copy only after current refs and exact field values are known.
# Form submission, upload, account change, or purchase needs separate authority.

set -euo pipefail

form_url="${1:?Usage: $0 <form-url> <allowed-domains> [output-dir]}"
allowed_domains="${2:?Usage: $0 <form-url> <allowed-domains> [output-dir]}"
output_dir="${3:-./browser-artifacts}"

case "$output_dir" in
    ""|"."|".."|"/"|/*|"../"*|*/"../"*|*/"..")
        printf '%s\n' "output directory must be a task-owned relative path" >&2
        exit 2
        ;;
esac

reject_symlink_ancestors() {
    local path="$1"
    local current=""
    local part
    local remaining="${path#./}"

    while [[ -n "$remaining" ]]; do
        if [[ "$remaining" == */* ]]; then
            part="${remaining%%/*}"
            remaining="${remaining#*/}"
        else
            part="$remaining"
            remaining=""
        fi
        [[ -z "$part" || "$part" == "." ]] && continue
        current="${current:+$current/}$part"
        if [[ -L "$current" ]]; then
            printf '%s\n' "output path must not contain a symlink" >&2
            exit 2
        fi
    done
}

reject_symlink_ancestors "$output_dir"

if ! command -v agent-browser >/dev/null 2>&1; then
    printf '%s\n' "agent-browser is required but was not found" >&2
    exit 2
fi

mkdir -p -- "$output_dir"
session_name="$(agent-browser session id --scope worktree --prefix form-review)"
cleanup() {
    agent-browser --session "$session_name" close >/dev/null 2>&1 || true
}
trap cleanup EXIT

agent-browser --session "$session_name" \
    --allowed-domains "$allowed_domains" \
    --content-boundaries \
    open "$form_url"
agent-browser --session "$session_name" wait --load networkidle
agent-browser --session "$session_name" snapshot -i \
    > "$output_dir/form-structure.txt"

# Example shapes for an adapted copy; values remain synthetic.
# agent-browser --session "$session_name" fill @e1 "SYNTHETIC_NAME"
# agent-browser --session "$session_name" fill @e2 "SYNTHETIC_ACCOUNT"
# agent-browser --session "$session_name" select @e3 "SYNTHETIC_OPTION"
# agent-browser --session "$session_name" check @e4
#
# Re-snapshot and obtain confirmation before a submit action:
# agent-browser --session "$session_name" snapshot -i
# agent-browser --session "$session_name" click @e5
# agent-browser --session "$session_name" wait --url "**/success"

agent-browser --session "$session_name" screenshot "$output_dir/form-review.png"
agent-browser --session "$session_name" get url
printf '%s\n' "$output_dir/form-structure.txt" "$output_dir/form-review.png"
