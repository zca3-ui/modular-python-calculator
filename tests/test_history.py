import pandas as pd
import pytest

from app.exceptions import InvalidInputError
from app.history import HistoryManager


def test_history_manager_defaults():
    """HistoryManager should use its default settings."""
    history = HistoryManager()

    assert history.max_history == 100
    assert history.filename == "calculator_history.csv"
    assert history.is_empty() is True
    assert history.count() == 0


def test_invalid_max_history_type():
    """Maximum history must be an integer."""
    with pytest.raises(
        InvalidInputError,
        match="Maximum history must be an integer",
    ):
        HistoryManager(max_history="100")


def test_invalid_max_history_value():
    """Maximum history must be greater than zero."""
    with pytest.raises(
        InvalidInputError,
        match="Maximum history must be greater than zero",
    ):
        HistoryManager(max_history=0)


def test_empty_filename():
    """Filename cannot be empty."""
    with pytest.raises(
        InvalidInputError,
        match="History filename cannot be empty",
    ):
        HistoryManager(filename="   ")


def test_add_calculation():
    """A calculation should be added to history."""
    history = HistoryManager()

    history.add_calculation(
        10,
        "+",
        5,
        15,
    )

    assert history.count() == 1
    assert history.is_empty() is False

    data = history.data

    assert data.iloc[0]["left"] == 10
    assert data.iloc[0]["operation"] == "+"
    assert data.iloc[0]["right"] == 5
    assert data.iloc[0]["result"] == 15


def test_data_returns_copy():
    """The data property should return a copy."""
    history = HistoryManager()

    history.add_calculation(
        10,
        "+",
        5,
        15,
    )

    data = history.data

    data.loc[0, "result"] = 999

    assert history.data.loc[0, "result"] == 15


def test_data_setter():
    """The data setter should replace history."""
    history = HistoryManager()

    new_data = pd.DataFrame(
        [
            {
                "left": 20,
                "operation": "*",
                "right": 5,
                "result": 100,
            }
        ]
    )

    history.data = new_data

    pd.testing.assert_frame_equal(
        history.data,
        new_data,
    )


def test_data_setter_invalid():
    """The data setter should reject non-DataFrame values."""
    history = HistoryManager()

    with pytest.raises(
        InvalidInputError,
        match="History data must be a pandas DataFrame",
    ):
        history.data = "invalid"


def test_max_history():
    """Old records should be removed when the limit is exceeded."""
    history = HistoryManager(max_history=2)

    history.add_calculation(1, "+", 1, 2)
    history.add_calculation(2, "+", 2, 4)
    history.add_calculation(3, "+", 3, 6)

    assert history.count() == 2

    data = history.data

    assert data.iloc[0]["left"] == 2
    assert data.iloc[1]["left"] == 3


def test_save_and_load(tmp_path):
    """History should persist correctly through CSV."""
    filename = tmp_path / "history.csv"

    history = HistoryManager(
        filename=str(filename),
    )

    history.add_calculation(
        10,
        "+",
        5,
        15,
    )

    history.save()

    loaded = HistoryManager(
        filename=str(filename),
    )

    loaded.load()

    assert loaded.count() == 1

    assert loaded.data.iloc[0]["left"] == 10
    assert loaded.data.iloc[0]["operation"] == "+"
    assert loaded.data.iloc[0]["right"] == 5
    assert loaded.data.iloc[0]["result"] == 15


def test_save_with_alternate_filename(tmp_path):
    """An alternate filename should be accepted by save."""
    default_file = tmp_path / "default.csv"
    alternate_file = tmp_path / "alternate.csv"

    history = HistoryManager(
        filename=str(default_file),
    )

    history.add_calculation(
        2,
        "*",
        3,
        6,
    )

    history.save(str(alternate_file))

    assert alternate_file.exists()
    assert not default_file.exists()


def test_load_with_alternate_filename(tmp_path):
    """An alternate filename should be accepted by load."""
    filename = tmp_path / "history.csv"

    data = pd.DataFrame(
        [
            {
                "left": 4,
                "operation": "+",
                "right": 6,
                "result": 10,
            }
        ]
    )

    data.to_csv(
        filename,
        index=False,
    )

    history = HistoryManager()

    history.load(str(filename))

    assert history.count() == 1
    assert history.data.iloc[0]["result"] == 10


def test_load_missing_file(tmp_path):
    """Loading a nonexistent file should create empty history."""
    filename = tmp_path / "missing.csv"

    history = HistoryManager(
        filename=str(filename),
    )

    history.add_calculation(
        10,
        "+",
        5,
        15,
    )

    history.load()

    assert history.is_empty() is True


def test_load_missing_columns(tmp_path):
    """Invalid CSV files should raise an error."""
    filename = tmp_path / "invalid.csv"

    invalid_data = pd.DataFrame(
        [
            {
                "wrong_column": 10,
            }
        ]
    )

    invalid_data.to_csv(
        filename,
        index=False,
    )

    history = HistoryManager(
        filename=str(filename),
    )

    with pytest.raises(
        InvalidInputError,
        match="History file is missing required columns",
    ):
        history.load()


def test_clear():
    """Clear should remove all history."""
    history = HistoryManager()

    history.add_calculation(
        10,
        "+",
        5,
        15,
    )

    history.clear()

    assert history.is_empty() is True
    assert history.count() == 0


def test_get_recent():
    """get_recent should return the requested records."""
    history = HistoryManager()

    history.add_calculation(1, "+", 1, 2)
    history.add_calculation(2, "+", 2, 4)
    history.add_calculation(3, "+", 3, 6)

    recent = history.get_recent(2)

    assert len(recent) == 2
    assert recent.iloc[0]["left"] == 2
    assert recent.iloc[1]["left"] == 3


def test_get_recent_zero():
    """A non-positive recent count should return empty history."""
    history = HistoryManager()

    history.add_calculation(
        10,
        "+",
        5,
        15,
    )

    recent = history.get_recent(0)

    assert recent.empty is True


def test_get_recent_negative():
    """Negative recent count should return empty history."""
    history = HistoryManager()

    recent = history.get_recent(-1)

    assert recent.empty is True



def test_save_empty_filename_raises_error():
    """An empty filename should raise an error."""
    with pytest.raises(InvalidInputError):
        HistoryManager(filename="")




def test_save_creates_parent_directory(tmp_path):
    """Saving to a nested path should create the parent directory."""
    filename = tmp_path / "history" / "calculator.csv"

    history = HistoryManager(
        filename=str(filename),
    )

    history.add_calculation(
        10,
        "+",
        5,
        15,
    )

    history.save()

    assert filename.exists()


def test_load_trims_history_to_max_history(tmp_path):
    """Loading history should respect the maximum history size."""
    filename = tmp_path / "calculator.csv"

    history = HistoryManager(
        max_history=2,
        filename=str(filename),
    )

    history.add_calculation(1, "+", 1, 2)
    history.add_calculation(2, "+", 2, 4)
    history.add_calculation(3, "+", 3, 6)

    history.save()

    loaded_history = HistoryManager(
        max_history=2,
        filename=str(filename),
    )

    loaded_history.load()

    assert loaded_history.count() == 2
    assert loaded_history.data.iloc[0]["left"] == 2
    assert loaded_history.data.iloc[1]["left"] == 3


def test_save_whitespace_filename_raises_error():
    """A whitespace-only filename should raise an error."""
    history = HistoryManager()

    with pytest.raises(InvalidInputError):
        history.save(" ")



def test_load_trims_history_to_max_history(tmp_path):
    """Loading history should keep only the newest records."""
    filename = tmp_path / "history.csv"

    history = HistoryManager(
        max_history=2,
        filename=str(filename),
    )

    history.data = pd.DataFrame(
        [
            {
                "left": 1,
                "operation": "+",
                "right": 2,
                "result": 3,
            },
            {
                "left": 2,
                "operation": "+",
                "right": 3,
                "result": 5,
            },
            {
                "left": 3,
                "operation": "+",
                "right": 4,
                "result": 7,
            },
        ]
    )

    history.save()

    loaded_history = HistoryManager(
        max_history=2,
        filename=str(filename),
    )

    loaded_history.load()

    assert len(loaded_history.data) == 2
    assert loaded_history.data.iloc[0]["result"] == 5
    assert loaded_history.data.iloc[1]["result"] == 7
