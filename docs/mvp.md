# MVP

Decision Engine is a backend system that manages events, applies deterministic rules, and records decisions with full auditability.

## Status

The MVP currently includes:

- Deterministic decision flow from event registration to decision outcome.
- Core domain entities implemented and unit tested (Event, Rule, Decision).
- Application use case (`RegisterEvent`) with explicit DTO boundaries.
- HTTP API exposed via FastAPI with dependency injection and composition root.
- API contract protected by automated tests (200 / 422 / 500 cases).
- In-memory repositories used as infrastructure placeholders.

## Entities

- Rule – Defines a condition and determines an outcome. Rules are deterministic and side-effect free.
- Event – The target of rules. Provides input data and defines the decision context.
- Decision – The result of applying rules to an event. References the event, the applied rule (if any), and the outcome.
- AuditLog – Records information about decisions taken (who, when, why, and result). Planned for a later iteration of the MVP.
