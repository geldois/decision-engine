# decision-engine

Rule-based decision engine built with Clean Architecture and strict TDD, focused on correctness, explicit boundaries, and deterministic decision-making.

## Current Status

- Core domain fully modeled and unit tested (Event, Rule, Decision).
- Application layer implemented with explicit use cases and DTO boundaries.
- HTTP API exposed via FastAPI with dependency injection and composition root.
- API contract protected by automated tests (200 / 422 / 500 cases).
- In-memory repositories used as infrastructure placeholders.
- Domain outcomes modeled via explicit enum (DecisionOutcome), mapped explicitly to API boundary status.

## Design Principles

- Explicit domain modeling with clear boundaries between layers, strong invariants and value semantics.
- Deterministic rule evaluation with no side effects.
- Domain logic isolated from frameworks and infrastructure.
- Application behavior expressed through use cases, not controllers.
- Domain-level outcome modeling decoupled from application boundary representations.

## Testing Strategy

- Domain and application layers developed using TDD.
- Business logic tested independently from the HTTP layer.
- API boundary locked with contract tests covering:
    - successful requests (200)
    - validation failures (422)
    - internal failures (500)

## Non-goals

- This project does not aim to be production-complete at this stage.
- Persistence and external integrations are intentionally incremental.
- AI-assisted analysis is explicitly out of scope for the current MVP.

## Roadmap

- Replace in-memory repositories with real persistence.
- Introduce application-level invariants and idempotency.
- Implement audit logging as a secondary use case.
