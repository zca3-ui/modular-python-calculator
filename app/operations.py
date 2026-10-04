
"""
Provides arithmetic operation strategies and an operation factory.

This module uses:
- Strategy Pattern: Each arithmetic operation has its own strategy class.
- Factory Pattern: OperationFactory creates the correct strategy based
  on the operation selected by the user.
"""

from abc import ABC, abstractmethod

from app.exceptions import (
    DivisionByZeroError,
    InvalidInputError,
    InvalidOperationError,
)


class OperationStrategy(ABC):
    """Base class for all calculator operation strategies."""

    @abstractmethod
    def execute(self, left: float, right: float) -> float:
        """
        Execute an arithmetic operation.

        Args:
            left: The first number.
            right: The second number.

        Returns:
            The result of the arithmetic operation.
        """
        raise NotImplementedError  # pragma: no cover


class AddStrategy(OperationStrategy):
    """Strategy for addition."""

    def execute(self, left: float, right: float) -> float:
        """Return the sum of two numbers."""
        return left + right


class SubtractStrategy(OperationStrategy):
    """Strategy for subtraction."""

    def execute(self, left: float, right: float) -> float:
        """Return the difference between two numbers."""
        return left - right


class MultiplyStrategy(OperationStrategy):
    """Strategy for multiplication."""

    def execute(self, left: float, right: float) -> float:
        """Return the product of two numbers."""
        return left * right


class DivideStrategy(OperationStrategy):
    """Strategy for division."""

    def execute(self, left: float, right: float) -> float:
        """
        Divide the first number by the second number.

        Raises:
            DivisionByZeroError: If the second number is zero.
        """
        # LBYL: Check for division by zero before performing division.
        if right == 0:
            raise DivisionByZeroError(
                "Cannot divide by zero."
            )

        return left / right


class PowerStrategy(OperationStrategy):
    """Strategy for exponentiation."""

    def execute(self, left: float, right: float) -> float:
        """
        Raise the first number to the power of the second number.

        Raises:
            InvalidInputError: If the calculation causes an overflow.
        """
        # EAFP: Attempt the operation and handle an error if it occurs.
        try:
            return left ** right
        except OverflowError as exc:
            raise InvalidInputError(
                "Power result is too large."
            ) from exc


class RootStrategy(OperationStrategy):
    """Strategy for calculating roots."""

    def execute(self, left: float, right: float) -> float:
        """
        Calculate the right-th root of the left number.

        Examples:
            27 root 3 = 3
            16 root 2 = 4

        Raises:
            InvalidInputError: If the root degree is zero or if an
                even root of a negative number is requested.
        """
        # A root degree of zero is invalid.
        if right == 0:
            raise InvalidInputError(
                "Root degree cannot be zero."
            )

        # Even roots of negative numbers are not real numbers.
        if left < 0 and right % 2 == 0:
            raise InvalidInputError(
                "Even root of a negative number is not real."
            )

        # Handle negative numbers with odd roots.
        if left < 0:
            return -((-left) ** (1 / right))

        return left ** (1 / right)


class OperationFactory:
    """
    Factory for creating arithmetic operation strategies.

    The Factory Pattern allows the application to create the correct
    operation strategy without directly creating individual strategy
    objects throughout the application.
    """

    _strategies = {
        "+": AddStrategy,
        "add": AddStrategy,

        "-": SubtractStrategy,
        "subtract": SubtractStrategy,

        "*": MultiplyStrategy,
        "multiply": MultiplyStrategy,

        "/": DivideStrategy,
        "divide": DivideStrategy,

        "^": PowerStrategy,
        "power": PowerStrategy,

        "root": RootStrategy,
    }

    @classmethod
    def create(cls, operation: str) -> OperationStrategy:
        """
        Create an operation strategy based on user input.

        Args:
            operation: The operation name or symbol.

        Returns:
            An instance of the appropriate operation strategy.

        Raises:
            InvalidOperationError: If the operation is not supported.
        """
        normalized = operation.strip().lower()

        strategy_class = cls._strategies.get(normalized)

        if strategy_class is None:
            raise InvalidOperationError(
                f"Unsupported operation: {operation}"
            )

        return strategy_class()

    @classmethod
    def names(cls) -> set[str]:
        """
        Return all supported operation names and symbols.

        Returns:
            A set containing the supported operations.
        """
        return set(cls._strategies.keys())

