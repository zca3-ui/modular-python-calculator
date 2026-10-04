
"""
Input validation utilities for the calculator application.

This module contains functions for validating and converting
user input before it is passed to the calculator.

Keeping validation in its own module helps keep the REPL and
calculation logic clean and easier to test.
"""

from app.exceptions import InvalidInputError


def validate_number(value: str) -> float:
    """
    Validate and convert a user-provided number.

    This function uses EAFP (Easier to Ask for Forgiveness than
    Permission) by attempting to convert the value to a float
    and handling the error if the conversion fails.

    Args:
        value: User input that should represent a number.

    Returns:
        The input converted to a float.

    Raises:
        InvalidInputError: If the value is empty or cannot be
            converted to a number.
    """

    if not isinstance(value, str):
        raise InvalidInputError(
            "Number input must be provided as text."
        )

    cleaned_value = value.strip()

    if not cleaned_value:
        raise InvalidInputError(
            "Number input cannot be empty."
        )

    try:
        return float(cleaned_value)
    except ValueError as exc:
        raise InvalidInputError(
            f"Invalid number: {value}"
        ) from exc


def validate_operation(operation: str) -> str:
    """
    Validate and normalize a calculator operation.

    Supported operations include:

        +       Addition
        -       Subtraction
        *       Multiplication
        /       Division
        ^       Power
        add     Addition
        subtract
        multiply
        divide
        power
        root

    The operation is converted to lowercase and surrounding
    whitespace is removed.

    Args:
        operation: User-provided operation.

    Returns:
        A normalized operation string.

    Raises:
        InvalidInputError: If the operation is empty or not a string.
    """

    if not isinstance(operation, str):
        raise InvalidInputError(
            "Operation must be provided as text."
        )

    cleaned_operation = operation.strip().lower()

    if not cleaned_operation:
        raise InvalidInputError(
            "Operation cannot be empty."
        )

    return cleaned_operation


def validate_command(command: str) -> str:
    """
    Validate and normalize a calculator command.

    Commands are used by the REPL for actions such as:

        help
        history
        undo
        redo
        clear
        save
        load
        exit

    Args:
        command: User-provided command.

    Returns:
        The normalized command.

    Raises:
        InvalidInputError: If the command is empty or not a string.
    """

    if not isinstance(command, str):
        raise InvalidInputError(
            "Command must be provided as text."
        )

    cleaned_command = command.strip().lower()

    if not cleaned_command:
        raise InvalidInputError(
            "Command cannot be empty."
        )

    return cleaned_command


def validate_root_degree(value: str) -> float:
    """
    Validate a root degree.

    A root degree must be a positive number greater than zero.

    Examples:

        2  -> square root
        3  -> cube root
        4  -> fourth root

    Args:
        value: User input representing the root degree.

    Returns:
        The root degree as a float.

    Raises:
        InvalidInputError: If the root degree is not a valid
            positive number.
    """

    degree = validate_number(value)

    if degree <= 0:
        raise InvalidInputError(
            "Root degree must be greater than zero."
        )

    return degree


def validate_required_inputs(
    left: str,
    operation: str,
    right: str,
) -> tuple[float, str, float]:
    """
    Validate the complete set of inputs needed for a calculation.

    This function combines the individual validation functions
    into one convenient function for the calculator.

    Args:
        left: The first number.
        operation: The arithmetic operation.
        right: The second number.

    Returns:
        A tuple containing:

            (left_number, normalized_operation, right_number)

    Raises:
        InvalidInputError: If any input is invalid.
    """

    left_number = validate_number(left)
    normalized_operation = validate_operation(operation)
    right_number = validate_number(right)

    return (
        left_number,
        normalized_operation,
        right_number,
    )


def is_command(value: str) -> bool:
    """
    Determine whether user input is a calculator command.

    This helper allows the REPL to check whether the user's input
    is a command before attempting to treat it as a calculation.

    Args:
        value: User input.

    Returns:
        True if the input matches a supported command,
        otherwise False.
    """

    if not isinstance(value, str):
        return False

    commands = {
        "help",
        "history",
        "undo",
        "redo",
        "clear",
        "save",
        "load",
        "exit",
        "quit",
    }

    return value.strip().lower() in commands


def is_number(value: str) -> bool:
   
   

    if not isinstance(value, str):
        return False

    try:
        float(value.strip())
        return True
    except ValueError:
        return False

