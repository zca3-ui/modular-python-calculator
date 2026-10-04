from datetime import datetime

import pytest

from app.calculation import Calculation


def test_calculation_creation():
    """A Calculation object should store all calculation values."""
    calculation = Calculation(
        left=10.0,
        operation="+",
        right=5.0,
        result=15.0,
        timestamp="2026-01-01T12:00:00+00:00",
    )

    assert calculation.left == 10.0
    assert calculation.operation == "+"
    assert calculation.right == 5.0
    assert calculation.result == 15.0
    assert (
        calculation.timestamp
        == "2026-01-01T12:00:00+00:00"
    )


def test_calculation_create():
    """The create method should create a Calculation with a timestamp."""
    calculation = Calculation.create(
        10.0,
        "+",
        5.0,
        15.0,
    )

    assert calculation.left == 10.0
    assert calculation.operation == "+"
    assert calculation.right == 5.0
    assert calculation.result == 15.0

    # Verify that the timestamp can be converted into a datetime.
    timestamp = datetime.fromisoformat(
        calculation.timestamp
    )

    assert timestamp.tzinfo is not None


@pytest.mark.parametrize(
    "left,operation,right,result",
    [
        (10.0, "+", 5.0, 15.0),
        (10.0, "-", 5.0, 5.0),
        (10.0, "*", 5.0, 50.0),
        (10.0, "/", 5.0, 2.0),
        (2.0, "^", 3.0, 8.0),
        (27.0, "root", 3.0, 3.0),
    ],
)
def test_calculation_create_for_operations(
    left,
    operation,
    right,
    result,
):
    """Calculation.create should work for all supported operations."""
    calculation = Calculation.create(
        left,
        operation,
        right,
        result,
    )

    assert calculation.left == left
    assert calculation.operation == operation
    assert calculation.right == right
    assert calculation.result == result
    assert calculation.timestamp


def test_calculation_is_frozen():
    """Calculation objects should be immutable."""
    calculation = Calculation(
        left=10.0,
        operation="+",
        right=5.0,
        result=15.0,
        timestamp="2026-01-01T12:00:00+00:00",
    )

    with pytest.raises(
        AttributeError,
    ):
        calculation.result = 100.0


def test_calculation_is_dataclass():
    """Calculation should behave as a dataclass."""
    calculation = Calculation(
        left=10.0,
        operation="+",
        right=5.0,
        result=15.0,
        timestamp="2026-01-01T12:00:00+00:00",
    )

    assert hasattr(calculation, "__dataclass_fields__")


def test_create_generates_different_timestamps():
    """Separate calculations should receive timestamps."""
    first = Calculation.create(
        1.0,
        "+",
        1.0,
        2.0,
    )

    second = Calculation.create(
        2.0,
        "+",
        2.0,
        4.0,
    )

    assert first.timestamp
    assert second.timestamp

    first_time = datetime.fromisoformat(
        first.timestamp
    )

    second_time = datetime.fromisoformat(
        second.timestamp
    )

    assert first_time.tzinfo is not None
    assert second_time.tzinfo is not None


def test_calculation_equality():
    """Calculations with identical values should be equal."""
    timestamp = "2026-01-01T12:00:00+00:00"

    first = Calculation(
        left=10.0,
        operation="+",
        right=5.0,
        result=15.0,
        timestamp=timestamp,
    )

    second = Calculation(
        left=10.0,
        operation="+",
        right=5.0,
        result=15.0,
        timestamp=timestamp,
    )

    assert first == second

