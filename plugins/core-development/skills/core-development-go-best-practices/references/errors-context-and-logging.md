# Errors, Context, Concurrency, and Logging

Use this reference for failure contracts, cancellation, goroutine lifetime, and
structured logs.

## Contents

- [Errors](#errors)
- [Switch and Failure Paths](#switch-and-failure-paths)
- [Panic and Recovery](#panic-and-recovery)
- [Context and Timeouts](#context-and-timeouts)
- [Goroutine Lifetimes](#goroutine-lifetimes)
- [Structured Logging](#structured-logging)

## Errors

Handle relevant returned errors. Add concise operation context without
duplicating the same phrase at every layer:

```go
result, err := client.Do(ctx, request)
if err != nil {
	return nil, fmt.Errorf("fetch widget: %w", err)
}
return result, nil
```

Wrapping with `%w` makes the cause part of the caller-visible error contract.
Use it when callers should inspect the cause; otherwise format without exposing
an implementation detail. Match wrapped identities and types with
`errors.Is`/`errors.As`, not direct equality or string comparison.

Expected absence or a two-way result may use `(value, ok)` when no explanation
is needed. Do not require an error return from a function that cannot fail.

For intentionally incomplete behavior, fail explicitly:

```go
func buildWidget(kind string) (*Widget, error) {
	return nil, fmt.Errorf("build widget: unsupported kind %q", kind)
}
```

Avoid leaking protected authentication inputs, raw queries, or full payloads
into error strings.

## Switch and Failure Paths

For untrusted open input, a default error prevents silent fallthrough:

```go
func processStatus(status string) (string, error) {
	switch status {
	case "active":
		return "processing", nil
	case "inactive":
		return "skipped", nil
	default:
		return "", fmt.Errorf("unsupported status %q", status)
	}
}
```

For a closed enum-like type, an exhaustive analyzer may work better without a
default. A switch that intentionally ignores values should make that intent
clear. The rule is to account for behavior, not mechanically add `default`.

## Panic and Recovery

Do not use panic for ordinary invalid input or operational failure. Panic can be
appropriate for an impossible programmer invariant or during initialization
when continuing would violate the process contract. A panic unwinds the current
goroutine and terminates the program if no deferred recovery boundary handles
it.

Recover only at an intentional boundary that can restore a valid state, record
the failure safely, and produce the contractually correct result. Do not use
recover to hide corrupted state or continue blindly.

## Context and Timeouts

- Pass `context.Context` explicitly as the first parameter of request-scoped
  functions.
- Do not store a request context in a long-lived struct or replace it with a
  custom context interface.
- Propagate the caller's context through external calls.
- The layer that owns a deadline derives it and calls the returned cancel
  function. A lower layer should not silently shorten a caller's deadline
  unless its API contract owns that budget.
- Stop work promptly on cancellation where possible and preserve the operation's
  documented error identity.

```go
func FetchWidget(
	ctx context.Context,
	client *http.Client,
	request *http.Request,
	timeout time.Duration,
) (*http.Response, error) {
	requestCtx, cancel := context.WithTimeout(ctx, timeout)
	defer cancel()

	response, err := client.Do(request.WithContext(requestCtx))
	if err != nil {
		return nil, fmt.Errorf("fetch widget: %w", err)
	}
	return response, nil
}
```

Use this shape only when `FetchWidget` owns the timeout parameter. Otherwise
accept the caller's context without deriving another deadline. On a successful
return, the caller owns `response.Body` and must close it; state that ownership
in the helper contract. A helper that fully consumes the body should close it
internally instead.

## Goroutine Lifetimes

Every goroutine needs a documented termination path and ownership model:

- who starts it and waits for it;
- which context, channel, or condition stops it;
- who closes channels and resources;
- how errors and panics are surfaced;
- whether input memory may still be accessed concurrently.

Prefer confining mutable state to one goroutine or passing immutable snapshots.
When sharing is required, choose a mechanism that matches the invariant:

- a mutex for compound state that must change atomically;
- atomic operations for a supported single-variable state machine;
- channel transfer when ownership moves between goroutines.

Document the protected fields and happens-before relationship. A race-enabled
test must exercise the actual concurrent reads and writes with assertions; a
clean run over an unvisited path is not proof.

Prefer synchronous functions when callers can add concurrency themselves.
Test cancellation, blocked sends/receives, early returns, partial startup, and
graceful termination. Use race-enabled tests for exercised concurrent paths
when supported.

## Structured Logging

Prefer the project's injected `*slog.Logger` or logging abstraction over a new
package-global logger:

```go
type WidgetService struct {
	logger *slog.Logger
}

func (service *WidgetService) Create(
	ctx context.Context,
	name string,
) (*Widget, error) {
	service.logger.DebugContext(ctx, "creating widget")
	widget := &Widget{Name: name}
	service.logger.DebugContext(ctx, "created widget")
	return widget, nil
}
```

Use stable field names and the request context. Avoid logging raw protected
values, tokens, request bodies, personal data, or high-cardinality fields
without an explicit observability and privacy contract.
