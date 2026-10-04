class CalculatorError(Exception):
    """Base exception for calculator errors."""


class InvalidOperationError(CalculatorError):
    """Raised when an unsupported operation is requested."""


class InvalidInputError(CalculatorError):
    """Raised when user input cannot be converted or validated."""


class DivisionByZeroError(CalculatorError):
    """Raised when division by zero is attempted."""


class ConfigurationError(CalculatorError):
    """Raised when application configuration is invalid."""


class HistoryError(CalculatorError):
    """Raised when calculation history cannot be persisted."""