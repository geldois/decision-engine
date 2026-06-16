# Explicit Composition Root over FastAPI Dependency Injection

## Status

Accepted

## Context

The initial implementation wired infrastructure into route handlers using FastAPI's built-in dependency injection (`Depends()`). This introduced two structural problems:

1. Use case classes were constructed inside `Depends()` callables, coupling the application layer to the HTTP framework. Testing a use case in isolation required either a full FastAPI test client or patching `app.dependency_overrides`.
2. Dependencies were resolved lazily at request time, making the construction graph invisible until the first request hit.

## Decision

Remove `Depends()` entirely. Build all dependencies eagerly at startup in `bootstrap.py`:

```python
def build_container(settings, overrides) -> Container:
    db = ...  # selected by settings.persistence
    use_cases = UseCaseSet(
        produce_decision=ProduceDecisionUseCase(uow_factory=db.uow_factory),
        register_event=RegisterEventUseCase(uow_factory=db.uow_factory),
        register_rule=RegisterRuleUseCase(uow_factory=db.uow_factory),
    )
    return Container(settings=settings, db=db, use_cases=use_cases)
```

Route handlers receive the fully constructed `Container` via closure, passed as an argument to router builder functions. They call `container.use_cases.produce_decision.execute(dto)` with no knowledge of how the use case was assembled.

Test injection uses `ContainerOverride` — a typed struct of optional pre-wired DB instances. `build_container` checks for overrides before constructing real infrastructure, so tests pass a pre-wired `InMemoryDB` or `SQLAlchemyDB` without side effects on the application's wiring.

## Consequences

- Use cases are framework-agnostic: `ProduceDecisionUseCase.execute(dto)` is a plain Python call with no HTTP context. It can be invoked from tests, CLI commands, or any other interface without a running server.
- The full construction graph is visible and statically verifiable in `bootstrap.py`. If a dependency fails to initialize, the application fails at startup rather than at the first request that needs it.
- Tests construct a container directly via `build_container(settings, overrides)` — no `TestClient`, no `app.dependency_overrides` mutations, no shared app state between test functions.
- Trade-off: no lazy initialization. All infrastructure is constructed at startup regardless of the code paths exercised. A misconfigured database URL fails the startup even if no request would have reached the database yet.
