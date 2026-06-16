# Transaction Rollback Isolation with Dual-Backend Test Parameterization

## Status

Accepted

## Context

Integration tests that write to PostgreSQL accumulate state between runs unless explicitly cleaned. Truncating tables or dropping and recreating the schema between tests is slow and couples the test lifecycle to DDL operations.

A second risk is backend divergence: tests written exclusively against an in-memory implementation can pass while the real SQL backend silently differs. JSONB codec bugs, constraint ordering, query semantics, or index behavior can all produce divergence that only manifests in production.

## Decision

Isolation is handled via PostgreSQL transaction rollback. Each test opens a real connection, begins a transaction, and the fixture rolls it back on teardown — no DDL required between tests. The SQLAlchemy `Session` runs in savepoint mode so it can commit within the test without promoting to the actual transaction:

```python
@pytest.fixture
def connection(engine):
    connection = engine.connect()
    transaction = connection.begin()
    yield connection
    transaction.rollback()

@pytest.fixture
def session(connection):
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()
```

Schema setup runs once per session via `alembic upgrade head` and is torn down with `alembic downgrade base` at the end.

Every test that touches persistence is parameterized over both backends via a `persistence` fixture:

```python
@pytest.fixture(params=["in_memory", "postgresql"])
def persistence(request):
    return request.param
```

`ContainerOverride` wires the correct DB implementation based on the parameter. The same test body exercises both backends without branching.

## Consequences

- Each test runs in fully isolated state with no cleanup step and no shared mutable state between functions.
- Any behavioral divergence between the in-memory and SQL backends fails immediately. Codec bugs, constraint violations, and query ordering issues are caught during development.
- CI provisions a containerized PostgreSQL (GitHub Actions `services:`) and runs the full parameterized suite on every push.
- Trade-off: the savepoint pattern requires the SQLAlchemy `Session` to always use the externally-provided connection rather than opening its own. Any path that bypasses the injected session would escape isolation. This constraint is enforced by the composition root: use cases receive only a `UoWFactory`, never a direct engine or session reference.
- Trade-off: the test suite runs each test twice, increasing total runtime. This cost is accepted — correctness on both backends is not optional.
