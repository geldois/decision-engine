## v1.1.0 (2026-06-17)

### Feat

- **observability**: add structured logging across all use cases and HTTP layer
- **observability**: add structlog logging with correlation id

### Fix

- **readme**: correct rule example to use valid operators

### Refactor

- enforce strict Ruff and basedpyright rules across the codebase
- **typing**: move type-only imports under TYPE_CHECKING
- **tests**: consolidate scattered factories into conftest make_* fixtures
- resolve basedpyright strict findings in src
- **domain**: replace Any with object in operator and field value objects
- **typing**: add from __future__ and replace UoW Protocol with a type alias
- **interface**: move cli into the interface layer
- **persistence**: instantiate repositories inside the unit of work
- **persistence**: rename in_memory to mem
- **errors**: adopt frozen DomainError hierarchy with error_code contract
- rename package to decision_engine and reorganize modules
- **repo**: remove roadmap and obsolete tooling

## v1.0.0 (2026-05-05)

### BREAKING CHANGE

- dependency wiring is now exclusively handled by bootstrap; FastAPI DI is no longer used

### Feat

- complete infrastructure overhaul with PostgreSQL, Alembic, and test isolation
- **decision-engine**: add decision trace with AST-based evaluation and visitor serialization
- **domain, application, infra**: implement rule evaluation using AST-based conditions
- **domain**: add rule priority with deterministic evaluation and temporal modeling (created_at, occurred_at)
- **roadmap**: refine and prioritize roadmap blocks
- **devtools**: improve context/delta tooling with scoped filters and structured diff output
- **api**: introduce event ingestion and decision evaluation endpoints
- **api**: expose swagger via root redirect
- **decision-engine**: introduce decision persistence and UUID domain identities
- **rule-engine**: introduce declarative rules and SQL rule repository
- **persistence**: activate SQL-backed EventRepository via composition root
- **api**: add HTTP adapter for RegisterEvent use case
- **application**: complete RegisterEvent use case with rule-based decision flow
- **application**: add RegisterEvent application service and initial test
- **infrastructure**: add in-memory EventRepository with save and get_by_id
- **testing**: enable domain testing with pytest and stabilize entities
- **domain**: add Decision entity
- **domain**: add Rule entity with callable condition
- **domain**: add Event entity
- add basic FastAPI app with health check

### Fix

- **decision-engine**: preserve event identity in SQL repository and store payload as JSON
- **api**: initialize database using FastAPI lifespan
- **domain**: align domain contracts and close decision core

### Refactor

- **domain**: replace generic exceptions with domain-specific ones and centralize HTTP error mapping
- **bootstrap, api, domain**: introduce explicit composition root with overrides and remove FastAPI DI
- **project**: reorganize domain structure and add AI context tooling
- **domain**: introduce DecisionOutcome and explicit outcome-to-status mapping
- **domain**: promote decision logic to domain service (DecisionEngine)
- **architecture**: invert repository dependencies and isolate infrastructure in composition root
- **application**: rename repositories to clarify contract role
- **typing**: clarify optional types and keyword argument usage at boundaries
- **application**: introduce request/response DTO boundary for RegisterEvent
- **domain**: finalize DecisionService logic and tests
- **domain**: improve type validation using isinstance
