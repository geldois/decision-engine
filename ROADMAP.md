# Decision Engine – Roadmap

## Domain refinement (hardening)

- [ ] Replace ValueError with domain-specific exceptions
- [ ] Define explicit error taxonomy (EventError, RuleError, DecisionError)
- [ ] Remove silent failures (no try/except returning False)
- [ ] Make rule evaluation explicit (priority / order)
- [ ] Strengthen invariants across entities
- [ ] Validate event payload structure (even minimally)
- [ ] Ensure use cases never raise generic exceptions

## API evolution

- [x] Split event ingestion and decision evaluation
- [x] Introduce /events/ endpoint
- [x] Introduce /rules/ endpoint
- [x] Introduce /decisions/ endpoint

## SQL persistence

- [x] Persist rules in SQL repository
- [x] Persist decisions in database
- [x] Add event → decision relationship
- [x] Migrate dependencies to pyproject.toml
- [x] Introduce CLI entrypoint
- [x] Package project as installable module

## Public deployment

- [x] Deploy API publicly (Render)
- [x] Configure environment variables
- [x] Add health check endpoint

## CI/CD

- [x] Add CI pipeline (tests)
- [x] Enable Continuous Deployment

## Application robustness

- [x] Introduce transaction boundary
- [x] Implement rollback
- [ ] Add DB indexes
- [ ] Domain exceptions
- [ ] HTTP mapping

## Observability

- [ ] Structured logging

## Infrastructure

- [ ] Dockerfile
- [ ] docker-compose
- [ ] database migrations

## System behavior

- [ ] Load test API
- [ ] Concurrent rule evaluation
- [ ] Failure scenarios
