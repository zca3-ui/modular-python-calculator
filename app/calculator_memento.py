
"""
Provides the Memento Pattern for the calculator application.

The Memento Pattern allows the calculator to save previous states
and restore those states when the user requests undo or redo.

This module contains two classes:

1. CalculatorMemento:
   Stores a snapshot of the calculator's history.

2. HistoryCaretaker:
   Manages the undo and redo stacks.
"""

from dataclasses import dataclass

import pandas as pd


@dataclass
class CalculatorMemento:
    """
    Stores a snapshot of the calculator's state.

    The calculator's history is stored as a pandas DataFrame.
    A copy is used so that future changes to the calculator's
    history do not change the saved snapshot.
    """

    history: pd.DataFrame

    def restore(self) -> pd.DataFrame:
        """
        Restore the saved calculator history.

        Returns:
            A copy of the saved history DataFrame.
        """
        return self.history.copy(deep=True)


class HistoryCaretaker:
    """
    Manages calculator history snapshots.

    The caretaker maintains two stacks:

    - undo_stack: Stores previous calculator states.
    - redo_stack: Stores states that can be restored after an undo.

    This class is responsible for managing snapshots but does not
    perform calculations itself.
    """

    def __init__(self) -> None:
        """Initialize empty undo and redo stacks."""
        self._undo_stack: list[CalculatorMemento] = []
        self._redo_stack: list[CalculatorMemento] = []

    def save(self, history: pd.DataFrame) -> None:
        """
        Save the current calculator state.

        A deep copy is created so that changes to the current history
        do not affect the saved snapshot.

        Saving a new state also clears the redo stack because once a
        new change is made, the previous redo path is no longer valid.

        Args:
            history: The current calculator history.
        """
        memento = CalculatorMemento(
            history.copy(deep=True)
        )

        self._undo_stack.append(memento)

        self._redo_stack.clear()

    def undo(self, current: pd.DataFrame) -> pd.DataFrame:
        """
        Restore the previous calculator state.

        The current state is first placed on the redo stack so that
        the user can restore it later using redo.

        Args:
            current: The calculator's current history.

        Returns:
            The previous calculator history.

        If there is no previous state, the current state is returned.
        """
        if not self._undo_stack:
            return current.copy(deep=True)

        current_memento = CalculatorMemento(
            current.copy(deep=True)
        )

        self._redo_stack.append(current_memento)

        previous_memento = self._undo_stack.pop()

        return previous_memento.restore()

    def redo(self, current: pd.DataFrame) -> pd.DataFrame:
        """
        Restore the most recently undone calculator state.

        The current state is first placed on the undo stack so that
        another undo can be performed later.

        Args:
            current: The calculator's current history.

        Returns:
            The restored calculator history.

        If there is no state available to redo, the current state
        is returned.
        """
        if not self._redo_stack:
            return current.copy(deep=True)

        current_memento = CalculatorMemento(
            current.copy(deep=True)
        )

        self._undo_stack.append(current_memento)

        next_memento = self._redo_stack.pop()

        return next_memento.restore()

    def clear(self) -> None:
        """
        Clear all saved undo and redo states.

        This can be used when the calculator needs to completely
        reset its state.
        """
        self._undo_stack.clear()
        self._redo_stack.clear()

    @property
    def can_undo(self) -> bool:
        """
        Determine whether an undo operation is available.

        Returns:
            True if there is a saved state to undo to,
            otherwise False.
        """
        return bool(self._undo_stack)

    @property
    def can_redo(self) -> bool:
        """
        Determine whether a redo operation is available.

        Returns:
            True if there is a saved state to redo to,
            otherwise False.
        """
        return bool(self._redo_stack)

    @property
    def undo_count(self) -> int:
        """
        Return the number of available undo states.

        Returns:
            Number of states currently stored for undo.
        """
        return len(self._undo_stack)

    @property
    def redo_count(self) -> int:
        """
        Return the number of available redo states.

        Returns:
            Number of states currently stored for redo.
        """
        return len(self._redo_stack)
  