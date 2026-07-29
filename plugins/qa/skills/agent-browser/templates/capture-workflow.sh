#!/usr/bin/env bash
# Template: Capture text, structure, screenshot, and PDF from one authorized URL.
# Usage: ./capture-workflow.sh <url> <allowed-domains> [output-dir]
#
# Outputs:
#   page-full.png
#   page-structure.txt
#   page-text.txt
#   page.pdf

set -euo pipefail

target_url="${1:?Usage: $0 <url> <allowed-domains> [output-dir]}"
allowed_domains="${2:?Usage: $0 <url> <allowed-domains> [output-dir]}"
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
session_name="$(agent-browser session id --scope worktree --prefix capture)"
cleanup() {
    agent-browser --session "$session_name" close >/dev/null 2>&1 || true
}
trap cleanup EXIT

agent-browser --session "$session_name" \
    --allowed-domains "$allowed_domains" \
    --content-boundaries \
    --max-output 20000 \
    open "$target_url"
agent-browser --session "$session_name" wait --load networkidle

agent-browser --session "$session_name" screenshot --full "$output_dir/page-full.png"
agent-browser --session "$session_name" snapshot -i > "$output_dir/page-structure.txt"
agent-browser --session "$session_name" get text body > "$output_dir/page-text.txt"
agent-browser --session "$session_name" pdf "$output_dir/page.pdf"

printf '%s\n' \
    "$output_dir/page-full.png" \
    "$output_dir/page-structure.txt" \
    "$output_dir/page-text.txt" \
    "$output_dir/page.pdf"
