import pytest

from app.exceptions import InvalidInputError
from app.input_validators import (
    is_command,
    is_number,
    validate_command,
    validate_number,
    validate_operation,
    validate_required_inputs,
    validate_root_degree,
)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("10", 10.0),
        ("3.14", 3.14),
        ("-5", -5.0),
        ("  25  ", 25.0),
        ("0", 0.0),
    ],
)
def test_validate_number(value, expected):
    """Valid numeric strings should become floats."""
    assert validate_number(value) == expected


def test_validate_number_empty():
    """Empty input should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="Number input cannot be empty",
    ):
        validate_number("")


def test_validate_number_whitespace():
    """Whitespace-only input should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="Number input cannot be empty",
    ):
        validate_number("   ")


def test_validate_number_invalid():
    """Non-numeric input should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="Invalid number",
    ):
        validate_number("hello")


def test_validate_number_non_string():
    """Non-string number input should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="Number input must be provided as text",
    ):
        validate_number(10)


@pytest.mark.parametrize(
    "operation,expected",
    [
        ("+", "+"),
        (" + ", "+"),
        ("ADD", "add"),
        (" Add ", "add"),
        ("ROOT", "root"),
        (" divide ", "divide"),
    ],
)
def test_validate_operation(operation, expected):
    """Operations should be normalized."""
    assert validate_operation(operation) == expected


def test_validate_operation_empty():
    """Empty operation should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="Operation cannot be empty",
    ):
        validate_operation("")


def test_validate_operation_non_string():
    """Non-string operation should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="Operation must be provided as text",
    ):
        validate_operation(5)


@pytest.mark.parametrize(
    "command,expected",
    [
        ("help", "help"),
        (" HELP ", "help"),
        ("History", "history"),
        ("UNDO", "undo"),
        ("Exit", "exit"),
        ("quit", "quit"),
    ],
)
def test_validate_command(command, expected):
    """Commands should be normalized."""
    assert validate_command(command) == expected


def test_validate_command_empty():
    """Empty commands should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="Command cannot be empty",
    ):
        validate_command("")


def test_validate_command_non_string():
    """Non-string commands should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="Command must be provided as text",
    ):
        validate_command(123)


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2", 2.0),
        ("3", 3.0),
        ("2.5", 2.5),
    ],
)
def test_validate_root_degree(value, expected):
    """Positive root degrees should be accepted."""
    assert validate_root_degree(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "0",
        "-1",
        "-5",
    ],
)
def test_validate_root_degree_invalid(value):
    """Zero and negative root degrees should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="Root degree must be greater than zero",
    ):
        validate_root_degree(value)


def test_validate_required_inputs():
    """All three calculation inputs should be validated."""
    result = validate_required_inputs(
        "10",
        " + ",
        "5",
    )

    assert result == (10.0, "+", 5.0)


def test_validate_required_inputs_invalid_left():
    """Invalid left input should be rejected."""
    with pytest.raises(InvalidInputError):
        validate_required_inputs(
            "hello",
            "+",
            "5",
        )


def test_validate_required_inputs_invalid_operation():
    """Empty operation should be rejected."""
    with pytest.raises(InvalidInputError):
        validate_required_inputs(
            "10",
            "",
            "5",
        )


def test_validate_required_inputs_invalid_right():
    """Invalid right input should be rejected."""
    with pytest.raises(InvalidInputError):
        validate_required_inputs(
            "10",
            "+",
            "hello",
        )


@pytest.mark.parametrize(
    "value",
    [
        "help",
        "history",
        "undo",
        "redo",
        "clear",
        "save",
        "load",
        "exit",
        "quit",
        " HELP ",
    ],
)
def test_is_command_true(value):
    """Supported commands should return True."""
    assert is_command(value) is True


@pytest.mark.parametrize(
    "value",
    [
        "10",
        "hello",
        "+",
        "",
        "unknown",
    ],
)
def test_is_command_false(value):
    """Non-command input should return False."""
    assert is_command(value) is False


def test_is_command_non_string():
    """Non-string input should return False."""
    assert is_command(10) is False


@pytest.mark.parametrize(
    "value",
    [
        "10",
        "3.14",
        "-5",
        " 20 ",
    ],
)
def test_is_number_true(value):
    """Valid numeric strings should return True."""
    assert is_number(value) is True


@pytest.mark.parametrize(
    "value",
    [
        "",
        "hello",
        "abc123",
    ],
)
def test_is_number_false(value):
    """Invalid numeric strings should return False."""
    assert is_number(value) is False


def test_is_number_non_string():
    """Non-string input should return False."""
    assert is_number(10) is False

