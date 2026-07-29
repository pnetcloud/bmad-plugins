#!/bin/bash
# Template: Authenticated Session Workflow
# Purpose: Login once, save state, reuse for subsequent runs
# Usage: ./authenticated-session.sh <login-url> [state-file]
#
# RECOMMENDED: Use the auth vault instead of this template:
#   echo "<pass>" | agent-browser auth save myapp --url <login-url> --username <user> --password-stdin
#   agent-browser auth login myapp
# The auth vault stores credentials securely and the LLM never sees passwords.
#
# Environment variables:
#   TEST_USERNAME - Login username/email
#   TEST_PASSWORD - Login password
#
# Two modes:
#   1. Discovery mode (default): Shows form structure so you can identify refs
#   2. Login mode: Performs actual login after you update the refs
#
# Setup steps:
#   1. Run once to see form structure (discovery mode)
#   2. Update refs in LOGIN FLOW section below
#   3. Set TEST_USERNAME and TEST_PASSWORD
#   4. Delete the DISCOVERY section

set -euo pipefail

login_url="${1:?Usage: $0 <login-url> [state-file]}"
state_file="${2:-./auth-state.json}"

echo "Authentication workflow: $login_url"

# ================================================================
# SAVED STATE: Skip login if valid saved state exists
# ================================================================
if [[ -f "$state_file" ]]; then
    echo "Loading saved state from $state_file..."
    if agent-browser --state "$state_file" open "$login_url" 2>/dev/null; then
        agent-browser wait --load networkidle

        current_url=$(agent-browser get url)
        if [[ "$current_url" != *"login"* ]] && [[ "$current_url" != *"signin"* ]]; then
            echo "Session restored successfully"
            agent-browser snapshot -i
            exit 0
        fi
        echo "Session expired, performing fresh login..."
        agent-browser close 2>/dev/null || true
    else
        echo "Failed to load state, re-authenticating..."
    fi
    rm -f "$state_file"
fi

# ================================================================
# DISCOVERY MODE: Shows form structure (delete after setup)
# ================================================================
echo "Opening login page..."
agent-browser open "$login_url"
agent-browser wait --load networkidle

echo ""
echo "Login form structure:"
echo "---"
agent-browser snapshot -i
echo "---"
echo ""
echo "Next steps:"
echo "  1. Note the refs: username=@e?, password=@e?, submit=@e?"
echo "  2. Update the LOGIN FLOW section below with your refs"
echo "  3. Set: export TEST_USERNAME='...' TEST_PASSWORD='...'"
echo "  4. Delete this DISCOVERY MODE section"
echo ""
agent-browser close
exit 0

# ================================================================
# LOGIN FLOW: Uncomment and customize after discovery
# ================================================================
# : "${TEST_USERNAME:?Set TEST_USERNAME environment variable}"
# : "${TEST_PASSWORD:?Set TEST_PASSWORD environment variable}"
#
# agent-browser open "$login_url"
# agent-browser wait --load networkidle
# agent-browser snapshot -i
#
# # Fill credentials (update refs to match your form)
# agent-browser fill @e1 "$TEST_USERNAME"
# agent-browser fill @e2 "$TEST_PASSWORD"
# agent-browser click @e3
# agent-browser wait --load networkidle
#
# # Verify login succeeded
# final_url=$(agent-browser get url)
# if [[ "$final_url" == *"login"* ]] || [[ "$final_url" == *"signin"* ]]; then
#     echo "Login failed - still on login page"
#     agent-browser screenshot /tmp/login-failed.png
#     agent-browser close
#     exit 1
# fi
#
# # Save state for future runs
# echo "Saving state to $state_file"
# agent-browser state save "$state_file"
# echo "Login successful"
# agent-browser snapshot -i
