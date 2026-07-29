# Types, Interfaces, Options, and Ownership

Use this reference when designing Go types, constructors, behavior boundaries,
receivers, or ownership. Adapt examples to the target package.

## Contents

- [Contract-First Type Design](#contract-first-type-design)
- [Named Domain Primitives](#named-domain-primitives)
- [Consumer-Owned Interfaces](#consumer-owned-interfaces)
- [Enum-Like Values](#enum-like-values)
- [Functional Options](#functional-options)
- [Embedding](#embedding)
- [Receivers and Ownership](#receivers-and-ownership)

## Contract-First Type Design

A useful type-first loop is:

1. describe observable behavior and invariants;
2. define the minimum data structures and function signatures that express it;
3. implement the behavior;
4. validate untrusted input at the boundary;
5. let tests and callers reveal whether another abstraction is needed.

```go
type UserID string

type User struct {
	ID        UserID
	Email     string
	Name      string
	CreatedAt time.Time
}

type CreateUserRequest struct {
	Email string
	Name  string
}

func CreateUser(req CreateUserRequest) (*User, error) {
	// Validate and implement the target package's contract.
	return nil, errors.New("not implemented")
}
```

This preserves the original structs-first workflow without requiring unused
types or interfaces before behavior is understood.

## Named Domain Primitives

Named types can prevent accidental assignment between distinct identifiers:

```go
type UserID string
type OrderID string

func GetUser(ctx context.Context, id UserID) (*User, error) {
	return nil, errors.New("not implemented")
}

func (id UserID) String() string {
	return string(id)
}
```

They do not by themselves guarantee valid runtime values: code can still
convert a string. When validation is important, centralize it:

```go
func ParseUserID(raw string) (UserID, error) {
	raw = strings.TrimSpace(raw)
	if raw == "" {
		return "", errors.New("user ID is empty")
	}
	return UserID(raw), nil
}
```

For stronger invariants, keep representation fields unexported behind a package
constructor. Balance that against serialization, zero-value, and API needs.

## Consumer-Owned Interfaces

Define what a consumer needs, not a mirror of everything an implementation has:

```go
type UserRepository interface {
	GetByID(ctx context.Context, id UserID) (*User, error)
	Save(ctx context.Context, user *User) error
}

func ProcessInput(r io.Reader) ([]byte, error) {
	return io.ReadAll(r)
}
```

Prefer a small interface in the consuming package after a real use appears.
Implementations normally return a concrete type so methods can grow without
changing consumer contracts:

```go
type Store struct {
	// ...
}

func NewStore(/* dependencies */) *Store {
	return &Store{}
}
```

Returning an interface is still appropriate when hiding the implementation is
part of the public API, as in several standard-library constructors. Record the
reason instead of applying either slogan mechanically.

## Enum-Like Values

Reserve the zero value deliberately and validate values crossing a boundary:

```go
type Status int

const (
	StatusUnknown Status = iota
	StatusActive
	StatusInactive
	StatusPending
)

func (s Status) String() string {
	switch s {
	case StatusActive:
		return "active"
	case StatusInactive:
		return "inactive"
	case StatusPending:
		return "pending"
	default:
		return fmt.Sprintf("Status(%d)", s)
	}
}

func ProcessStatus(s Status) (string, error) {
	switch s {
	case StatusActive:
		return "processing", nil
	case StatusInactive:
		return "skipped", nil
	case StatusPending:
		return "waiting", nil
	default:
		return "", fmt.Errorf("unsupported status %d", s)
	}
}
```

A defensive `default` is useful for untrusted or forward-compatible input. In a
closed internal switch, omitting it may allow an exhaustive-switch analyzer to
detect a newly added constant. Choose based on the boundary and toolchain.

## Functional Options

Use options when optional constructor configuration is expected to grow:

```go
type ServerOption func(*Server) error

func WithPort(port int) ServerOption {
	return func(server *Server) error {
		if port < 1 || port > 65_535 {
			return fmt.Errorf("port %d is outside the valid range", port)
		}
		server.port = port
		return nil
	}
}

func WithTimeout(timeout time.Duration) ServerOption {
	return func(server *Server) error {
		if timeout <= 0 {
			return fmt.Errorf("timeout must be positive")
		}
		server.timeout = timeout
		return nil
	}
}

func NewServer(options ...ServerOption) (*Server, error) {
	server := &Server{
		port:    8080,
		timeout: 30 * time.Second,
	}
	for index, option := range options {
		if option == nil {
			return nil, fmt.Errorf("server option %d is nil", index)
		}
		if err := option(server); err != nil {
			return nil, fmt.Errorf("apply server option %d: %w", index, err)
		}
	}
	return server, nil
}
```

For a few mandatory parameters, ordinary arguments are clearer. For a complete
declarative configuration, a validated config struct may be clearer.

## Embedding

Embedding can intentionally promote fields and methods:

```go
type Timestamps struct {
	CreatedAt time.Time
	UpdatedAt time.Time
}

type User struct {
	Timestamps
	ID    UserID
	Email string
}
```

Promotion changes the outer method set and public field surface. Use a named
field when callers should not treat the embedded value as part of the outer
type's identity or API.

## Receivers and Ownership

- Use a pointer receiver for mutation, large values, values containing a mutex
  or other no-copy state, or when receiver consistency requires it.
- A value receiver fits a small immutable value type with no problematic
  internal pointers.
- Do not mix pointer and value receivers casually across one type's method set.
- Passing a slice or map does not copy its backing storage. Mutate, clone, or
  document aliasing according to the API contract.
- Avoid package-level mutable state when explicit dependencies or scoped state
  make ownership clearer.
- Return a new value when that is the promised API; mutate in place when the
  operation and ownership contract make mutation clearer and cheaper.
- Closures and higher-order helpers are useful when they simplify local logic,
  such as sorting or iteration; do not obscure control flow to appear
  “functional.”
