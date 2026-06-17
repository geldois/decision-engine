from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from decision_engine.domain.entities.decision import Decision
    from decision_engine.infrastructure.persistence.mem.repositories.mem_decision_repository import (  # noqa: E501
        MemDecisionRepository,
    )
    from decision_engine.infrastructure.persistence.mem.repositories.mem_event_repository import (  # noqa: E501
        MemEventRepository,
    )
    from decision_engine.infrastructure.persistence.mem.repositories.mem_rule_repository import (  # noqa: E501
        MemRuleRepository,
    )
    from tests.conftest import MakeDecision, MakeEvent, MakeRule


@pytest.fixture
def decision_with_scenario(
    make_decision: MakeDecision,
    make_event: MakeEvent,
    make_rule: MakeRule,
    mem_event_repo: MemEventRepository,
    mem_rule_repo: MemRuleRepository,
) -> Decision:
    event = make_event()
    rule = make_rule()
    decision = make_decision(event=event, rules=[rule])

    mem_event_repo.save(event=event)
    mem_rule_repo.save(rule=rule)

    return decision


# VALID CASES


def test_mem_decision_repository_returns_saved_decision(
    decision_with_scenario: Decision,
    mem_decision_repo: MemDecisionRepository,
) -> None:
    saved = mem_decision_repo.save(decision=decision_with_scenario)

    assert saved is decision_with_scenario


def test_mem_decision_repository_returns_decision_when_id_exists(
    decision_with_scenario: Decision,
    mem_decision_repo: MemDecisionRepository,
) -> None:
    mem_decision_repo.save(decision=decision_with_scenario)

    returned = mem_decision_repo.get_by_id(decision_id=decision_with_scenario.id)

    assert returned is decision_with_scenario


def test_mem_decision_repository_returns_none_when_id_does_not_exist(
    decision_with_scenario: Decision,
    mem_decision_repo: MemDecisionRepository,
) -> None:
    returned = mem_decision_repo.get_by_id(decision_id=decision_with_scenario.id)

    assert returned is None


def test_mem_decision_repository_returns_true_when_decision_is_deleted(
    decision_with_scenario: Decision,
    mem_decision_repo: MemDecisionRepository,
) -> None:
    mem_decision_repo.save(decision=decision_with_scenario)

    it_was_deleted = mem_decision_repo.delete(decision=decision_with_scenario)

    returned = mem_decision_repo.get_by_id(decision_id=decision_with_scenario.id)

    assert it_was_deleted

    assert returned is None


def test_mem_decision_repository_returns_false_when_decision_is_not_deleted(
    decision_with_scenario: Decision,
    mem_decision_repo: MemDecisionRepository,
) -> None:
    it_was_deleted = mem_decision_repo.delete(decision=decision_with_scenario)

    assert not it_was_deleted


def test_mem_decision_repository_returns_list_of_decisions(
    decision_with_scenario: Decision,
    mem_decision_repo: MemDecisionRepository,
) -> None:
    mem_decision_repo.save(decision=decision_with_scenario)

    decisions = mem_decision_repo.list_all()

    assert isinstance(decisions, list)

    assert decision_with_scenario in decisions
