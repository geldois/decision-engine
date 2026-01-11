# descissor-api

Rule-based decision engine with auditability and AI-assisted insights.

## Current Status

- Core domain modeled and tested (Event, Rule, Decision, AuditLog).
- Focus is currently on domain correctness and explicit business rules.
- API layer, persistence, and AI-assisted analysis are planned next steps.

## Design Principles

- Explicit domain modeling with clear boundaries between entities and services.
- Deterministic rule evaluation (no side effects).
- Auditability as a first-class concern.
- Domain logic isolated from infraestructure and frameworks.

## Non-goals

- This project does not aim to provide a production-ready rule engine.
- No persistence or external integrations are implemented yet.
- AI components are intentionally out of scope for the current MVP.
