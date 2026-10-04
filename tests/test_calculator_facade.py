import pandas as pd
import pytest

from app.calculator import Calculator
from app.calculator_config import CalculatorConfig
from app.history import HistoryManager


def make_calculator(
    tmp_path,
    autosave=False,
):
    """Create a calculator with isolated test configuration."""
    config = CalculatorConfig(
        history_file=str(
            tmp_path / "history.csv"
        ),
        autosave=autosave,
        max_history=100,
    )

    history = HistoryManager(
        max_history=config.max_history,
        filename=config.history_file,
    )

    return Calculator(
        config=config,
        history=history,
    )


def test_calculator_initialization(tmp_path):
    """Calculator should initialize its components."""
    calculator = make_calculator(tmp_path)

    assert calculator.config is not None
    assert calculator.history is not None
    assert calculator.caretaker is not None


@pytest.mark.parametrize(
    "left,operation,right,expected",
    [
        (10, "+", 5, 15),
        (10, "-", 5, 5),
        (10, "*", 5, 50),
        (10, "/", 5, 2),
        (2, "^", 3, 8),
        (27, "root", 3, 3),
    ],
)
def test_calculate(
    tmp_path,
    left,
    operation,
    right,
    expected,
):
    """Calculator should perform supported calculations."""
    calculator = make_calculator(tmp_path)

    result = calculator.calculate(
        left,
        operation,
        right,
    )

    assert result == pytest.approx(expected)
    assert calculator.history_count() == 1


def test_calculate_saves_history_when_autosave_enabled(
    tmp_path,
):
    """Autosave should write history to the configured file."""
    calculator = make_calculator(
        tmp_path,
        autosave=True,
    )

    calculator.calculate(
        10,
        "+",
        5,
    )

    history_file = tmp_path / "history.csv"

    assert history_file.exists()


def test_get_history(tmp_path):
    """get_history should return calculation history."""
    calculator = make_calculator(tmp_path)

    calculator.calculate(
        10,
        "+",
        5,
    )

    history = calculator.get_history()

    assert isinstance(history, pd.DataFrame)
    assert len(history) == 1
    assert history.iloc[0]["result"] == 15


def test_get_history_returns_copy(tmp_path):
    """get_history should return a copy."""
    calculator = make_calculator(tmp_path)

    calculator.calculate(
        10,
        "+",
        5,
    )

    history = calculator.get_history()

    history.loc[0, "result"] = 999

    assert calculator.get_history().iloc[0]["result"] == 15


def test_undo(tmp_path):
    """Undo should remove the most recent calculation."""
    calculator = make_calculator(tmp_path)

    calculator.calculate(
        10,
        "+",
        5,
    )

    assert calculator.history_count() == 1

    assert calculator.undo() is True

    assert calculator.history_count() == 0


def test_undo_when_unavailable(tmp_path):
    """Undo should return False when unavailable."""
    calculator = make_calculator(tmp_path)

    assert calculator.undo() is False


def test_redo(tmp_path):
    """Redo should restore an undone calculation."""
    calculator = make_calculator(tmp_path)

    calculator.calculate(
        10,
        "+",
        5,
    )

    calculator.undo()

    assert calculator.history_count() == 0

    assert calculator.redo() is True

    assert calculator.history_count() == 1
    assert calculator.get_history().iloc[0]["result"] == 15


def test_redo_when_unavailable(tmp_path):
    """Redo should return False when unavailable."""
    calculator = make_calculator(tmp_path)

    assert calculator.redo() is False


def test_clear_history(tmp_path):
    """Clear should remove history and undo/redo states."""
    calculator = make_calculator(tmp_path)

    calculator.calculate(
        10,
        "+",
        5,
    )

    calculator.clear_history()

    assert calculator.history_count() == 0
    assert calculator.can_undo() is False
    assert calculator.can_redo() is False


def test_save_history(tmp_path):
    """save_history should create the configured CSV file."""
    calculator = make_calculator(tmp_path)

    calculator.calculate(
        10,
        "+",
        5,
    )

    calculator.save_history()

    assert (
        tmp_path / "history.csv"
    ).exists()


def test_load_history(tmp_path):
    """load_history should restore saved calculations."""
    calculator = make_calculator(tmp_path)

    calculator.calculate(
        10,
        "+",
        5,
    )

    calculator.save_history()

    new_calculator = make_calculator(tmp_path)

    new_calculator.load_history()

    assert new_calculator.history_count() == 1
    assert (
        new_calculator.get_history()
        .iloc[0]["result"]
        == 15
    )


def test_load_clears_memento_states(tmp_path):
    """Loading history should clear undo and redo states."""
    calculator = make_calculator(tmp_path)

    calculator.calculate(
        10,
        "+",
        5,
    )

    calculator.save_history()

    calculator.load_history()

    assert calculator.can_undo() is False
    assert calculator.can_redo() is False


def test_supported_operations(tmp_path):
    """Calculator should expose supported operations."""
    calculator = make_calculator(tmp_path)

    operations = calculator.supported_operations()

    assert "+" in operations
    assert "-" in operations
    assert "*" in operations
    assert "/" in operations
    assert "^" in operations
    assert "root" in operations


def test_can_undo_and_redo(tmp_path):
    """Availability checks should reflect calculator state."""
    calculator = make_calculator(tmp_path)

    assert calculator.can_undo() is False
    assert calculator.can_redo() is False

    calculator.calculate(
        10,
        "+",
        5,
    )

    assert calculator.can_undo() is True
    assert calculator.can_redo() is False

    calculator.undo()

    assert calculator.can_undo() is False
    assert calculator.can_redo() is True



def test_calculate_restores_history_when_calculation_fails():
    """A failed calculation should restore the previous history state."""
    calculator = Calculator()

    calculator.calculate(10, "+", 5)

    original_history = calculator.get_history()

    with pytest.raises(Exception):
        calculator.calculate(10, "/", 0)

    restored_history = calculator.get_history()

    assert restored_history.equals(original_history)

