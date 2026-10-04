import pytest

from app.calculator_config import (
    CalculatorConfig,
    load_config,
)
from app.exceptions import InvalidInputError


def test_default_configuration(monkeypatch):
    """Default configuration should be used when variables are absent."""
    monkeypatch.delenv(
        "CALCULATOR_HISTORY_FILE",
        raising=False,
    )
    monkeypatch.delenv(
        "CALCULATOR_AUTOSAVE",
        raising=False,
    )
    monkeypatch.delenv(
        "CALCULATOR_MAX_HISTORY",
        raising=False,
    )

    config = CalculatorConfig.from_environment()

    assert config.history_file == "calculator_history.csv"
    assert config.autosave is True
    assert config.max_history == 100


def test_configuration_from_environment(monkeypatch):
    """Environment variables should override defaults."""
    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        "test_history.csv",
    )
    monkeypatch.setenv(
        "CALCULATOR_AUTOSAVE",
        "false",
    )
    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY",
        "25",
    )

    config = CalculatorConfig.from_environment()

    assert config.history_file == "test_history.csv"
    assert config.autosave is False
    assert config.max_history == 25


@pytest.mark.parametrize(
    "value,expected",
    [
        ("true", True),
        ("TRUE", True),
        ("yes", True),
        ("YES", True),
        ("1", True),
        ("on", True),
        ("false", False),
        ("FALSE", False),
        ("no", False),
        ("NO", False),
        ("0", False),
        ("off", False),
    ],
)
def test_parse_boolean(value, expected):
    """Supported Boolean values should be converted correctly."""
    assert CalculatorConfig._parse_boolean(value) is expected


def test_parse_boolean_invalid():
    """Invalid Boolean values should raise an error."""
    with pytest.raises(
        InvalidInputError,
        match="Invalid Boolean configuration value",
    ):
        CalculatorConfig._parse_boolean("maybe")


def test_parse_positive_integer():
    """Positive integer strings should be converted."""
    assert (
        CalculatorConfig._parse_positive_integer(
            "50",
            "TEST_SETTING",
        )
        == 50
    )


@pytest.mark.parametrize(
    "value",
    [
        "abc",
        "",
        "3.5",
    ],
)
def test_parse_positive_integer_invalid(value):
    """Invalid integers should raise an error."""
    with pytest.raises(
        InvalidInputError,
        match="must be an integer",
    ):
        CalculatorConfig._parse_positive_integer(
            value,
            "TEST_SETTING",
        )


@pytest.mark.parametrize(
    "value",
    [
        "0",
        "-1",
        "-100",
    ],
)
def test_parse_positive_integer_non_positive(value):
    """Zero and negative values should be rejected."""
    with pytest.raises(
        InvalidInputError,
        match="must be greater than zero",
    ):
        CalculatorConfig._parse_positive_integer(
            value,
            "TEST_SETTING",
        )


def test_empty_history_file_from_environment(monkeypatch):
    """An empty history filename should be rejected."""
    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        "   ",
    )

    with pytest.raises(
        InvalidInputError,
        match="CALCULATOR_HISTORY_FILE cannot be empty",
    ):
        CalculatorConfig.from_environment()


def test_validate_valid_configuration():
    """A valid configuration should pass validation."""
    config = CalculatorConfig(
        history_file="history.csv",
        autosave=True,
        max_history=100,
    )

    config.validate()


def test_validate_empty_filename():
    """An empty filename should fail validation."""
    config = CalculatorConfig(
        history_file="   ",
        autosave=True,
        max_history=100,
    )

    with pytest.raises(
        InvalidInputError,
        match="History file name cannot be empty",
    ):
        config.validate()


def test_validate_invalid_autosave():
    """Autosave must be Boolean."""
    config = CalculatorConfig(
        history_file="history.csv",
        autosave="yes",
        max_history=100,
    )

    with pytest.raises(
        InvalidInputError,
        match="Autosave must be a Boolean",
    ):
        config.validate()


def test_validate_invalid_max_history_type():
    """Maximum history must be an integer."""
    config = CalculatorConfig(
        history_file="history.csv",
        autosave=True,
        max_history="100",
    )

    with pytest.raises(
        InvalidInputError,
        match="Maximum history must be an integer",
    ):
        config.validate()


def test_validate_invalid_max_history_value():
    """Maximum history must be greater than zero."""
    config = CalculatorConfig(
        history_file="history.csv",
        autosave=True,
        max_history=0,
    )

    with pytest.raises(
        InvalidInputError,
        match="Maximum history must be greater than zero",
    ):
        config.validate()


def test_load_config(monkeypatch):
    """load_config should return a validated configuration."""
    monkeypatch.setenv(
        "CALCULATOR_HISTORY_FILE",
        "history.csv",
    )
    monkeypatch.setenv(
        "CALCULATOR_AUTOSAVE",
        "true",
    )
    monkeypatch.setenv(
        "CALCULATOR_MAX_HISTORY",
        "20",
    )

    config = load_config()

    assert config.history_file == "history.csv"
    assert config.autosave is True
    assert config.max_history == 20

