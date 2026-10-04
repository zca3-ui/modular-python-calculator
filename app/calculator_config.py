
"""
Configuration management for the calculator application.

This module loads calculator settings from environment variables
and an optional .env file.

The configuration is centralized in one class so that the rest
of the application does not need to repeatedly read environment
variables.

Environment variables supported:

- CALCULATOR_HISTORY_FILE:
    Name/path of the CSV file used to save calculator history.

- CALCULATOR_AUTOSAVE:
    Whether calculator history should be automatically saved.
    Accepted values: true, false, yes, no, 1, 0, on, off.

- CALCULATOR_MAX_HISTORY:
    Maximum number of history records to keep.

Example .env file:

CALCULATOR_HISTORY_FILE=calculator_history.csv
CALCULATOR_AUTOSAVE=true
CALCULATOR_MAX_HISTORY=100
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from app.exceptions import InvalidInputError


# Load variables from a .env file if one exists.
load_dotenv()


@dataclass
class CalculatorConfig:
    """
    Stores validated calculator configuration settings.

    Using a dataclass makes it easy to group related configuration
    values into one object.
    """

    history_file: str = "calculator_history.csv"
    autosave: bool = True
    max_history: int = 100

    @classmethod
    def from_environment(cls) -> "CalculatorConfig":
        """
        Create a CalculatorConfig using environment variables.

        If an environment variable is not provided, the default
        value defined by the class is used.

        Returns:
            A validated CalculatorConfig object.

        Raises:
            InvalidInputError: If an environment variable contains
                an invalid value.
        """

        history_file = os.getenv(
            "CALCULATOR_HISTORY_FILE",
            "calculator_history.csv",
        )

        autosave_value = os.getenv(
            "CALCULATOR_AUTOSAVE",
            "true",
        )

        max_history_value = os.getenv(
            "CALCULATOR_MAX_HISTORY",
            "100",
        )

        autosave = cls._parse_boolean(autosave_value)
        max_history = cls._parse_positive_integer(
            max_history_value,
            "CALCULATOR_MAX_HISTORY",
        )

        if not history_file.strip():
            raise InvalidInputError(
                "CALCULATOR_HISTORY_FILE cannot be empty."
            )

        return cls(
            history_file=history_file.strip(),
            autosave=autosave,
            max_history=max_history,
        )

    @staticmethod
    def _parse_boolean(value: str) -> bool:
        """
        Convert a string environment value into a Boolean.

        Accepted true values:
            true, yes, 1, on

        Accepted false values:
            false, no, 0, off

        Args:
            value: The environment variable value.

        Returns:
            True or False.

        Raises:
            InvalidInputError: If the value cannot be interpreted
                as a Boolean.
        """

        normalized = value.strip().lower()

        true_values = {"true", "yes", "1", "on"}
        false_values = {"false", "no", "0", "off"}

        if normalized in true_values:
            return True

        if normalized in false_values:
            return False

        raise InvalidInputError(
            f"Invalid Boolean configuration value: {value}"
        )

    @staticmethod
    def _parse_positive_integer(
        value: str,
        setting_name: str,
    ) -> int:
        """
        Convert a string into a positive integer.

        Args:
            value: The value that should contain an integer.
            setting_name: The name of the configuration setting.

        Returns:
            A positive integer.

        Raises:
            InvalidInputError: If the value is not a valid positive
                integer.
        """

        try:
            number = int(value)
        except (TypeError, ValueError) as exc:
            raise InvalidInputError(
                f"{setting_name} must be an integer."
            ) from exc

        if number <= 0:
            raise InvalidInputError(
                f"{setting_name} must be greater than zero."
            )

        return number

    def validate(self) -> None:
        """
        Validate the current configuration.

        This method provides an additional validation step that can
        be called after the configuration object is created.

        Raises:
            InvalidInputError: If any configuration value is invalid.
        """

        if not self.history_file.strip():
            raise InvalidInputError(
                "History file name cannot be empty."
            )

        if not isinstance(self.autosave, bool):
            raise InvalidInputError(
                "Autosave must be a Boolean value."
            )

        if not isinstance(self.max_history, int):
            raise InvalidInputError(
                "Maximum history must be an integer."
            )

        if self.max_history <= 0:
            raise InvalidInputError(
                "Maximum history must be greater than zero."
            )


def load_config() -> CalculatorConfig:
    """
    Load and validate the calculator configuration.

    This function provides a simple way for the rest of the
    application to obtain configuration settings.

    Returns:
        A validated CalculatorConfig object.

    Raises:
        InvalidInputError: If the environment configuration is invalid.
    """

    config = CalculatorConfig.from_environment()
    config.validate()

    return config

