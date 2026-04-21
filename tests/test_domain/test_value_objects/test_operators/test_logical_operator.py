from app.domain.value_objects.operators.logical_operator import LogicalOperator

# VALID CASES


def test_logical_operator_and_returns_valid_bool() -> None:
    operator = LogicalOperator.AND

    assert operator.evaluate(conditions=[True])

    assert operator.evaluate(conditions=[True, True])

    assert not operator.evaluate(conditions=[False])

    assert not operator.evaluate(conditions=[False, False])

    assert not operator.evaluate(conditions=[True, False])


def test_logical_operator_or_returns_valid_bool() -> None:
    operator = LogicalOperator.OR

    assert operator.evaluate(conditions=[True])

    assert operator.evaluate(conditions=[True, True])

    assert operator.evaluate(conditions=[True, False])

    assert not operator.evaluate(conditions=[False])

    assert not operator.evaluate(conditions=[False, False])
