from collections.abc import Callable

from app.domain.entities.rule import Rule
from app.infrastructure.persistence.in_memory.repositories.in_memory_rule_repository import (
    InMemoryRuleRepository,
)

# VALID CASES


def test_in_memory_rule_repository_returns_saved_rule(
    rule_factory: Callable[..., Rule],
    in_memory_rule_repo: InMemoryRuleRepository,
) -> None:
    rule = rule_factory()

    saved = in_memory_rule_repo.save(rule)

    assert saved is rule


def test_in_memory_rule_repository_returns_rule_when_id_exists(
    rule_factory: Callable[..., Rule],
    in_memory_rule_repo: InMemoryRuleRepository,
) -> None:
    rule = rule_factory()

    in_memory_rule_repo.save(rule=rule)

    returned = in_memory_rule_repo.get_by_id(rule_id=rule.id)

    assert returned is rule


def test_in_memory_rule_repository_returns_none_when_id_does_not_exist(
    rule_factory: Callable[..., Rule],
    in_memory_rule_repo: InMemoryRuleRepository,
) -> None:
    rule = rule_factory()

    returned = in_memory_rule_repo.get_by_id(rule_id=rule.id)

    assert not returned


def test_in_memory_rule_repository_returns_true_when_rule_is_deleted(
    rule_factory: Callable[..., Rule],
    in_memory_rule_repo: InMemoryRuleRepository,
) -> None:
    rule = rule_factory()

    in_memory_rule_repo.save(rule=rule)

    it_was_deleted = in_memory_rule_repo.delete(rule=rule)

    returned = in_memory_rule_repo.get_by_id(rule_id=rule.id)

    assert it_was_deleted

    assert returned is None


def test_in_memory_rule_repository_returns_false_when_rule_is_not_deleted(
    rule_factory: Callable[..., Rule],
    in_memory_rule_repo: InMemoryRuleRepository,
) -> None:
    rule = rule_factory()

    it_was_deleted = in_memory_rule_repo.delete(rule=rule)

    assert not it_was_deleted


def test_in_memory_rule_repository_returns_list_of_rules(
    rule_factory: Callable[..., Rule],
    in_memory_rule_repo: InMemoryRuleRepository,
) -> None:
    rule = rule_factory()

    in_memory_rule_repo.save(rule=rule)

    rules = in_memory_rule_repo.list_all()

    assert isinstance(rules, list)

    assert rule in rules
