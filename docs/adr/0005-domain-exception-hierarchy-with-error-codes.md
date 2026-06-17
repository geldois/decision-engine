# Domain exception hierarchy with typed error codes

## Status

Accepted — supersedes the initial approach of raising generic Python exceptions with string messages

## Context

The early codebase raised `ValueError` and `RuntimeError` with string messages to signal domain
invariant violations. At the HTTP boundary, catching these required matching on exception type and
message strings — fragile and untestable. HTTP status code decisions were also scattered across
individual route handlers, each duplicating its own mapping logic.

## Decision

`DomainException` is the base class with two mandatory structural fields: a human-readable `message`
string and a typed `ErrorCode` enum value. An optional `details` dict carries structured context.

Domain-specific subclasses — `ConditionException`, `EventException`, `RuleException`,
`DecisionException` — inherit from `DomainException`. Each exposes named factory classmethods that
encapsulate the error code and message. Raise sites are self-documenting: the classmethod name
identifies the error condition explicitly without embedding a string message at the callsite.

`HTTPErrorCodeMapper` maps each `ErrorCode` value to an HTTP status code. Route handlers catch
`DomainException` once, delegate to the mapper, and return a uniform `HTTPErrorResponse`. No handler
imports or names any concrete exception class.

## Consequences

- The full error surface of the domain is enumerated in `ErrorCode`. Adding a new error condition
  requires updating the enum, making omissions visible.
- The HTTP layer catches one type and delegates mapping entirely. No route handler imports concrete
  exception classes.
- Tests assert on `exception.error_code` rather than parsing string messages, making them resilient
  to wording changes.
- Trade-off: adding a new error condition requires touching both the exception class and `ErrorCode`.
  This is intentional — it prevents undocumented error paths from accumulating silently.
