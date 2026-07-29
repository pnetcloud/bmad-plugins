# Video Recording

Capture browser automation as video for debugging, documentation, or verification.

Recording can capture credentials, personal data, private messages, and people.
Require explicit authorization for the page, account, duration, output path,
retention, and audience. Pause or stop before protected input.

**Related**: [commands.md](commands.md) for full command reference, [SKILL.md](../SKILL.md) for quick start.

## Contents

- [Basic Recording](#basic-recording)
- [Recording Commands](#recording-commands)
- [Use Cases](#use-cases)
- [Best Practices](#best-practices)
- [Output Format](#output-format)
- [Limitations](#limitations)

## Basic Recording

```bash
# Start recording
agent-browser record start ./demo.webm

# Perform actions
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser click @e1
agent-browser fill @e2 "test input"

# Stop and save
agent-browser record stop
```

## Recording Commands

```bash
# Start recording to file
agent-browser record start ./output.webm

# Stop current recording
agent-browser record stop

# Restart with new file (stops current + starts new)
agent-browser record restart ./take2.webm
```

## Use Cases

### Debugging Failed Automation

```bash
#!/bin/bash
# Record automation for debugging

agent-browser record start ./debug-$(date +%Y%m%d-%H%M%S).webm

# Run your automation
agent-browser open https://app.example.com
agent-browser snapshot -i
agent-browser click @e1 || {
    echo "Click failed - check recording"
    agent-browser record stop
    exit 1
}

agent-browser record stop
```

### Documentation Generation

```bash
#!/bin/bash
# Record a synthetic, non-authenticated workflow for documentation

agent-browser record start ./docs/navigation-example.webm

agent-browser open https://example.com
agent-browser wait 1000  # Pause for visibility

agent-browser snapshot -i
agent-browser click @e1
agent-browser wait --load networkidle
agent-browser wait 1000  # Show result

agent-browser record stop
```

### CI/CD Test Evidence

```bash
#!/bin/bash
# Record E2E test runs for CI artifacts

test_name="${1:-e2e-test}"
recording_dir="./test-recordings"
mkdir -p "$recording_dir"

agent-browser record start "$recording_dir/$test_name-$(date +%s).webm"

# Run test
if run_e2e_test; then
    echo "Test passed"
else
    echo "Test failed - recording saved"
fi

agent-browser record stop
```

## Best Practices

### 1. Add Pauses for Clarity

```bash
# Slow down for human viewing
agent-browser click @e1
agent-browser wait 500  # Let viewer see result
```

Use bounded waits for presentation only after the underlying state has been
verified with a specific condition. A pause is not proof that the page is ready.

### 2. Use Descriptive Filenames

```bash
# Include context in filename
agent-browser record start ./recordings/navigation-flow.webm
agent-browser record start ./recordings/synthetic-checkout.webm
```

### 3. Handle Recording in Error Cases

```bash
#!/bin/bash
set -e

cleanup() {
    agent-browser record stop 2>/dev/null || true
    agent-browser close 2>/dev/null || true
}
trap cleanup EXIT

agent-browser record start ./automation.webm
# ... automation steps ...
```

The cleanup handler must stop only the recording and session owned by this task.
Do not hide a failed stop or claim that an incomplete recording was saved.

### 4. Combine with Screenshots

```bash
# Record video AND capture key frames
agent-browser record start ./flow.webm

agent-browser open https://example.com
agent-browser screenshot ./screenshots/step1-homepage.png

agent-browser click @e1
agent-browser screenshot ./screenshots/step2-after-click.png

agent-browser record stop
```

## Output Format

- Common output is WebM; confirm codec and compatibility in the installed
  version before promising a consumer-specific format.
- Treat every recording as potentially sensitive until reviewed and redacted.

## Limitations

- Recording adds slight overhead to automation
- Large recordings can consume significant disk space
- Some headless environments may have codec limitations
- Recording may capture transient protected content that is absent from the
  final screenshot or page state.
