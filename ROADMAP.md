# Decision Engine – Roadmap

The objective is to transform this project from a clean architectural MVP into a production-oriented backend system with strong fundamentals in database design, HTTP semantics, transaction handling, and engineering practices.

The current system is fully functional and tested. The roadmap below defines the next technical evolution steps toward production-grade robustness.

---
## PHASE 1 – Database & SQL Mastery (Foundational)

- [ ] Introduce persistent Rule repository (SQL)
- [ ] Model Rule table properly (columns, constraints)
- [ ] Add relationship between Event and Decision in database
- [ ] Create database indexes where appropriate
- [ ] Write integration tests hitting real SQLite database

---
## PHASE 2 – SQLAlchemy Deep Understanding

- [ ] Understand Session lifecycle
- [ ] Understand flush vs commit
- [ ] Implement transaction boundary in use case
- [ ] Refactor repositories to avoid implicit session misuse
- [ ] Add rollback on failure
- [ ] Introduce migration tool (Alembic)

---
## PHASE 3 – HTTP & Application Robustness

- [ ] Replace generic exception handling in API
- [ ] Introduce domain-specific exceptions
- [ ] Map domain exceptions to correct HTTP status codes (400 / 409 / 500)
- [ ] Implement idempotency for RegisterEvent
- [ ] Improve validation boundaries
- [ ] Add structured logging

---
## PHASE 4 – Production Engineering

- [ ] Add Dockerfile
- [ ] Add docker-compose (app + db)
- [ ] Configure environment variables
- [ ] Configure CI pipeline running pytest
- [ ] Add coverage report
- [ ] Add health check with DB verification

---
## PHASE 5 – Domain Evolution

- [ ] Add rule priority mechanism
- [ ] Add versioning for rules
- [ ] Persist Decision entity explicitly
- [ ] Implement audit logging
- [ ] Improve DecisionEngine extensibility

---
## Final Objective

- Strong SQL understanding
- Solid transaction handling
- Correct HTTP semantics
- Production-ready engineering baseline
- Clean and defensible architecture

---
