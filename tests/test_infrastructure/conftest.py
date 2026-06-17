import pytest
from sqlalchemy.orm import Session

from decision_engine.infrastructure.persistence.mem.mem_storage import MemStorage
from decision_engine.infrastructure.persistence.mem.repositories.mem_decision_repository import (  # noqa: E501
    MemDecisionRepository,
)
from decision_engine.infrastructure.persistence.mem.repositories.mem_event_repository import (  # noqa: E501
    MemEventRepository,
)
from decision_engine.infrastructure.persistence.mem.repositories.mem_rule_repository import (  # noqa: E501
    MemRuleRepository,
)
from decision_engine.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_decision_repository import (  # noqa: E501
    SQLAlchemyDecisionRepository,
)
from decision_engine.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_event_repository import (  # noqa: E501
    SQLAlchemyEventRepository,
)
from decision_engine.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_rule_repository import (  # noqa: E501
    SQLAlchemyRuleRepository,
)


@pytest.fixture
def mem_decision_repo(
    mem_storage: MemStorage,
) -> MemDecisionRepository:
    return MemDecisionRepository(storage=mem_storage)


@pytest.fixture
def mem_event_repo(
    mem_storage: MemStorage,
) -> MemEventRepository:
    return MemEventRepository(storage=mem_storage)


@pytest.fixture
def mem_rule_repo(
    mem_storage: MemStorage,
) -> MemRuleRepository:
    return MemRuleRepository(storage=mem_storage)


@pytest.fixture
def sqlalchemy_decision_repo(
    session: Session,
) -> SQLAlchemyDecisionRepository:
    return SQLAlchemyDecisionRepository(session=session)


@pytest.fixture
def sqlalchemy_event_repo(session: Session) -> SQLAlchemyEventRepository:
    return SQLAlchemyEventRepository(session=session)


@pytest.fixture
def sqlalchemy_rule_repo(session: Session) -> SQLAlchemyRuleRepository:
    return SQLAlchemyRuleRepository(session=session)
