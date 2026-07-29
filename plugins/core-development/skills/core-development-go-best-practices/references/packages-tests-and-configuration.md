# Packages, Tests, and Configuration

Use this reference for module/package layout, file organization, test depth, and
typed configuration.

## Contents

- [Module and Package Structure](#module-and-package-structure)
- [Files and API Surface](#files-and-api-surface)
- [Tests and Tooling](#tests-and-tooling)
- [Typed Configuration](#typed-configuration)
- [Configuration Source Boundary](#configuration-source-boundary)

## Module and Package Structure

Inspect `go.mod`, `go.work`, toolchain directives, repository layout, import
graph, and existing commands before adding packages.

- Keep packages cohesive around a responsibility and name them for what callers
  use, not generic buckets such as `util`, `common`, or `types`.
- Use `internal/` when the module intentionally prevents external imports.
- Keep commands in the repository's established command layout.
- Avoid import cycles and packages created only to hold one interface or mock.
- Preserve generated-code and public-module boundaries.

Package boundaries define APIs; file boundaries are an internal organization
choice.

## Files and API Surface

Split files when it improves navigation, build-tag separation, generated/manual
separation, or conceptual cohesion. There is no universal 300-line limit or
one-type-per-file rule. Do not produce many tiny files that fragment one
operation, and do not keep unrelated concerns together solely to reduce file
count.

Keep `_test.go` files near the package they test. Choose same-package versus
external-package tests according to whether the test needs internals or should
exercise only the public API.

Export only the API consumers need. Add Go doc comments for exported
declarations and meaningful package documentation according to repository
rules.

## Tests and Tooling

Add focused tests for changed behavior. Table-driven tests are useful when cases
share one setup and assertion shape:

```go
func TestParseStatus(t *testing.T) {
	tests := []struct {
		name    string
		input   string
		want    Status
		wantErr bool
	}{
		{name: "active", input: "active", want: StatusActive},
		{name: "empty", input: "", wantErr: true},
		{name: "unknown", input: "other", wantErr: true},
	}

	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			got, err := ParseStatus(test.input)
			if (err != nil) != test.wantErr {
				t.Fatalf("ParseStatus(%q) error = %v, wantErr %v", test.input, err, test.wantErr)
			}
			if got != test.want {
				t.Errorf("ParseStatus(%q) = %v, want %v", test.input, got, test.want)
			}
		})
	}
}
```

Also consider, when applicable:

- examples for exported package usage;
- fuzz targets for parsers, decoders, and boundary-heavy invariants;
- race-enabled tests for exercised concurrent behavior;
- `go vet` and repository linters;
- the repository's approved vulnerability scanner;
- cross-version or cross-platform tests promised by the public module.

Fuzzing and race checks can be expensive; vulnerability checks may download
data; tests may execute initialization and integration dependencies. Inspect
scope and authority rather than running every tool by default.

## Typed Configuration

Centralize parsing and validation so business code receives typed values rather
than repeatedly looking up strings:

```go
type RawConfig struct {
	ListenPort        string
	DatabaseReference string
	ProtectedValueRef string
	Environment       string
}

type Config struct {
	ListenPort        uint16
	DatabaseReference string
	ProtectedValueRef string
	Environment       string
}

func ParseConfig(raw RawConfig) (Config, error) {
	port, err := strconv.ParseUint(raw.ListenPort, 10, 16)
	if err != nil || port == 0 {
		return Config{}, fmt.Errorf("parse listen port %q", raw.ListenPort)
	}
	if strings.TrimSpace(raw.DatabaseReference) == "" {
		return Config{}, errors.New("database reference is empty")
	}
	if strings.TrimSpace(raw.ProtectedValueRef) == "" {
		return Config{}, errors.New("protected value reference is empty")
	}
	environment := raw.Environment
	if environment == "" {
		environment = "development"
	}
	return Config{
		ListenPort:        uint16(port),
		DatabaseReference: raw.DatabaseReference,
		ProtectedValueRef: raw.ProtectedValueRef,
		Environment:       environment,
	}, nil
}
```

The example carries references to protected material, not the material itself.
Adapt fields and defaults to the application's actual configuration contract.
Production defaults must not silently weaken authentication, authorization,
transport, or data protection.

## Configuration Source Boundary

The process boundary may populate `RawConfig` from environment variables,
flags, a file, a protected-settings provider, or another approved source. Keep
concrete source keys and private topology in the application, not in this public
skill.

- Inspect configuration names and schemas without printing current values.
- Distinguish absence from an intentionally empty value.
- Validate required and cross-field constraints before serving traffic.
- Return actionable errors that name the invalid field but not its protected
  value.
- Avoid scattered direct lookups in business packages.
- Do not invent development defaults for protected production settings.

Tests should cover missing, empty, malformed, boundary, defaulted, and
conflicting inputs without using real protected values or infrastructure
endpoints.
