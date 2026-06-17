from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from decision_engine.infrastructure.persistence.sqlalchemy.repositories.sqlalchemy_rule_repository import (  # noqa: E501
        SQLAlchemyRuleRepository,
    )
    from tests.conftest import MakeRule

# VALID CASES


def test_sql_rule_repository_returns_saved_rule(
    make_rule: MakeRule,
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = make_rule()

    saved = sqlalchemy_rule_repo.save(rule=rule)

    assert saved is rule


def test_sql_rule_repository_returns_rule_when_id_exists(
    make_rule: MakeRule,
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = make_rule()

    sqlalchemy_rule_repo.save(rule=rule)

    returned = sqlalchemy_rule_repo.get_by_id(rule_id=rule.id)

    assert returned

    assert returned == rule

    assert returned.is_structurally_equal(other=rule)


def test_sql_rule_repository_returns_none_when_id_does_not_exist(
    make_rule: MakeRule,
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = make_rule()

    returned = sqlalchemy_rule_repo.get_by_id(rule_id=rule.id)

    assert returned is None


def test_sql_rule_repository_returns_true_when_rule_is_deleted(
    make_rule: MakeRule,
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = make_rule()

    sqlalchemy_rule_repo.save(rule=rule)

    it_was_deleted = sqlalchemy_rule_repo.delete(rule=rule)

    returned = sqlalchemy_rule_repo.get_by_id(rule_id=rule.id)

    assert it_was_deleted

    assert returned is None


def test_sql_rule_repository_returns_false_when_rule_is_not_deleted(
    make_rule: MakeRule,
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = make_rule()

    it_was_deleted = sqlalchemy_rule_repo.delete(rule=rule)

    assert not it_was_deleted


def test_sql_rule_repository_returns_list_of_rules(
    make_rule: MakeRule,
    sqlalchemy_rule_repo: SQLAlchemyRuleRepository,
) -> None:
    rule = make_rule()

    sqlalchemy_rule_repo.save(rule=rule)

    rules = sqlalchemy_rule_repo.list_all()

    assert isinstance(rules, list)

    assert rule in rules
