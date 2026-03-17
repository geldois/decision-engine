from functools import partial

from app.application.use_cases.produce_decision_use_case import (
    produce_decision_use_case_factory,
)
from app.application.use_cases.register_event_use_case import (
    register_event_use_case_factory,
)
from app.application.use_cases.register_rule_use_case import (
    register_rule_use_case_factory,
)
from app.bootstrap.config import Config
from app.infrastructure.database.base import base_factory
from app.infrastructure.database.engine import engine_factory
from app.infrastructure.database.session import get_session_factory
from app.infrastructure.persistence.in_memory.repositories.in_memory_decision_repository import (
    in_memory_decision_repository_factory,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_event_repository import (
    in_memory_event_repository_factory,
)
from app.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    in_memory_rule_repository_factory,
)
from app.infrastructure.persistence.in_memory.storage.in_memory_storage import (
    in_memory_storage_factory,
)
from app.infrastructure.persistence.in_memory.unit_of_work.in_memory_unit_of_work import (
    InMemoryUnitOfWork,
)
from app.infrastructure.persistence.sql.repositories.sql_decision_repository import (
    sql_decision_repository_factory,
)
from app.infrastructure.persistence.sql.repositories.sql_event_repository import (
    sql_event_repository_factory,
)
from app.infrastructure.persistence.sql.repositories.sql_rule_repository import (
    sql_rule_repository_factory,
)
from app.infrastructure.persistence.sql.unit_of_work.sql_unit_of_work import (
    SqlUnitOfWork,
)


class Container:
    def __init__(self, settings: Config):
        self.settings = settings

    def build(self):
        self.database_url = self.settings.get_env()

        if self.database_url:
            self.engine = engine_factory(
                database_url=self.database_url,
                check_same_thread=False
                if self.database_url == "sqlite:///:memory:"
                else True,
                staticpool=True if self.database_url == "sqlite:///:memory:" else False,
            )
            base_factory(engine=self.engine)
            self.session_factory = get_session_factory(engine=self.engine)

            self.decision_repository_factory = sql_decision_repository_factory
            self.event_repository_factory = sql_event_repository_factory
            self.rule_repository_factory = sql_rule_repository_factory

            self.unit_of_work_factory = partial(
                SqlUnitOfWork,
                session_factory=self.session_factory,
                decision_repository_factory=self.decision_repository_factory,
                event_repository_factory=self.event_repository_factory,
                rule_repository_factory=self.rule_repository_factory,
            )

            self.produce_decision_use_case = produce_decision_use_case_factory(
                unit_of_work_factory=self.unit_of_work_factory
            )
            self.register_event_use_case = register_event_use_case_factory(
                unit_of_work_factory=self.unit_of_work_factory
            )
            self.register_rule_use_case = register_rule_use_case_factory(
                unit_of_work_factory=self.unit_of_work_factory
            )
        else:
            self.in_memory_storage_factory = in_memory_storage_factory

            self.decision_repository_factory = in_memory_decision_repository_factory
            self.event_repository_factory = in_memory_event_repository_factory
            self.rule_repository_factory = in_memory_rule_repository_factory

            self.unit_of_work_factory = partial(
                InMemoryUnitOfWork,
                in_memory_storage_factory=self.in_memory_storage_factory,
                decision_repository_factory=self.decision_repository_factory,
                event_repository_factory=self.event_repository_factory,
                rule_repository_factory=self.rule_repository_factory,
            )

            self.produce_decision_use_case = produce_decision_use_case_factory(
                unit_of_work_factory=self.unit_of_work_factory
            )
            self.register_event_use_case = register_event_use_case_factory(
                unit_of_work_factory=self.unit_of_work_factory
            )
            self.register_rule_use_case = register_rule_use_case_factory(
                unit_of_work_factory=self.unit_of_work_factory
            )
