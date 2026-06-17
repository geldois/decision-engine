# Transaction rollback isolation with dual-backend test parameterization

## Status

Accepted

## Context

Integration tests that write to PostgreSQL accumulate state between runs unless explicitly cleaned.
Truncating tables or dropping and recreating the schema between tests is slow and couples the test
lifecycle to DDL operations.

A second risk is backend divergence: tests written exclusively against an in-memory implementation
can pass while the real SQL backend silently differs. JSONB codec bugs, constraint ordering, query
semantics, or index behavior can all produce divergence that only manifests in production.

## Decision

Isolation is handled via PostgreSQL transaction rollback. Each test opens a real connection, begins
a transaction, and the fixture rolls it back on teardown — no DDL required between tests. The
SQLAlchemy `Session` runs in savepoint mode so use case commits within the test do not promote to
the outer transaction, preserving isolation without preventing writes.

Schema setup runs once per session via Alembic and is torn down at the end.

Every test that touches persistence is parameterized over both backends — in-memory and PostgreSQL
— via a `persistence` fixture. `ContainerOverride` wires the correct backend based on the parameter.
The same test body exercises both backends without branching.

## Consequences

- Each test runs in fully isolated state with no cleanup step and no shared mutable state between
  functions.
- Any behavioral divergence between the in-memory and SQL backends fails immediately. Codec bugs,
  constraint violations, and query ordering issues are caught during development.
- CI provisions a containerized PostgreSQL and runs the full parameterized suite on every push.
- Trade-off: the savepoint pattern requires the SQLAlchemy `Session` to always use the
  externally-provided connection rather than opening its own. Any path that bypasses the injected
  session would escape isolation. This constraint is enforced by the composition root: use cases
  receive only a `UoWFactory`, never a direct engine or session reference.
- Trade-off: the test suite runs each test twice, increasing total runtime. This cost is accepted —
  correctness on both backends is not optional.
