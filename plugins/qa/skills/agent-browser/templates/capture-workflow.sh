#!/bin/bash
# Template: Content Capture Workflow
# Purpose: Extract content from web pages (text, screenshots, PDF)
# Usage: ./capture-workflow.sh <url> [output-dir]
#
# Outputs:
#   - page-full.png: Full page screenshot
#   - page-structure.txt: Page element structure with refs
#   - page-text.txt: All text content
#   - page.pdf: PDF version
#
# Optional: Load auth state for protected pages

set -euo pipefail

target_url="${1:?Usage: $0 <url> [output-dir]}"
output_dir="${2:-.}"

echo "Capturing: $target_url"
mkdir -p "$output_dir"

# Optional: Load authentication state
# if [[ -f "./auth-state.json" ]]; then
#     echo "Loading authentication state..."
#     agent-browser state load "./auth-state.json"
# fi

# Navigate to target
agent-browser open "$target_url"
agent-browser wait --load networkidle

# Get metadata
title=$(agent-browser get title)
current_url=$(agent-browser get url)
echo "Title: $title"
echo "URL: $current_url"

# Capture full page screenshot
agent-browser screenshot --full "$output_dir/page-full.png"
echo "Saved: $output_dir/page-full.png"

# Get page structure with refs
agent-browser snapshot -i > "$output_dir/page-structure.txt"
echo "Saved: $output_dir/page-structure.txt"

# Extract all text content
agent-browser get text body > "$output_dir/page-text.txt"
echo "Saved: $output_dir/page-text.txt"

# Save as PDF
agent-browser pdf "$output_dir/page.pdf"
echo "Saved: $output_dir/page.pdf"

# Optional: Extract specific elements using refs from structure
# agent-browser get text @e5 > "$output_dir/main-content.txt"

# Optional: Handle infinite scroll pages
# for i in {1..5}; do
#     agent-browser scroll down 1000
#     agent-browser wait 1000
# done
# agent-browser screenshot --full "$output_dir/page-scrolled.png"

# Cleanup
agent-browser close

echo ""
echo "Capture complete:"
ls -la "$output_dir"
