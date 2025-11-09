# Lab0: Data Preprocessing CLI & CI Fundamentals

This project is a command-line interface (CLI) tool written in Python for performing common data preprocessing operations. The primary goal of the lab is to demonstrate the fundamentals of Continuous Integration (CI), including code formatting, linting, and automated testing.

The project uses `uv` for dependency management and `click` for the CLI.

## Features

The CLI is organized into four main command groups:

* **`clean`**: Functions for cleaning data (removing or filling missing values).
* **`numeric`**: Functions for processing numerical attributes (normalizing, standardizing, clipping, etc.).
* **`text`**: Functions for processing textual information (tokenizing, removing punctuation, etc.).
* **`struct`**: Functions for manipulating data structure (flattening, shuffling, unique values).

## Project Structure
Lab0/ 
	├── .gitignore 
	├── pyproject.toml 
	├── pytest.ini 
	├── README.md 
	├── src/ 
	│ ├── init.py 
	│ ├── cli.py 
	│ └── preprocessing.py 
	├── tests/ 
	│ ├── test_cli.py 
	│ └── test_logic.py 
	└── uv.lock
	
## 📋 Core Dependencies

* **`click`**: For building the command-line interface.
* **`black`**: For automatic code formatting.
* **`pylint`**: For linting and code quality analysis.
* **`pytest`**: For running unit and integration tests.
* **`pytest-cov`**: For measuring test coverage.


## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/pina131714/Lab0.git](https://github.com/pina131714/Lab0.git)
    cd Lab0
    ```

2.  Initialize the `uv` environment (if needed) and sync the dependencies (reads `uv.lock`):
    ```bash
    uv sync
    ```
    
## Development & Testing
This project is set up to use standard formatting, linting, and testing tools.

### Linting with pylint
To analyze code quality and check for potential errors:
```bash
uv run python -m pylint src/*.py
```

### Formatting with black
To automatically format all code (in src/ and tests/):
```bash
uv run black src/*.py
```

### Testing
To run all unit and integration tests:
```bash
uv run python -m pytest -v
```

### Measuring Test Coverage
To run tests and see what percentage of the src/ code is covered:
```bash
uv run python -m pytest -v --cov=src
```

