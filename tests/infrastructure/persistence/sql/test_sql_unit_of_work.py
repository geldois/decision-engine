from sqlalchemy import select

from app.bootstrap.bootstrap import build_dev_session_factory
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.domain.services.decision_engine import DecisionEngine
from app.domain.value_objects.decision_outcome import DecisionOutcome
from app.domain.value_objects.event_field import EventField
from app.domain.value_objects.operators.comparison_operator import ComparisonOperator
from app.infrastructure.database.models.decision_model import DecisionModel
from app.infrastructure.database.models.event_model import EventModel
from app.infrastructure.database.models.rule_model import RuleModel
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


# ==========
# valid cases
# ==========
def test_sql_unit_of_work_commits() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    session_factory = build_dev_session_factory()
    sql_unit_of_work = SqlUnitOfWork(
        session_factory=session_factory,
        decision_repository_factory=SqlDecisionRepository,
        event_repository_factory=SqlEventRepository,
        rule_repository_factory=SqlRuleRepository,
    )
    session = session_factory()

    assert not next(session.execute(select(EventModel).limit(1)), None)

    assert not next(session.execute(select(RuleModel).limit(1)), None)

    assert not next(session.execute(select(DecisionModel).limit(1)), None)

    try:
        with sql_unit_of_work:
            sql_unit_of_work.events.save(event=event)
            sql_unit_of_work.rules.save(rule=rule)
            sql_unit_of_work.decisions.save(decision=decision)
    except Exception:
        pass

    assert (
        session.execute(select(EventModel).where(EventModel.id == event.id))
        .scalars()
        .first()
    )

    assert (
        session.execute(select(RuleModel).where(RuleModel.id == rule.id))
        .scalars()
        .first()
    )

    assert (
        session.execute(select(DecisionModel).where(DecisionModel.id == decision.id))
        .scalars()
        .first()
    )

    session.close()


# ==========
# invalid cases
# ==========
def test_sql_unit_of_work_rolls_back() -> None:
    event = Event(
        event_type="USER_CREATED",
        payload={"user_id": 123, "email": "user@email.com"},
        occurred_at=1700000000,
    )
    rule = Rule(
        name="ALWAYS_APPLIES",
        condition_field=EventField.EVENT_TYPE,
        condition_operator=ComparisonOperator.EQUALS,
        condition_value="USER_CREATED",
        outcome=DecisionOutcome.APPROVED,
        priority=0,
    )
    decision_engine = DecisionEngine()
    decision = decision_engine.decide(event=event, rules=[rule])
    session_factory = build_dev_session_factory()
    sql_unit_of_work = SqlUnitOfWork(
        session_factory=session_factory,
        decision_repository_factory=SqlDecisionRepository,
        event_repository_factory=SqlEventRepository,
        rule_repository_factory=SqlRuleRepository,
    )
    session = session_factory()

    assert not next(session.execute(select(EventModel).limit(1)), None)

    assert not next(session.execute(select(RuleModel).limit(1)), None)

    assert not next(session.execute(select(DecisionModel).limit(1)), None)

    try:
        with sql_unit_of_work:
            sql_unit_of_work.events.save(event=event)
            sql_unit_of_work.rules.save(rule=rule)
            sql_unit_of_work.decisions.save(decision=decision)

            raise Exception
    except Exception:
        pass

    assert not next(session.execute(select(EventModel).limit(1)), None)

    assert not next(session.execute(select(RuleModel).limit(1)), None)

    assert not next(session.execute(select(DecisionModel).limit(1)), None)

    session.close()
