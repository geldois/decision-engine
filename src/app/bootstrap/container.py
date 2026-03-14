import fastapi, sqlalchemy, sqlalchemy.orm

from app.application.repositories.decision_repository_contract import DecisionRepositoryContract
from app.application.repositories.event_repository_contract import EventRepositoryContract
from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.bootstrap.config import Config
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.database.engine import create_engine, create_session
from app.infrastructure.repositories.in_memory_decision_repository import InMemoryDecisionRepository
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository
from app.infrastructure.repositories.sql_decision_repository import SqlDecisionRepository
from app.infrastructure.repositories.sql_event_repository import SqlEventRepository
from app.infrastructure.repositories.sql_rule_repository import SqlRuleRepository

# classes
class Container:
    # initializer
    def __init__(
        self, 
        settings: Config
    ):
        self.settings = settings
        self.engine = None
        self.session_factory = None
        self.decision_repository = None
        self.event_repository = None
        self.rule_repository = None
        self.decision_engine = DecisionEngine()

    # methods
    def build(self):
        self.engine = create_engine(
            database_url = self.settings.database_url, 
            check_same_thread = False if self.settings.database_url == "sqlite:///:memory:" else True, 
            staticpool = True if self.settings.database_url == "sqlite:///:memory:" else False
        )
        self.session_factory = create_session(engine = self.engine)
        self.decision_repository = InMemoryDecisionRepository() if self.settings.database_url == "sqlite:///:memory:" else SqlDecisionRepository(session = fastapi.Depends(self.get_session))
        self.event_repository = InMemoryEventRepository() if self.settings.database_url == "sqlite:///:memory:" else SqlDecisionRepository(session = fastapi.Depends(self.get_session))
        self.rule_repository = InMemoryRuleRepository() if self.settings.database_url == "sqlite:///:memory:" else SqlDecisionRepository(session = fastapi.Depends(self.get_session))

    def get_session(self):
        session: sqlalchemy.orm.Session = self.session_factory()

        try:
            yield session
            
            session.commit()
        except:
            session.rollback()
            
            raise
        finally:
            session.close()

# functions

# get_produce_decision_use_case
def get_produce_decision_use_case(
    decision_repository: DecisionRepositoryContract = fastapi.Depends(get_decision_repository), 
    event_repository: EventRepositoryContract = fastapi.Depends(get_event_repository), 
    rule_repository: RuleRepositoryContract = fastapi.Depends(get_rule_repository), 
    decision_engine: DecisionEngine = decision_engine
) -> ProduceDecisionUseCase:
    return ProduceDecisionUseCase(
        decision_repository = decision_repository, 
        event_repository = event_repository,
        rule_repository = rule_repository,
        decision_engine = decision_engine
    )

# get_register_event_use_case
def get_register_event_use_case(event_repository = fastapi.Depends(get_event_repository)) -> RegisterEventUseCase:
    return RegisterEventUseCase(event_repository = event_repository)

# get_register_rule_use_case
def get_register_rule_use_case(rule_repository = fastapi.Depends(get_rule_repository)) -> RegisterRuleUseCase:
    return RegisterRuleUseCase(rule_repository = rule_repository)
