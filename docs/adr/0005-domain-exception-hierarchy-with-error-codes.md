# Domain Exception Hierarchy with Typed Error Codes

## Status

Accepted — Supersedes the initial approach of raising generic Python exceptions with string messages

## Context

The early codebase raised `ValueError` and `RuntimeError` with string messages to signal domain invariant violations. At the HTTP boundary, catching these required matching on exception type and message strings — fragile and untestable. HTTP status code decisions were also scattered across individual route handlers, each duplicating its own mapping logic.

## Decision

Define a `DomainException` base with two mandatory structural fields: a human-readable `message` and a typed `ErrorCode` enum value:

```python
class DomainException(Exception):
    def __init__(self, message: str, error_code: ErrorCode, details: dict | None) -> None:
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)
```

Domain-specific exception classes (`ConditionException`, `EventException`, `RuleException`, `DecisionException`) inherit from `DomainException`. Each exposes named factory classmethods that encapsulate the error code and message:

```python
class EventException(DomainException):
    @classmethod
    def event_not_found(cls, details=None) -> EventException:
        return cls(message="Event not found", error_code=ErrorCode.EVENT_NOT_FOUND, details=details)
```

A central `HTTPErrorCodeMapper` maps each `ErrorCode` value to an HTTP status code. Route handlers catch `DomainException` once, delegate to the mapper, and return a uniform `HTTPErrorResponse`. No handler knows about concrete exception classes.

## Consequences

- The full error surface of the domain is enumerated in `ErrorCode`. Adding a new error condition requires updating the enum, making omissions visible.
- The HTTP layer catches one type (`DomainException`) and delegates mapping entirely. No route handler imports concrete exception classes.
- Tests assert on `exception.error_code` rather than parsing string messages, making them resilient to wording changes.
- Factory classmethods make raise sites self-documenting: `raise EventException.event_not_found()` names the condition explicitly.
- Trade-off: adding a new error condition requires touching both the exception class and `ErrorCode`. This is intentional — it prevents undocumented error paths from accumulating silently.
