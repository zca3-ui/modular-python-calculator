import pytest

from app.exceptions import (
    DivisionByZeroError,
    InvalidInputError,
    InvalidOperationError,
)
from app.operations import (
    AddStrategy,
    DivideStrategy,
    MultiplyStrategy,
    OperationFactory,
    PowerStrategy,
    RootStrategy,
    SubtractStrategy,
)


def test_add_strategy():
    """Addition strategy should add two numbers."""
    strategy = AddStrategy()

    assert strategy.execute(10, 5) == 15


def test_subtract_strategy():
    """Subtraction strategy should subtract two numbers."""
    strategy = SubtractStrategy()

    assert strategy.execute(10, 5) == 5


def test_multiply_strategy():
    """Multiplication strategy should multiply two numbers."""
    strategy = MultiplyStrategy()

    assert strategy.execute(10, 5) == 50


def test_divide_strategy():
    """Division strategy should divide two numbers."""
    strategy = DivideStrategy()

    assert strategy.execute(10, 5) == 2


def test_divide_by_zero():
    """Division by zero should raise the correct exception."""
    strategy = DivideStrategy()

    with pytest.raises(
        DivisionByZeroError,
        match="Cannot divide by zero",
    ):
        strategy.execute(10, 0)


def test_power_strategy():
    """Power strategy should calculate powers."""
    strategy = PowerStrategy()

    assert strategy.execute(2, 3) == 8


def test_power_with_zero_exponent():
    """Any non-zero number to the zero power should be one."""
    strategy = PowerStrategy()

    assert strategy.execute(10, 0) == 1


def test_power_overflow():
    """Extremely large powers should raise InvalidInputError."""
    strategy = PowerStrategy()

    with pytest.raises(
        InvalidInputError,
        match="Power result is too large",
    ):
        strategy.execute(10.0, 10000)


def test_root_strategy():
    """Root strategy should calculate roots."""
    strategy = RootStrategy()

    assert strategy.execute(27, 3) == pytest.approx(3)


def test_square_root():
    """Root strategy should calculate square roots."""
    strategy = RootStrategy()

    assert strategy.execute(16, 2) == pytest.approx(4)


def test_root_of_negative_with_odd_degree():
    """Odd roots of negative numbers should work."""
    strategy = RootStrategy()

    assert strategy.execute(-8, 3) == pytest.approx(-2)


def test_zero_root_degree():
    """A zero root degree should raise InvalidInputError."""
    strategy = RootStrategy()

    with pytest.raises(
        InvalidInputError,
        match="Root degree cannot be zero",
    ):
        strategy.execute(16, 0)


def test_even_root_of_negative_number():
    """Even roots of negative numbers should be rejected."""
    strategy = RootStrategy()

    with pytest.raises(
        InvalidInputError,
        match="Even root of a negative number",
    ):
        strategy.execute(-16, 2)


@pytest.mark.parametrize(
    "operation,left,right,expected",
    [
        ("+", 5, 3, 8),
        ("add", 5, 3, 8),
        ("-", 5, 3, 2),
        ("subtract", 5, 3, 2),
        ("*", 5, 3, 15),
        ("multiply", 5, 3, 15),
        ("/", 6, 3, 2),
        ("divide", 6, 3, 2),
        ("^", 2, 3, 8),
        ("power", 2, 3, 8),
    ],
)
def test_operation_factory(
    operation,
    left,
    right,
    expected,
):
    """Factory should create the correct strategy."""
    strategy = OperationFactory.create(operation)

    assert strategy.execute(left, right) == expected


def test_operation_factory_root():
    """Factory should create RootStrategy."""
    strategy = OperationFactory.create("root")

    assert isinstance(strategy, RootStrategy)
    assert strategy.execute(27, 3) == pytest.approx(3)


def test_operation_factory_is_case_insensitive():
    """Factory should accept uppercase operation names."""
    strategy = OperationFactory.create("ADD")

    assert isinstance(strategy, AddStrategy)
    assert strategy.execute(2, 3) == 5


def test_operation_factory_strips_whitespace():
    """Factory should remove surrounding whitespace."""
    strategy = OperationFactory.create("  +  ")

    assert isinstance(strategy, AddStrategy)


def test_operation_factory_invalid_operation():
    """Unsupported operations should raise InvalidOperationError."""
    with pytest.raises(
        InvalidOperationError,
        match="Unsupported operation",
    ):
        OperationFactory.create("invalid")


def test_operation_factory_names():
    """Factory should return supported operation names."""
    names = OperationFactory.names()

    assert "+" in names
    assert "-" in names
    assert "*" in names
    assert "/" in names
    assert "^" in names
    assert "root" in names
    assert "add" in names
    assert "subtract" in names
    assert "multiply" in names
    assert "divide" in names
    assert "power" in names

