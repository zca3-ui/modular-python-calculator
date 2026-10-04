import subprocess
import sys
import pandas as pd
import pytest


from app.calculator_repl import CalculatorRepl
from app.exceptions import (
    InvalidInputError,
)


class FakeCalculator:
    """Simple calculator used to isolate REPL tests."""

    def __init__(self):
        self.history = pd.DataFrame(
            columns=[
                "left",
                "operation",
                "right",
                "result",
            ]
        )

        self.undo_available = False
        self.redo_available = False
        self.saved = False
        self.loaded = False
        self.cleared = False

    def calculate(
        self,
        left,
        operation,
        right,
    ):
        """Perform a simple test calculation."""
        if operation == "+":
            result = left + right
        elif operation == "-":
            result = left - right
        elif operation == "*":
            result = left * right
        elif operation == "/":
            result = left / right
        else:
            result = 0

        self.history = pd.concat(
            [
                self.history,
                pd.DataFrame(
                    [
                        {
                            "left": left,
                            "operation": operation,
                            "right": right,
                            "result": result,
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )

        self.undo_available = True

        return result

    def get_history(self):
        """Return a copy of test history."""
        return self.history.copy(deep=True)

    def undo(self):
        """Simulate undo."""
        if not self.undo_available:
            return False

        self.undo_available = False
        self.redo_available = True

        if not self.history.empty:
            self.history = self.history.iloc[:-1].copy()

        return True

    def redo(self):
        """Simulate redo."""
        if not self.redo_available:
            return False

        self.redo_available = True
        return True

    def clear_history(self):
        """Simulate clearing history."""
        self.history = self.history.iloc[0:0].copy()
        self.undo_available = False
        self.redo_available = False
        self.cleared = True

    def save_history(self):
        """Simulate saving history."""
        self.saved = True

    def load_history(self):
        """Simulate loading history."""
        self.loaded = True


def make_repl():
    """Create a REPL using the fake calculator."""
    calculator = FakeCalculator()

    repl = CalculatorRepl(
        calculator=calculator,
    )

    return repl, calculator


def test_repl_initialization():
    """REPL should initialize with a calculator."""
    repl, calculator = make_repl()

    assert repl.calculator is calculator
    assert repl.running is False


def test_show_welcome(capsys):
    """Welcome message should be displayed."""
    repl, _ = make_repl()

    repl.show_welcome()

    output = capsys.readouterr().out

    assert "Professional Python Calculator" in output
    assert "help" in output
    assert "exit" in output


def test_get_input(monkeypatch):
    """get_input should return stripped user input."""
    repl, _ = make_repl()

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "  10 + 5  ",
    )

    assert repl.get_input() == "10 + 5"


def test_handle_calculation(capsys):
    """REPL should process a calculation."""
    repl, calculator = make_repl()

    repl.handle_calculation(
        "10 + 5"
    )

    assert calculator.history.iloc[0]["result"] == 15

    output = capsys.readouterr().out

    assert "Result: 10 + 5 = 15" in output


def test_handle_calculation_invalid_format():
    """Invalid calculation format should raise an error."""
    repl, _ = make_repl()

    with pytest.raises(
        InvalidInputError,
        match="number operation number",
    ):
        repl.handle_calculation(
            "10 +"
        )


def test_handle_calculation_too_many_values():
    """Too many calculation parts should be rejected."""
    repl, _ = make_repl()

    with pytest.raises(InvalidInputError):
        repl.handle_calculation(
            "10 + 5 extra"
        )


def test_handle_command_help(capsys):
    """Help command should display help."""
    repl, _ = make_repl()

    repl.handle_command("help")

    output = capsys.readouterr().out

    assert "Available Commands" in output
    assert "Available Operations" in output


def test_handle_unknown_command():
    """Unknown commands should raise an error."""
    repl, _ = make_repl()

    with pytest.raises(
        InvalidInputError,
        match="Unknown command",
    ):
        repl.handle_command(
            "unknown"
        )


def test_show_empty_history(capsys):
    """Empty history should display an appropriate message."""
    repl, _ = make_repl()

    repl.show_history()

    output = capsys.readouterr().out

    assert "No calculation history available" in output


def test_show_history(capsys):
    """History should be displayed when available."""
    repl, calculator = make_repl()

    calculator.calculate(
        10,
        "+",
        5,
    )

    repl.show_history()

    output = capsys.readouterr().out

    assert "Calculation History" in output
    assert "10" in output
    assert "15" in output


def test_undo_success(capsys):
    """Successful undo should display confirmation."""
    repl, calculator = make_repl()

    calculator.calculate(
        10,
        "+",
        5,
    )

    repl.undo()

    output = capsys.readouterr().out

    assert "Last calculation undone" in output


def test_undo_unavailable(capsys):
    """Unavailable undo should display a message."""
    repl, _ = make_repl()

    repl.undo()

    output = capsys.readouterr().out

    assert "Nothing to undo" in output


def test_redo_unavailable(capsys):
    """Unavailable redo should display a message."""
    repl, _ = make_repl()

    repl.redo()

    output = capsys.readouterr().out

    assert "Nothing to redo" in output


def test_redo_success(capsys):
    """The REPL should display a message when redo succeeds."""
    calculator = FakeCalculator()
    repl = CalculatorRepl(calculator=calculator)

    calculator.undo_available = True
    calculator.undo()

    repl.redo()

    captured = capsys.readouterr()

    assert "Calculation restored." in captured.out




def test_clear_history(capsys):
    """Clear command should clear history."""
    repl, calculator = make_repl()

    calculator.calculate(
        10,
        "+",
        5,
    )

    repl.clear_history()

    assert calculator.cleared is True
    assert calculator.history.empty

    output = capsys.readouterr().out

    assert "history cleared" in output


def test_save_history(capsys):
    """Save command should save history."""
    repl, calculator = make_repl()

    repl.save_history()

    assert calculator.saved is True

    output = capsys.readouterr().out

    assert "history saved" in output


def test_load_history(capsys):
    """Load command should load history."""
    repl, calculator = make_repl()

    repl.load_history()

    assert calculator.loaded is True

    output = capsys.readouterr().out

    assert "history loaded" in output


def test_exit():
    """Exit should stop the REPL."""
    repl, _ = make_repl()

    repl.running = True

    repl.exit()

    assert repl.running is False


def test_commands_dictionary():
    """All required commands should have handlers."""
    repl, _ = make_repl()

    expected_commands = {
        "help",
        "history",
        "undo",
        "redo",
        "clear",
        "save",
        "load",
        "exit",
        "quit",
    }

    assert expected_commands.issubset(
        repl.commands.keys()
    )


def test_handle_command_quit():
    """Quit should use the exit handler."""
    repl, _ = make_repl()

    repl.running = True

    repl.handle_command("quit")

    assert repl.running is False


def test_run_with_calculation_then_exit(
    monkeypatch,
    capsys,
):
    """REPL should process calculations and then exit."""
    repl, calculator = make_repl()

    inputs = iter(
        [
            "10 + 5",
            "exit",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    repl.run()

    assert calculator.history.iloc[0]["result"] == 15
    assert repl.running is False

    output = capsys.readouterr().out

    assert "Result: 10 + 5 = 15" in output


def test_run_handles_empty_input(
    monkeypatch,
):
    """REPL should ignore empty input."""
    repl, _ = make_repl()

    inputs = iter(
        [
            "",
            "exit",
        ]
    )

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    repl.run()

    assert repl.running is False


def test_run_handles_keyboard_interrupt(
    monkeypatch,
    capsys,
):
    """KeyboardInterrupt should close the calculator."""
    repl, _ = make_repl()

    def raise_interrupt(_):
        raise KeyboardInterrupt

    monkeypatch.setattr(
        "builtins.input",
        raise_interrupt,
    )

    repl.run()

    assert repl.running is False

    output = capsys.readouterr().out

    assert "Calculator closed" in output


def test_run_handles_eof(
    monkeypatch,
    capsys,
):
    """EOFError should close the calculator."""
    repl, _ = make_repl()

    def raise_eof(_):
        raise EOFError

    monkeypatch.setattr(
        "builtins.input",
        raise_eof,
    )

    repl.run()

    assert repl.running is False

    output = capsys.readouterr().out

    assert "Calculator closed" in output


def test_run_displays_calculator_error(monkeypatch, capsys):
    """The REPL should display calculator errors to the user."""
    calculator = FakeCalculator()
    repl = CalculatorRepl(calculator=calculator)

    inputs = iter(["10 / 0", "exit"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(inputs),
    )

    def raise_error(_):
        from app.exceptions import DivisionByZeroError

        raise DivisionByZeroError("Cannot divide by zero.")

    monkeypatch.setattr(
        repl,
        "handle_calculation",
        raise_error,
    )

    repl.run()

    captured = capsys.readouterr()

    assert "Error: Cannot divide by zero." in captured.out




def test_main(monkeypatch, capsys):
    """The main function should start the calculator REPL."""
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "exit",
    )

    from app.calculator_repl import main

    main()

    captured = capsys.readouterr()

    assert "Calculator" in captured.out



def test_calculator_repl_module_execution():
    """Running the REPL module directly should execute main."""
    result = subprocess.run(
        [sys.executable, "-m", "app.calculator_repl"],
        input="exit\n",
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.returncode == 0
    assert "Calculator" in result.stdout



