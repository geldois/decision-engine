# Decision Engine – Roadmap

## SQL persistence

- [x] Persist rules in SQL repository
- [x] Persist decisions in database
- [x] Add event → decision relationship
- [x] Migrate dependencies to pyproject.toml
- [x] Introduce CLI entrypoint
- [x] Package project as installable module

## Public deployment

- [x] Deploy API publicly (Render)
- [ ] Configure environment variables
- [x] Add health check endpoint

## CI/CD

- [x] Add CI pipeline (tests)
- [x] Enable Continuous Deployment

## Application robustness

- [ ] Introduce transaction boundary
- [ ] Implement rollback
- [ ] Add DB indexes
- [ ] Domain exceptions
- [ ] HTTP mapping

## Observability

- [ ] Structured logging

## Infrastructure

- [ ] Dockerfile
- [ ] docker-compose
- [ ] database migrations
