from fastapi import Depends
from sqlalchemy.orm import Session

from app.application.use_cases.register_event_use_case import RegisterEventUseCase
from app.application.use_cases.register_rule_use_case import RegisterRuleUseCase
from app.domain.services.decision_engine import DecisionEngine
from app.infrastructure.database.engine import SessionLocal
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

def get_register_event_use_case(session: Session = Depends(get_session)) -> RegisterEventUseCase:
    event_repository = SqlEventRepository(session)
    rule_repository = SqlRuleRepository(session)
    decision_engine = DecisionEngine()

    return RegisterEventUseCase(
        event_repository = event_repository,
        rule_repository = rule_repository,
        decision_engine = decision_engine
    )

def get_register_rule_use_case(session: Session = Depends(get_session)) -> RegisterRuleUseCase:
    rule_repository = SqlRuleRepository(session)

    return RegisterRuleUseCase(rule_repository = rule_repository)
