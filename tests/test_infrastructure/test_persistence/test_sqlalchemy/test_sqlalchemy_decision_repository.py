from collections.abc import Callable

import pytest

from app.domain.entities.decision import Decision
from app.domain.entities.event import Event
from app.domain.entities.rule import Rule
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
def decision_with_scenario(
    decision_factory: Callable[..., Decision],
    event_factory: Callable[..., Event],
    rule_factory: Callable[..., Rule],
    sqlalchemy_event_repo: SQLAlchemyEventRepository,
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> Decision:
    event = event_factory()
    rule = rule_factory()
    decision = decision_factory(event=event, rules=[rule])

    sqlalchemy_event_repo.save(event=event)
    sqlalchemy_rule_repo.save(rule=rule)

    return decision


# VALID CASES


def test_sql_decision_repository_returns_saved_decision(
    decision_with_scenario: Decision,
    sqlalchemy_decision_repo: SQLAlchemyDecisionRepository,
) -> None:
    saved = sqlalchemy_decision_repo.save(decision=decision_with_scenario)

    assert saved is decision_with_scenario


def test_sql_decision_repository_returns_decision_when_id_exists(
    decision_with_scenario: Decision,
    sqlalchemy_decision_repo: SQLAlchemyDecisionRepository,
) -> None:
    sqlalchemy_decision_repo.save(decision=decision_with_scenario)

    returned = sqlalchemy_decision_repo.get_by_id(
        decision_id=decision_with_scenario.id
    )

    assert returned

    assert returned == decision_with_scenario

    assert returned.is_structurally_equal(other=decision_with_scenario)


def test_sql_decision_repository_returns_none_when_id_does_not_exist(
    decision_with_scenario: Decision,
    sqlalchemy_decision_repo: SQLAlchemyDecisionRepository,
) -> None:
    returned = sqlalchemy_decision_repo.get_by_id(
        decision_id=decision_with_scenario.id
    )

    assert returned is None


def test_sql_decision_repository_returns_true_when_decision_is_deleted(
    decision_with_scenario: Decision,
    sqlalchemy_decision_repo: SQLAlchemyDecisionRepository,
) -> None:
    sqlalchemy_decision_repo.save(decision=decision_with_scenario)

    it_was_deleted = sqlalchemy_decision_repo.delete(
        decision=decision_with_scenario
    )

    returned = sqlalchemy_decision_repo.get_by_id(
        decision_id=decision_with_scenario.id
    )

    assert it_was_deleted

    assert returned is None


def test_sql_decision_repository_returns_false_when_decision_is_not_deleted(
    decision_with_scenario: Decision,
    sqlalchemy_decision_repo: SQLAlchemyDecisionRepository,
) -> None:
    it_was_deleted = sqlalchemy_decision_repo.delete(
        decision=decision_with_scenario
    )

    assert not it_was_deleted


def test_sql_decision_repository_returns_list_of_decisions(
    decision_with_scenario: Decision,
    sqlalchemy_decision_repo: SQLAlchemyDecisionRepository,
) -> None:
    sqlalchemy_decision_repo.save(decision=decision_with_scenario)

    decisions = sqlalchemy_decision_repo.list_all()

    assert isinstance(decisions, list)

    assert decision_with_scenario in decisions
