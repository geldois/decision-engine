from collections.abc import Callable

from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
from app.infrastructure.persistence.sqlalchemy.sqlalchemy_unit_of_work import (
    SQLAlchemyUnitOfWork,
)

# VALID CASES


def test_sqlalchemy_unit_of_work_commits(
    decision_factory: Callable[..., Decision],
    event_factory: Callable[..., Event],
    rule_factory: Callable[..., Rule],
    sqlalchemy_uow_factory: Callable[[], SQLAlchemyUnitOfWork],
) -> None:
    event = event_factory()
    rule = rule_factory()
    decision = decision_factory(event=event, rules=[rule])

    with sqlalchemy_uow_factory() as uow:
        uow.events.save(event=event)
        uow.rules.save(rule=rule)
        uow.decisions.save(decision=decision)

    with sqlalchemy_uow_factory() as uow:
        assert uow.decisions.get_by_id(decision_id=decision.id)
        assert uow.events.get_by_id(event_id=event.id)
        assert uow.rules.get_by_id(rule_id=rule.id)


# INVALID CASES


def test_sqlalchemy_unit_of_work_rolls_back(
    decision_factory: Callable[..., Decision],
    event_factory: Callable[..., Event],
    rule_factory: Callable[..., Rule],
    sqlalchemy_uow_factory: Callable[[], SQLAlchemyUnitOfWork],
) -> None:
    event = event_factory()
    rule = rule_factory()
    decision = decision_factory(event=event, rules=[rule])

    try:
        with sqlalchemy_uow_factory() as uow:
            uow.events.save(event=event)
            uow.rules.save(rule=rule)
            uow.decisions.save(decision=decision)

            raise Exception
    except Exception:
        pass

    with sqlalchemy_uow_factory() as uow:
        assert uow.decisions.get_by_id(decision_id=decision.id) is None
        assert uow.events.get_by_id(event_id=event.id) is None
        assert uow.rules.get_by_id(rule_id=rule.id) is None
