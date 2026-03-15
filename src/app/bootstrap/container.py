from sqlalchemy.orm import Session

from app.application.repositories.decision_repository_contract import (
    DecisionRepositoryContract,
)
from app.application.repositories.event_repository_contract import (
    EventRepositoryContract,
)
from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.bootstrap.config import Config
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.database.engine import (
    create_database_engine,
    create_session_factory,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_decision_repository import (
    InMemoryDecisionRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    InMemoryEventRepository,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    InMemoryRuleRepository,
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


class Container:
    def __init__(self, settings: Config):
        self.settings = settings
        self.decision_engine = DecisionEngine()

    def build(self):
        if self.settings.database_url:
            self.engine = create_database_engine(
                database_url=self.settings.database_url,
                check_same_thread=False
                if self.settings.database_url == "sqlite:///:memory:"
                else True,
                staticpool=True
                if self.settings.database_url == "sqlite:///:memory:"
                else False,
            )

            self.session_factory = create_session_factory(engine=self.engine)

        def decision_repository_factory(
            session: Session,
        ) -> DecisionRepositoryContract:
            if self.settings.database_url == "sqlite:///:memory:":
                return InMemoryDecisionRepository()
            else:
                return SqlDecisionRepository(session=session)

        def event_repository_factory(
            session: Session,
        ) -> EventRepositoryContract:
            if self.settings.database_url == "sqlite:///:memory:":
                return InMemoryEventRepository()
            else:
                return SqlEventRepository(session=session)

        def rule_repository_factory(
            session: Session,
        ) -> RuleRepositoryContract:
            if self.settings.database_url == "sqlite:///:memory:":
                return InMemoryRuleRepository()
            else:
                return SqlRuleRepository(session=session)

        def get_produce_decision_use_case(
            unit_of_work=self.sql_unit_of_work,
        ) -> ProduceDecisionUseCase:
            return ProduceDecisionUseCase(unit_of_work=unit_of_work)

        def get_register_event_use_case(
            unit_of_work=self.sql_unit_of_work,
        ) -> RegisterEventUseCase:
            return RegisterEventUseCase(unit_of_work=unit_of_work)

        def get_register_rule_use_case(
            unit_of_work=self.sql_unit_of_work,
        ) -> RegisterRuleUseCase:
            return RegisterRuleUseCase(unit_of_work=unit_of_work)
