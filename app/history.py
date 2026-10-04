from __future__ import annotations

from pathlib import Path

import pandas as pd

from app.exceptions import InvalidInputError


class HistoryManager:
    """
    Manage calculator history using a pandas DataFrame.

    Each history record contains:

        left
        operation
        right
        result

    Args:
        max_history:
            Maximum number of calculations to keep.

        filename:
            CSV file used for saving and loading history.
    """

    COLUMNS = [
        "left",
        "operation",
        "right",
        "result",
    ]

    def __init__(
        self,
        max_history: int = 100,
        filename: str = "calculator_history.csv",
    ) -> None:
        """
        Initialize the HistoryManager.

        Args:
            max_history:
                Maximum number of records to keep.

            filename:
                File used to save and load calculator history.

        Raises:
            InvalidInputError:
                If max_history is not a positive integer or the
                filename is empty.
        """

        if not isinstance(max_history, int):
            raise InvalidInputError(
                "Maximum history must be an integer."
            )

        if max_history <= 0:
            raise InvalidInputError(
                "Maximum history must be greater than zero."
            )

        if not isinstance(filename, str) or not filename.strip():
            raise InvalidInputError(
                "History filename cannot be empty."
            )

        self.max_history = max_history
        self.filename = filename.strip()

        self._data = pd.DataFrame(columns=self.COLUMNS)

    @property
    def data(self) -> pd.DataFrame:
        """
        Return the current history DataFrame.

        A copy is returned so callers cannot accidentally modify
        the internal DataFrame directly.

        Returns:
            A copy of the calculator history.
        """

        return self._data.copy(deep=True)

    @data.setter
    def data(self, value: pd.DataFrame) -> None:
        """
        Replace the current history DataFrame.

        Args:
            value:
                New history DataFrame.

        Raises:
            InvalidInputError:
                If value is not a pandas DataFrame.
        """

        if not isinstance(value, pd.DataFrame):
            raise InvalidInputError(
                "History data must be a pandas DataFrame."
            )

        self._data = value.copy(deep=True)

    def add_calculation(
        self,
        left: float,
        operation: str,
        right: float,
        result: float,
    ) -> None:
        """
        Add a calculation to the history.

        If the history exceeds the configured maximum size, the
        oldest record is removed.

        Args:
            left:
                First number in the calculation.

            operation:
                Arithmetic operation.

            right:
                Second number in the calculation.

            result:
                Result of the calculation.
        """

        new_record = pd.DataFrame(
            [
                {
                    "left": left,
                    "operation": operation,
                    "right": right,
                    "result": result,
                }
            ]
        )

        self._data = pd.concat(
            [self._data, new_record],
            ignore_index=True,
        )

        if len(self._data) > self.max_history:
            self._data = self._data.tail(
                self.max_history
            ).reset_index(drop=True)

    def save(self, filename: str | None = None) -> None:
        """
        Save calculator history to a CSV file.

        Args:
            filename:
                Optional alternate filename. If omitted, the
                configured filename is used.

        Raises:
            InvalidInputError:
                If the filename is empty.
        """

        target = filename or self.filename

        if not target.strip():
            raise InvalidInputError(
                "History filename cannot be empty."
            )

        path = Path(target)

        # Create the parent directory when a directory is included
        # in the configured path.
        if path.parent != Path("."):
            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

        self._data.to_csv(
            path,
            index=False,
        )

    def load(self, filename: str | None = None) -> None:
        """
        Load calculator history from a CSV file.

        If the file does not exist, an empty history is created.

        Args:
            filename:
                Optional alternate filename. If omitted, the
                configured filename is used.

        Raises:
            InvalidInputError:
                If the CSV file does not contain the expected
                columns.
        """

        target = filename or self.filename
        path = Path(target)

        if not path.exists():
            self._data = pd.DataFrame(
                columns=self.COLUMNS
            )
            return

        loaded_data = pd.read_csv(path)

        missing_columns = [
            column
            for column in self.COLUMNS
            if column not in loaded_data.columns
        ]

        if missing_columns:
            raise InvalidInputError(
                "History file is missing required columns: "
                + ", ".join(missing_columns)
            )

        self._data = loaded_data[
            self.COLUMNS
        ].copy()

        if len(self._data) > self.max_history:
            self._data = self._data.tail(
                self.max_history
            ).reset_index(drop=True)

    def clear(self) -> None:
        """
        Clear all calculator history.
        """

        self._data = pd.DataFrame(
            columns=self.COLUMNS
        )

    def count(self) -> int:
        """
        Return the number of stored calculations.

        Returns:
            Number of calculations currently stored.
        """

        return len(self._data)

    def is_empty(self) -> bool:
        """
        Determine whether the history is empty.

        Returns:
            True if there are no calculations, otherwise False.
        """

        return self._data.empty

    def get_recent(
        self,
        count: int = 5,
    ) -> pd.DataFrame:
        """
        Return the most recent calculations.

        Args:
            count:
                Number of recent calculations to return.

        Returns:
            A DataFrame containing the requested recent records.
        """

        if count <= 0:
            return pd.DataFrame(
                columns=self.COLUMNS
            )

        return self._data.tail(count).copy(
            deep=True
        )

