from __future__ import annotations

from typing import Optional

import pandas as pd

from app.calculator_config import CalculatorConfig, load_config
from app.calculator_memento import HistoryCaretaker
from app.exceptions import CalculatorError
from app.history import HistoryManager
from app.operations import OperationFactory


class Calculator:
    """
    Facade for the calculator application.

    The Calculator class coordinates the calculator's major
    subsystems and provides a simple interface for the REPL.

    Design Pattern:
        Facade Pattern

    The class hides the details of the following components:

        OperationFactory
            Creates the appropriate operation strategy.

        HistoryManager
            Stores and manages calculation history.

        HistoryCaretaker
            Manages undo and redo states.

        CalculatorConfig
            Stores application configuration.
    """

    def __init__(
        self,
        config: Optional[CalculatorConfig] = None,
        history: Optional[HistoryManager] = None,
    ) -> None:
        """
        Initialize the calculator.

        Args:
            config:
                Optional calculator configuration. If no
                configuration is provided, the configuration is
                loaded from the environment.

            history:
                Optional HistoryManager. This parameter is useful
                for testing because a test can provide its own
                history manager.
        """

        # Load configuration if one was not provided.
        self.config = config or load_config()

        # Use the provided HistoryManager or create a new one.
        self.history = history or HistoryManager(
            max_history=self.config.max_history,
            filename=self.config.history_file,
        )

        # Create the Memento Pattern caretaker.
        self.caretaker = HistoryCaretaker()

    def calculate(
        self,
        left: float,
        operation: str,
        right: float,
    ) -> float:
        """
        Perform an arithmetic calculation.

        The appropriate operation strategy is created through
        OperationFactory. The calculation is then performed and
        recorded in history.

        Args:
            left:
                The first number.

            operation:
                The arithmetic operation.

            right:
                The second number.

        Returns:
            The result of the calculation.

        Raises:
            CalculatorError:
                If the operation cannot be performed.
        """

        # Save the current state before making a new change.
        self.caretaker.save(self.history.data)

        try:
            # Factory Pattern:
            # Create the correct Strategy object.
            strategy = OperationFactory.create(operation)

            # Strategy Pattern:
            # Execute the selected operation.
            result = strategy.execute(left, right)

            # Add the successful calculation to history.
            self.history.add_calculation(
                left=left,
                operation=operation,
                right=right,
                result=result,
            )

            # Automatically save the history when enabled.
            if self.config.autosave:
                self.history.save()

            return result

        except CalculatorError:
            # If the calculation fails, restore the state that
            # existed before the attempted calculation.
            self.history.data = self.caretaker.undo(
                self.history.data
            )

            raise

    def undo(self) -> bool:
        """
        Undo the most recent calculator change.

        Returns:
            True if an undo was performed.
            False if there is no previous state to restore.
        """

        if not self.caretaker.can_undo:
            return False

        self.history.data = self.caretaker.undo(
            self.history.data
        )

        return True

    def redo(self) -> bool:
        """
        Redo the most recently undone calculator change.

        Returns:
            True if a redo was performed.
            False if there is no state available to restore.
        """

        if not self.caretaker.can_redo:
            return False

        self.history.data = self.caretaker.redo(
            self.history.data
        )

        return True

    def clear_history(self) -> None:
        """
        Clear all calculator history.

        The undo and redo stacks are also cleared because the
        previous calculator states are no longer relevant after
        the history has been cleared.
        """

        self.history.clear()
        self.caretaker.clear()

    def get_history(self) -> pd.DataFrame:
        """
        Return a copy of the calculator history.

        Returns:
            A pandas DataFrame containing the calculation history.
        """

        return self.history.data.copy(deep=True)

    def save_history(self) -> None:
        """
        Save the current calculator history to the configured CSV file.
        """

        self.history.save()

    def load_history(self) -> None:
        """
        Load calculator history from the configured CSV file.

        Loading a new history replaces the current state, so the
        undo and redo stacks are cleared afterward.
        """

        self.history.load()

        # The previous undo/redo states no longer correspond to
        # the newly loaded history.
        self.caretaker.clear()

    def history_count(self) -> int:
        """
        Return the number of calculations currently in history.

        Returns:
            Number of history records.
        """

        return len(self.history.data)

    def can_undo(self) -> bool:
        """
        Determine whether an undo operation is available.

        Returns:
            True if undo is available, otherwise False.
        """

        return self.caretaker.can_undo

    def can_redo(self) -> bool:
        """
        Determine whether a redo operation is available.

        Returns:
            True if redo is available, otherwise False.
        """

        return self.caretaker.can_redo

    def supported_operations(self) -> set[str]:
        """
        Return the operations supported by the calculator.

        Returns:
            A set containing supported operation names and symbols.
        """

        return OperationFactory.names()

