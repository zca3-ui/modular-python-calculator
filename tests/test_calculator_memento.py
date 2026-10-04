import pandas as pd

from app.calculator_memento import (
    CalculatorMemento,
    HistoryCaretaker,
)


def make_history(
    values=None,
) -> pd.DataFrame:
    """Create a sample history DataFrame for testing."""
    if values is None:
        values = []

    return pd.DataFrame(
        values,
        columns=[
            "left",
            "operation",
            "right",
            "result",
        ],
    )


def test_memento_restore():
    """Memento should restore a copy of saved history."""
    history = make_history(
        [
            [10, "+", 5, 15],
        ]
    )

    memento = CalculatorMemento(history)

    restored = memento.restore()

    pd.testing.assert_frame_equal(
        restored,
        history,
    )


def test_memento_restore_returns_copy():
    """Restored history should be independent of the original."""
    history = make_history(
        [
            [10, "+", 5, 15],
        ]
    )

    memento = CalculatorMemento(history)

    restored = memento.restore()

    restored.loc[0, "result"] = 999

    assert history.loc[0, "result"] == 15


def test_caretaker_starts_empty():
    """Caretaker should start without undo or redo states."""
    caretaker = HistoryCaretaker()

    assert caretaker.can_undo is False
    assert caretaker.can_redo is False
    assert caretaker.undo_count == 0
    assert caretaker.redo_count == 0


def test_save_creates_undo_state():
    """Saving a history should create an undo state."""
    caretaker = HistoryCaretaker()

    history = make_history(
        [
            [10, "+", 5, 15],
        ]
    )

    caretaker.save(history)

    assert caretaker.can_undo is True
    assert caretaker.undo_count == 1
    assert caretaker.can_redo is False


def test_undo_restores_previous_state():
    """Undo should restore the saved state."""
    caretaker = HistoryCaretaker()

    original = make_history(
        [
            [10, "+", 5, 15],
        ]
    )

    current = make_history(
        [
            [10, "+", 5, 15],
            [20, "-", 5, 15],
        ]
    )

    caretaker.save(original)

    restored = caretaker.undo(current)

    pd.testing.assert_frame_equal(
        restored,
        original,
    )

    assert caretaker.can_redo is True
    assert caretaker.redo_count == 1


def test_undo_without_saved_state():
    """Undo should return the current state when unavailable."""
    caretaker = HistoryCaretaker()

    current = make_history(
        [
            [10, "+", 5, 15],
        ]
    )

    restored = caretaker.undo(current)

    pd.testing.assert_frame_equal(
        restored,
        current,
    )

    assert caretaker.can_undo is False
    assert caretaker.can_redo is False


def test_redo_restores_undone_state():
    """Redo should restore the most recently undone state."""
    caretaker = HistoryCaretaker()

    original = make_history(
        [
            [10, "+", 5, 15],
        ]
    )

    current = make_history(
        [
            [10, "+", 5, 15],
            [20, "-", 5, 15],
        ]
    )

    caretaker.save(original)

    caretaker.undo(current)

    restored = caretaker.redo(original)

    pd.testing.assert_frame_equal(
        restored,
        current,
    )

    assert caretaker.can_undo is True
    assert caretaker.can_redo is False


def test_redo_without_saved_state():
    """Redo should return current state when unavailable."""
    caretaker = HistoryCaretaker()

    current = make_history(
        [
            [10, "+", 5, 15],
        ]
    )

    restored = caretaker.redo(current)

    pd.testing.assert_frame_equal(
        restored,
        current,
    )

    assert caretaker.can_redo is False


def test_save_clears_redo_stack():
    """Saving a new state should invalidate redo history."""
    caretaker = HistoryCaretaker()

    first = make_history(
        [
            [10, "+", 5, 15],
        ]
    )

    second = make_history(
        [
            [10, "+", 5, 15],
            [20, "-", 5, 15],
        ]
    )

    caretaker.save(first)
    caretaker.undo(second)

    assert caretaker.can_redo is True

    caretaker.save(second)

    assert caretaker.can_redo is False


def test_clear():
    """Clear should remove all undo and redo states."""
    caretaker = HistoryCaretaker()

    first = make_history(
        [
            [10, "+", 5, 15],
        ]
    )

    second = make_history(
        [
            [20, "*", 5, 100],
        ]
    )

    caretaker.save(first)
    caretaker.undo(second)

    caretaker.clear()

    assert caretaker.can_undo is False
    assert caretaker.can_redo is False
    assert caretaker.undo_count == 0
    assert caretaker.redo_count == 0

