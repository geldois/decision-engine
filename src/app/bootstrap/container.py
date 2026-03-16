from sqlalchemy.orm import Session

from app.application.contracts.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.application.contracts.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.application.contracts.repositories.rule_repository_contract import (
    RuleRepositoryContract,
)
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.bootstrap.config import Config
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.database.base import create_base
from app.infrastructure.database.engine import create_database_engine
from app.infrastructure.database.session import create_session_factory
from app.infrastructure.persistence.in_memory.repositories.in_memory_decision_repository import (
    InMemoryDecisionRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    InMemoryRuleRepository,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    InMemoryStorage,
)
from app.infrastructure.persistence.in_memory.unit_of_work.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)
from app.infrastructure.persistence.sql.repositories.sql_decision_repository import (
    SqlDecisionRepository,
)
from app.infrastructure.persistence.sql.repositories.sql_event_repository import (
    SqlEventRepository,
)
from app.infrastructure.persistence.sql.repositories.sql_rule_repository import (
    SqlRuleRepository,
)
from app.infrastructure.persistence.sql.unit_of_work.sql_unit_of_work import (
    SqlUnitOfWork,
)


class Container:
    def __init__(self, settings: Config):
        self.settings = settings

    def build(self):
        self.database_url = self.settings.get_env()
        self.decision_engine = DecisionEngine()

        def decision_repository_factory(
            s: Session | InMemoryStorage,
        ) -> DecisionRepositoryContract:
            if isinstance(s, Session):
                return SqlDecisionRepository(session=s)
            else:
                return InMemoryDecisionRepository(in_memory_storage=s)

        def event_repository_factory(
            s: Session | InMemoryStorage,
        ) -> EventRepositoryContract:
            if isinstance(s, Session):
                return SqlEventRepository(session=s)
            else:
                return InMemoryEventRepository(in_memory_storage=s)

        def rule_repository_factory(
            s: Session | InMemoryStorage,
        ) -> RuleRepositoryContract:
            if isinstance(s, Session):
                return SqlRuleRepository(session=s)
            else:
                return InMemoryRuleRepository(in_memory_storage=s)

        self.decision_repository_factory = decision_repository_factory
        self.event_repository_factory = event_repository_factory
        self.rule_repository_factory = rule_repository_factory

        if self.database_url:
            self.engine = create_database_engine(
                database_url=self.database_url,
                check_same_thread=False
                if self.database_url == "sqlite:///:memory:"
                else True,
                staticpool=True
                if self.database_url == "sqlite:///:memory:"
                else False,
            )

            create_base(engine=self.engine)

            self.session_factory = create_session_factory(engine=self.engine)
            self.unit_of_work = SqlUnitOfWork(
                session_factory=self.session_factory,
                decision_repository_factory=self.decision_repository_factory,
                event_repository_factory=self.event_repository_factory,
                rule_repository_factory=self.rule_repository_factory,
            )
        else:

            def in_memory_storage_factory() -> InMemoryStorage:
                return InMemoryStorage()

            self.in_memory_storage_factory = in_memory_storage_factory
            self.unit_of_work = InMemoryUnitOfWork(
                in_memory_storage_factory=self.in_memory_storage_factory,
                decision_repository_factory=self.decision_repository_factory,
                event_repository_factory=self.event_repository_factory,
                rule_repository_factory=self.rule_repository_factory,
            )

        def get_produce_decision_use_case() -> ProduceDecisionUseCase:
            return ProduceDecisionUseCase(
                unit_of_work=self.unit_of_work, decision_engine=self.decision_engine
            )

        def get_register_event_use_case() -> RegisterEventUseCase:
            return RegisterEventUseCase(unit_of_work=self.unit_of_work)

        def get_register_rule_use_case() -> RegisterRuleUseCase:
            return RegisterRuleUseCase(unit_of_work=self.unit_of_work)

        self.get_produce_decision_use_case = get_produce_decision_use_case
        self.get_register_event_use_case = get_register_event_use_case
        self.get_register_rule_use_case = get_register_rule_use_case
