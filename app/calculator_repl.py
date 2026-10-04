from __future__ import annotations

from typing import Callable, Optional

from app.calculator import Calculator
from app.exceptions import CalculatorError, InvalidInputError
from app.input_validators import (
    is_command,
    validate_command,
    validate_number,
    validate_operation,
)


class CalculatorRepl:
    """
    Provides the interactive command-line interface.

    The REPL communicates with the Calculator Facade instead of
    directly managing calculations, history, or undo/redo logic.
    """

    def __init__(
        self,
        calculator: Optional[Calculator] = None,
    ) -> None:
        """
        Initialize the calculator REPL.

        Args:
            calculator:
                Optional Calculator instance.

                A Calculator can be provided during testing so that
                the REPL can be tested without creating a completely
                new calculator.
        """

        self.calculator = calculator or Calculator()

        self.running = False

        self.commands: dict[str, Callable[[], None]] = {
            "help": self.show_help,
            "history": self.show_history,
            "undo": self.undo,
            "redo": self.redo,
            "clear": self.clear_history,
            "save": self.save_history,
            "load": self.load_history,
            "exit": self.exit,
            "quit": self.exit,
        }

    def run(self) -> None:
        """
        Start the calculator REPL.

        The REPL continues running until the user enters the
        exit or quit command.
        """

        self.running = True

        self.show_welcome()

        while self.running:
            try:
                user_input = self.get_input()

                if not user_input:
                    continue

                if is_command(user_input):
                    command = validate_command(user_input)
                    self.handle_command(command)
                else:
                    self.handle_calculation(user_input)

            except CalculatorError as exc:
                print(f"Error: {exc}")

            except KeyboardInterrupt:
                print("\nCalculator closed.")
                self.running = False

            except EOFError:
                print("\nCalculator closed.")
                self.running = False

    def get_input(self) -> str:
        """
        Get a line of input from the user.

        Returns:
            The user's input with surrounding whitespace removed.
        """

        return input(">>> ").strip()

    def show_welcome(self) -> None:
        """Display the calculator welcome message."""

        print()
        print("=" * 50)
        print("       Professional Python Calculator")
        print("=" * 50)
        print("Type 'help' to see available commands.")
        print("Type 'exit' to close the calculator.")
        print()

    def show_help(self) -> None:
        """Display available calculator commands and operations."""

        print()
        print("Available Commands")
        print("-" * 30)
        print("help     - Show this help message")
        print("history  - Show calculation history")
        print("undo     - Undo the most recent calculation")
        print("redo     - Redo the most recently undone calculation")
        print("clear    - Clear calculation history")
        print("save     - Save history to a CSV file")
        print("load     - Load history from a CSV file")
        print("exit     - Exit the calculator")
        print("quit     - Exit the calculator")

        print()
        print("Available Operations")
        print("-" * 30)
        print("+        - Addition")
        print("-        - Subtraction")
        print("*        - Multiplication")
        print("/        - Division")
        print("^        - Power")
        print("root     - Root")

        print()
        print("Example:")
        print("10 + 5")
        print()

    def handle_command(self, command: str) -> None:
        """
        Execute a calculator command.

        Args:
            command:
                A validated and normalized command.

        Raises:
            InvalidInputError:
                If the command is not supported.
        """

        handler = self.commands.get(command)

        if handler is None:
            raise InvalidInputError(
                f"Unknown command: {command}"
            )

        handler()

    def handle_calculation(self, user_input: str) -> None:
        """
        Process a calculation entered by the user.

        The REPL supports calculations entered in the form:

            number operation number

        Examples:

            10 + 5
            20 / 4
            2 ^ 3
            27 root 3

        Args:
            user_input:
                The complete calculation entered by the user.
        """

        parts = user_input.split()

        if len(parts) != 3:
            raise InvalidInputError(
                "Please enter a calculation in this format: "
                "number operation number"
            )

        left_input, operation_input, right_input = parts

        left = validate_number(left_input)
        operation = validate_operation(operation_input)
        right = validate_number(right_input)

        result = self.calculator.calculate(
            left,
            operation,
            right,
        )

        self.display_result(
            left,
            operation,
            right,
            result,
        )

    def display_result(
        self,
        left: float,
        operation: str,
        right: float,
        result: float,
    ) -> None:
        """
        Display the result of a calculation.

        Args:
            left:
                First number.

            operation:
                Operation performed.

            right:
                Second number.

            result:
                Calculation result.
        """

        print()
        print(f"Result: {left:g} {operation} {right:g} = {result:g}")
        print()

    def show_history(self) -> None:
        """Display the calculator's calculation history."""

        history = self.calculator.get_history()

        if history.empty:
            print()
            print("No calculation history available.")
            print()
            return

        print()
        print("Calculation History")
        print("-" * 70)

        print(history.to_string(index=False))

        print()

    def undo(self) -> None:
        """Undo the most recent calculator calculation."""

        if self.calculator.undo():
            print()
            print("Last calculation undone.")
            print()
        else:
            print()
            print("Nothing to undo.")
            print()

    def redo(self) -> None:
        """Redo the most recently undone calculation."""

        if self.calculator.redo():
            print()
            print("Calculation restored.")
            print()
        else:
            print()
            print("Nothing to redo.")
            print()

    def clear_history(self) -> None:
        """Clear all calculator history."""

        self.calculator.clear_history()

        print()
        print("Calculation history cleared.")
        print()

    def save_history(self) -> None:
        """Save calculator history to the configured CSV file."""

        self.calculator.save_history()

        print()
        print("Calculation history saved.")
        print()

    def load_history(self) -> None:
        """Load calculator history from the configured CSV file."""

        self.calculator.load_history()

        print()
        print("Calculation history loaded.")
        print()

    def exit(self) -> None:
        """Stop the calculator REPL."""

        self.running = False

        print()
        print("Thank you for using the Professional Python Calculator.")
        print()


def main() -> None:
    """
    Start the calculator application.

    This function provides the entry point for launching the REPL.
    """

    repl = CalculatorRepl()
    repl.run()


if __name__ == "__main__":
    main()  # pragma: no cover


