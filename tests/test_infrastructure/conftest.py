import pytest
from sqlalchemy.orm import Session

from app.infrastructure.persistence.in_memory.in_memory_storage import InMemoryStorage
from app.infrastructure.persistence.in_memory.repositories.in_memory_decision_repository import (
    InMemoryDecisionRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    InMemoryRuleRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_decision_repository import (
    SQLAlchemyDecisionRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_event_repository import (
    SQLAlchemyEventRepository,
)
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_rule_repository import (
    SQLAlchemyRuleRepository,
)


@pytest.fixture(scope="function")
def in_memory_decision_repo(
    in_memory_storage: InMemoryStorage,
) -> InMemoryDecisionRepository:
    return InMemoryDecisionRepository(storage=in_memory_storage)


@pytest.fixture(scope="function")
def in_memory_event_repo(
    in_memory_storage: InMemoryStorage,
) -> InMemoryEventRepository:
    return InMemoryEventRepository(storage=in_memory_storage)


@pytest.fixture(scope="function")
def in_memory_rule_repo(
    in_memory_storage: InMemoryStorage,
) -> InMemoryRuleRepository:
    return InMemoryRuleRepository(storage=in_memory_storage)


@pytest.fixture(scope="function")
def sqlalchemy_decision_repo(
    session: Session,
) -> SQLAlchemyDecisionRepository:
    return SQLAlchemyDecisionRepository(session=session)


@pytest.fixture(scope="function")
def sqlalchemy_event_repo(session: Session) -> SQLAlchemyEventRepository:
    return SQLAlchemyEventRepository(session=session)


@pytest.fixture(scope="function")
def sqlalchemy_rule_repo(session: Session) -> SQLAlchemyRuleRepository:
    return SQLAlchemyRuleRepository(session=session)
