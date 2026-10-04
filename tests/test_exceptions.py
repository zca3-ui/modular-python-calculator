import pytest

from app.exceptions import (
    CalculatorError,
    DivisionByZeroError,
    InvalidInputError,
    InvalidOperationError,
)


def test_calculator_error_is_exception():
    """CalculatorError should inherit from Exception."""
    error = CalculatorError("Test error")

    assert isinstance(error, Exception)
    assert str(error) == "Test error"


def test_invalid_operation_error():
    """InvalidOperationError should inherit from CalculatorError."""
    error = InvalidOperationError("Invalid operation")

    assert isinstance(error, CalculatorError)
    assert str(error) == "Invalid operation"


def test_invalid_input_error():
    """InvalidInputError should inherit from CalculatorError."""
    error = InvalidInputError("Invalid input")

    assert isinstance(error, CalculatorError)
    assert str(error) == "Invalid input"


def test_division_by_zero_error():
    """DivisionByZeroError should inherit from CalculatorError."""
    error = DivisionByZeroError("Cannot divide by zero.")

    assert isinstance(error, CalculatorError)
    assert str(error) == "Cannot divide by zero."


def test_exception_classes_can_be_raised():
    """All custom exceptions should be raisable."""
    with pytest.raises(InvalidOperationError):
        raise InvalidOperationError("Invalid operation")

    with pytest.raises(InvalidInputError):
        raise InvalidInputError("Invalid input")

    with pytest.raises(DivisionByZeroError):
        raise DivisionByZeroError("Division by zero")

