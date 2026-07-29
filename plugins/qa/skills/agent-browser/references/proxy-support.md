# Proxy Support

Proxy configuration for authorized network-path, localization, failover, and
controlled-environment testing. Never use a proxy to evade access controls,
rate limits, bans, attribution, or policy.

**Related**: [commands.md](commands.md) for global options, [SKILL.md](../SKILL.md) for quick start.

## Contents

- [Basic Proxy Configuration](#basic-proxy-configuration)
- [Authenticated Proxy](#authenticated-proxy)
- [SOCKS Proxy](#socks-proxy)
- [Proxy Bypass](#proxy-bypass)
- [Common Use Cases](#common-use-cases)
- [Verifying Proxy Connection](#verifying-proxy-connection)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Basic Proxy Configuration

Prefer the explicit `--proxy` flag so routing is visible in the reviewed
command:

```bash
agent-browser --proxy "http://proxy.example.com:8080" open https://example.com
```

The installed version may also honor `HTTP_PROXY` and `HTTPS_PROXY`. Set them
only in a task-scoped process through approved runtime configuration; do not
persist or print them. Confirm whether they affect browser traffic, provider
traffic, or both.

## Authenticated Proxy

Credential-bearing proxy URLs expose secrets in shell history, process
inspection, logs, and error output. The current CLI accepts the complete URL
through `--proxy`; keep the value in a task-scoped lowercase variable populated
by an approved runtime injector:

```bash
agent-browser --proxy "$proxy_url" open https://example.com
```

For runtimes that document proxy environment support, `HTTP_PROXY`,
`HTTPS_PROXY`, or `ALL_PROXY` can instead be injected into only the owned
browser process. Do not print, persist, or interpolate the value into generated
shell source. If neither route meets the execution environment's disclosure
policy, stop rather than embedding credentials.

## SOCKS Proxy

```bash
# SOCKS5 proxy
agent-browser --proxy "socks5://proxy.example.com:1080" open https://example.com
```

`ALL_PROXY` may be supported by the installed runtime. Treat authenticated SOCKS
configuration with the same secret-input boundary as HTTP proxies.

## Proxy Bypass

Skip the proxy for an explicit reviewed set using `--proxy-bypass`:

```bash
# Via CLI flag
agent-browser --proxy "http://proxy.example.com:8080" \
  --proxy-bypass "localhost,127.0.0.1,*.service.example" \
  open https://service.example
```

`NO_PROXY` is process-wide and easy to over-broaden. Use it only through
approved task configuration and verify every bypass destination.

## Common Use Cases

### Geo-Location Testing

```bash
# Use separately authorized endpoints and explicit session names.
agent-browser --session region-a --proxy "http://region-a.proxy.example:8080" \
  open https://example.com
agent-browser --session region-a screenshot "./screenshots/region-a.png"
agent-browser --session region-a close

agent-browser --session region-b --proxy "http://region-b.proxy.example:8080" \
  open https://example.com
agent-browser --session region-b screenshot "./screenshots/region-b.png"
agent-browser --session region-b close
```

Verify that the site permits automated regional testing and that recorded
location or IP data follows the artifact-retention policy.

### Proxy Failover Testing

Test one approved route at a time, record the expected failure mode, close its
session, and move to the next only when the test plan authorizes it. Bound
attempts and request volume. Do not rotate identities or routes to continue
after a denial, quota, CAPTCHA, ban, or rate-limit response.

### Corporate Network Access

Use only the organization-provided endpoint and bypass contract. Keep internal
hostnames and proxy credentials out of public examples and logs:

```bash
agent-browser --proxy "http://gateway.proxy.example:8080" \
  --proxy-bypass "localhost,127.0.0.1,*.service.example" \
  open https://service.example
```

## Verifying Proxy Connection

Use a user-approved diagnostic endpoint that returns only the minimum routing
evidence. Do not send traffic to an arbitrary public IP service or publish the
observed address. Compare the result with the expected route, then close the
session.

## Troubleshooting

### Proxy Connection Failed

Confirm the endpoint, scheme, DNS path, and approved credential injection with
the proxy owner. Test through a synthetic or owned destination before touching
the target application. Never add credentials to a diagnostic command.

### SSL/TLS Errors Through Proxy

Some authorized proxies perform TLS inspection. Install and verify the approved
trust chain through the environment owner. Use `--ignore-https-errors` only in
an explicitly disposable test environment after the certificate failure is
understood; never use it to bypass an unexpected identity error.

### Slow Performance

Measure an owned test path and narrow proxy scope only with the network owner's
approval. A broad bypass can leak traffic outside the intended control.

## Best Practices

1. Prefer an explicit, credential-free `--proxy` endpoint in reviewed commands.
2. Inject authenticated configuration through an approved secret channel.
3. Keep bypass lists narrow and verify direct destinations.
4. Test connectivity against an owned or approved endpoint before automation.
5. Bound retries and stop on denials, quotas, CAPTCHAs, or policy errors.
6. Record route evidence without exposing proxy credentials, internal hosts, or
   observed client addresses.
