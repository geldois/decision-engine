from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.repositories.decision_repository_contract import DecisionRepositoryContract
from app.application.repositories.event_repository_contract import EventRepositoryContract
from app.application.repositories.rule_repository_contract import RuleRepositoryContract
from app.application.use_cases.produce_decision_use_case import ProduceDecisionUseCase
from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.database.engine import SessionLocal
from app.infrastructure.repositories.in_memory_decision_repository import InMemoryDecisionRepository
from app.infrastructure.repositories.in_memory_event_repository import InMemoryEventRepository
from app.infrastructure.repositories.in_memory_rule_repository import InMemoryRuleRepository
from app.infrastructure.repositories.sql_decision_repository import SqlDecisionRepository
from app.infrastructure.repositories.sql_event_repository import SqlEventRepository
from app.infrastructure.repositories.sql_rule_repository import SqlRuleRepository

# functions
def get_session():
    session: Session = SessionLocal()

    try:
        yield session
        
        session.commit()
    except:
        session.rollback()
        
        raise
    finally:
        session.close()

def get_decision_repository(session: Session = Depends(get_session)) -> DecisionRepositoryContract:
    return SqlDecisionRepository(session = session)

def get_event_repository(session: Session = Depends(get_session)) -> EventRepositoryContract:
    return SqlEventRepository(session = session)

def get_rule_repository(session: Session = Depends(get_session)) -> RuleRepositoryContract:
    return SqlRuleRepository(session = session)

def get_decision_engine() -> DecisionEngine:
    return DecisionEngine()

# get_produce_decision_use_case
def get_produce_decision_use_case(
    decision_repository = Depends(get_decision_repository), 
    event_repository = Depends(get_event_repository), 
    rule_repository = Depends(get_rule_repository), 
    decision_engine = Depends(get_decision_engine)
) -> ProduceDecisionUseCase:
    return ProduceDecisionUseCase(
        decision_repository = decision_repository, 
        event_repository = event_repository,
        rule_repository = rule_repository,
        decision_engine = decision_engine
    )

# get_register_event_use_case
def get_register_event_use_case(event_repository = Depends(get_event_repository)) -> RegisterEventUseCase:
    return RegisterEventUseCase(event_repository = event_repository)

# get_register_rule_use_case
def get_register_rule_use_case(rule_repository = Depends(get_rule_repository)) -> RegisterRuleUseCase:
    return RegisterRuleUseCase(rule_repository = rule_repository)
