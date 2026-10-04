Repository Setup:

Initialize a new Git repository locally and create a corresponding repository on GitHub.
Set up a Python project in your preferred IDE with a well-structured directory layout, following the provided flat folder structure (app/calculator_repl.py, app/calculation.py, app/calculator_config.py, app/calculator_memento.py, app/exceptions.py, app/history.py, app/input_validators.py, app/operations.py, and tests/ directory).
Create and activate a virtual environment for your project.
2. Application Development:

Develop an enhanced calculator command-line application with the following features:
REPL Interface: Implement a Read-Eval-Print Loop for continuous user interaction.
Advanced Arithmetic Operations: Allow users to perform addition, subtraction, multiplication, division, power, and root operations.
Design Patterns Integration:
Observer Pattern: Implement observers to monitor and react to calculation events (e.g., logging, auto-saving history).
Memento Pattern: Enable undo and redo functionality by preserving and restoring the application's state.
Strategy Pattern: Implement interchangeable operation execution strategies using the Strategy pattern.
Factory Pattern: Use a factory to instantiate operation classes based on user input.
Facade Pattern: Provide a simplified interface to complex subsystems within the Calculator class.
Data Management with pandas:
History Management: Utilize pandas DataFrames to store, manipulate, and persist calculation history.
Auto-Saving and Loading: Automatically save calculation history to CSV files and load existing history upon application start.
Configuration Management:
Implement a configuration system using environment variables and the dotenv library to manage application settings.
Validate configuration settings and handle configuration errors gracefully.
User Commands:
Implement commands such as help, history, exit, clear, undo, redo, save, and load to enhance user experience.
Error Handling:
Implement comprehensive error handling to manage invalid inputs and exceptional scenarios (e.g., division by zero, invalid operations).
Demonstrate both LBYL (Look Before You Leap) and EAFP (Easier to Ask Forgiveness than Permission) paradigms within your error handling strategies.
3. Best Practices:

DRY Principle: Apply the DRY (Don't Repeat Yourself) principle and other best practices to ensure your code is maintainable and efficient.
Modular Design: Organize your code into modules and classes to enhance readability and reusability.
Documentation:
Create a detailed README.md file with setup and usage instructions.
Document your code with meaningful comments and docstrings to enhance readability and maintainability.
4. Testing:

Unit Tests:
Write comprehensive unit tests using pytest to verify the functionality of individual components (e.g., arithmetic operations, calculation classes, observers).
Ensure that each method and function behaves as expected under various scenarios.
Parameterized Tests:
Implement parameterized tests in tests/test_calculations.py, tests/test_calculator_repl.py, tests/test_calculator_config.py, tests/test_calculator_memento.py, tests/test_exceptions.py, tests/test_history.py, tests/test_input_validators.py, and tests/test_operations.py to cover multiple input scenarios efficiently.
Achieve extensive test coverage by testing both positive and negative cases.
Test Coverage:
Use coverage tools (e.g., pytest-cov) to measure your test coverage.
Achieve 100% test coverage, ensuring that all lines of code, branches, and edge cases are tested.
Handling Coverage Exceptions:
Some lines of code, such as those containing pass or continue, may not be covered by tests. Research how to use coverage comments (e.g., # pragma: no cover) to intentionally ignore these lines without affecting overall coverage metrics.
Example:
if some_condition:
    pass  # pragma: no cover
5. Version Control & CI:

Push Code to GitHub:
Ensure your code follows best practices for code organization and documentation.
Commit changes with clear and descriptive messages.
Configure GitHub Actions:
Set up GitHub Actions to automatically run your tests and measure test coverage on each push to the repository.
Enforce 100% Test Coverage:
Configure your CI pipeline to check for 100% test coverage. If the coverage is below 100%, the build should fail, prompting you to add the necessary tests.
Example GitHub Actions workflow file (.github/workflows/python-app.yml):
name: Python application

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.x
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pytest pytest-cov pandas python-dotenv
    - name: Run tests with coverage
      run: |
        pytest --cov=app tests/
    - name: Check coverage
      run: |
        coverage report --fail-under=100
Handling Coverage Exceptions:
In your code, add comments like # pragma: no cover to lines that are intentionally excluded from coverage metrics (e.g., lines with pass or continue). This ensures that your coverage report accurately reflects the test coverage without being penalized for these lines.
Example:
if some_condition:
    pass  # pragma: no cover
Grading Expectations: 
Functionality: Completeness and accuracy of the enhanced calculator command-line application, including all specified features.
User Interface: Proper implementation of the REPL pattern and a user-friendly interface that handles user inputs gracefully.
Code Quality: Efficient use of Python control structures, adherence to the DRY principle, and professional coding practices.
Design Patterns Implementation: Correct and effective use of advanced design patterns (Factory, Observer, Memento, Strategy, Facade) within the application.
Data Management with pandas: Efficient integration of pandas for data handling, ensuring data integrity and performance.
Error Handling: Comprehensive error handling mechanisms that manage invalid inputs and exceptional scenarios effectively.
Testing:
Thorough unit and parameterized testing using pytest.
Achieving 90+% test coverage, ensuring all code paths are tested.
Documentation: Well-structured code with comprehensive documentation, including a clear and informative README.md.
Automation: Successful setup of GitHub Actions to automatically run your tests and enforce 100% test coverage, ensuring code quality on every commit.
