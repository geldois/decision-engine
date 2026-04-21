from collections.abc import Callable

from app.domain.entities.rule import Rule
from app.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_rule_repository import (
    SQLAlchemyRuleRepository,
)

# VALID CASES


def test_sql_rule_repository_returns_saved_rule(
    rule_factory: Callable[..., Rule],
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = rule_factory()

    saved = sqlalchemy_rule_repo.save(rule=rule)

    assert saved is rule


def test_sql_rule_repository_returns_rule_when_id_exists(
    rule_factory: Callable[..., Rule],
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = rule_factory()

    sqlalchemy_rule_repo.save(rule=rule)

    returned = sqlalchemy_rule_repo.get_by_id(rule_id=rule.id)

    assert returned

    assert returned == rule

    assert returned.is_structurally_equal(other=rule)


def test_sql_rule_repository_returns_none_when_id_does_not_exist(
    rule_factory: Callable[..., Rule],
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = rule_factory()

    returned = sqlalchemy_rule_repo.get_by_id(rule_id=rule.id)

    assert returned is None


def test_sql_rule_repository_returns_true_when_rule_is_deleted(
    rule_factory: Callable[..., Rule],
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = rule_factory()

    sqlalchemy_rule_repo.save(rule=rule)

    it_was_deleted = sqlalchemy_rule_repo.delete(rule=rule)

    returned = sqlalchemy_rule_repo.get_by_id(rule_id=rule.id)

    assert it_was_deleted

    assert returned is None


def test_sql_rule_repository_returns_false_when_rule_is_not_deleted(
    rule_factory: Callable[..., Rule],
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = rule_factory()

    it_was_deleted = sqlalchemy_rule_repo.delete(rule=rule)

    assert not it_was_deleted


def test_sql_rule_repository_returns_list_of_rules(
    rule_factory: Callable[..., Rule],
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = rule_factory()

    sqlalchemy_rule_repo.save(rule=rule)

    rules = sqlalchemy_rule_repo.list_all()

    assert isinstance(rules, list)

    assert rule in rules
