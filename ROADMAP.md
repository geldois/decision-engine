# Decision Engine - Roadmap

## Domain

- [ ] Replace generic exceptions with domain-specific ones
- [ ] Define error types (EventError, RuleError, DecisionError)
- [ ] Remove silent failures (no hidden try/except)
- [x] Enforce strict invariants in entities
- [ ] Define explicit rule evaluation behavior (order, priority)
- [ ] Add rule priority and deterministic execution
- [ ] Support rule composition (AND / OR)
- [ ] Ensure type consistency (no implicit coercion)
- [ ] Improve decision explanation (full evaluation context)

## Domain - Audit Log

- [ ] Create AuditLog entity
- [ ] Record decision execution (event, rule, outcome)
- [ ] Persist audit logs
- [ ] Integrate into use cases
- [ ] Expose audit endpoint (read-only)
- [ ] Ensure audit does not break main flow

## Infrastructure

- [x] Enforce referential integrity
- [x] Define deterministic save behavior
- [ ] Prevent duplication/conflicts
- [x] Ensure transaction consistency
- [ ] Handle failure paths explicitly
- [ ] Add domain-oriented queries

## Infrastructure - PostgreSQL

- [ ] Introduce PostgreSQL (replace SQLite)
- [ ] Configure connection via env
- [ ] Adapt models if needed
- [ ] Add DB indexes (critical fields)
- [ ] Validate queries and performance basics

## Application

- [x] Define input contracts (structured models, no raw dict)
- [x] Define output contracts (no domain leakage)
- [ ] Make orchestration explicit (step-by-step flows)
- [ ] Handle failures explicitly (domain vs infra)
- [ ] Prevent partial state (atomic flows)
- [ ] Add simple retry/failure strategies
- [x] Keep business logic out of application layer

## API

- [ ] Define request schemas
- [ ] Define response schemas
- [ ] Map errors (domain → 4xx, infra → 5xx)
- [ ] Ensure idempotency where needed
- [ ] Separate validation (API vs domain)

## Bootstrap

- [ ] Ensure container is single source of truth
- [x] Remove hidden wiring
- [ ] Validate config at startup
- [x] Support envs (test/dev/prod)

## Observability

- [ ] Structured logging (request → decision → persistence)
- [ ] Log errors explicitly
- [ ] Add minimal tracing (ids per request)

## Testing

- [x] Isolated tests (no shared state)
- [ ] Use bootstrap in tests
- [x] Cover domain rules
- [x] Cover failure scenarios

## Deployment

- [ ] Dockerize app
- [ ] Add migrations
- [ ] Keep CI running
