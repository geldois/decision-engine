# Explicit composition root over FastAPI dependency injection

## Status

Accepted

## Context

The initial implementation wired infrastructure into route handlers using FastAPI's built-in
dependency injection via `Depends()`. This introduced two structural problems:

1. Use case classes were constructed inside `Depends()` callables, coupling the application layer to
   the HTTP framework. Testing a use case in isolation required either a full FastAPI test client or
   patching `app.dependency_overrides`.
2. Dependencies were resolved lazily at request time, making the construction graph invisible until
   the first request hit.

## Decision

`Depends()` is removed entirely. All dependencies are assembled eagerly at startup in `bootstrap.py`
via a `build_container` function. It selects the persistence backend from settings, instantiates the
full use case set with the backend's `UoWFactory`, and returns a fully constructed `Container`.

Route handlers receive this container via closure — passed as an argument to router builder
functions. They call into the container's use cases with no knowledge of how those use cases were
assembled.

Test injection uses `ContainerOverride` — a typed struct of optional pre-wired database instances.
`build_container` checks for overrides before constructing real infrastructure, so tests pass
pre-wired backends without side effects on the application's wiring.

## Consequences

- Use cases are framework-agnostic: executing one is a plain Python call with no HTTP context. It
  can be invoked from tests, CLI commands, or any other interface without a running server.
- The full construction graph is visible and statically verifiable in `bootstrap.py`. If a
  dependency fails to initialize, the application fails at startup rather than at the first request.
- Tests construct a container directly via `build_container` — no `TestClient`, no
  `app.dependency_overrides` mutations, no shared app state between test functions.
- Trade-off: no lazy initialization. All infrastructure is constructed at startup regardless of the
  code paths exercised. A misconfigured database URL fails the startup even if no request would have
  reached the database yet.
