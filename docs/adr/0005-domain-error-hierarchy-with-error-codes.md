# Domain error hierarchy with typed error codes

## Status

Accepted — supersedes the initial approach of raising generic Python exceptions with string messages

## Context

The early codebase raised generic exceptions with string messages to signal domain invariant
violations. At the HTTP boundary, catching these required matching on exception type and message
strings — fragile and untestable. HTTP status code decisions were also scattered across individual
route handlers, each duplicating its own mapping logic.

## Decision

A single abstract base anchors a hierarchy of domain errors, grouped by aggregate (condition,
decision, event, rule). Every concrete error declares a stable, machine-readable error code as part
of its own class definition, and the base enforces this as a contract: an error that fails to declare
a code is rejected when its class is defined, not when it is first raised.

Each concrete error is its own type. The class name identifies the invariant that was violated, and
the error builds its own human-readable message from its typed attributes — so raise sites carry no
string literals and read as a single, self-documenting expression. Errors are immutable once
constructed.

A single boundary mapper translates each error code to an HTTP status and a uniform error response.
Route handlers catch the domain base once and delegate to the mapper; no handler names or imports a
concrete error.

## Consequences

- Error codes are stable identifiers, decoupled from message wording. Tests and API clients assert on
  the code, not the message, and remain resilient to rewording.
- The identity contract guarantees every error is self-describing — a code plus a built message — and
  makes a code-less error impossible to define.
- The HTTP layer catches one type and delegates mapping entirely; the interface never couples to
  concrete error classes.
- Trade-off: each new error condition is a new class. This is intentional — it keeps the domain's
  error surface explicit and reviewable, and prevents undocumented error paths from accumulating
  silently.
