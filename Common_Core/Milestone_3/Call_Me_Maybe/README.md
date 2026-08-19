# Call Me Maybe

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Build](https://img.shields.io/badge/Build-Makefile-orange) ![Code Style](https://img.shields.io/badge/Code%20Style-Flake8-green) ![Typing](https://img.shields.io/badge/Type%20Checking-MyPy-blueviolet) ![Testing](https://img.shields.io/badge/Testing-Pytest-brightgreen) ![Status](https://img.shields.io/badge/Status-Completed-success) ![42](https://img.shields.io/badge/School-42-black) ![Language](https://img.shields.io/badge/Language-Python-blue)

---

## Overview

Small function-calling project in Python that selects the most relevant function from a natural-language prompt and extracts the parameters needed to call it correctly.

This project combines lightweight schema validation, deterministic scoring, and a minimal local SDK fallback so it runs cleanly in constrained environments.

### Summary

- Function selection from natural language
- Parameter extraction for the chosen function
- JSON output generation
- Validation with pytest, flake8, and mypy
- Simple local setup using a virtual environment and Makefile

## Objective

Given a set of functions in JSON and a list of prompts, the program:

1. evaluates which function best matches the request;
2. extracts the relevant parameters from the text;
3. generates a structured JSON result.

The project was designed to run in constrained environments, with a local fallback and without requiring heavy ML dependencies.

---

## Project Structure

- `src/__main__.py` — CLI entry point
- `src/scorer.py` — logic for selecting the best function
- `src/models.py` — schemas and validation with Pydantic
- `src/parser.py` — JSON reading and writing
- `llm_sdk/llm_sdk/__init__.py` — lightweight SDK with local fallback
- `data/input/functions_definition.json` — available function definitions
- `data/input/function_calling_tests.json` — test prompts
- `data/output/function_calling_results.json` — generated output
- `Makefile` — installation, execution, and validation commands

---

## Requirements

- Python 3.10+
- `venv` available in the system

---

## Installation

```bash
make install
```

This command creates the virtual environment and installs:

- the local SDK package;
- the main project package;
- `flake8` and `mypy` for validation.

---

## How to Run

```bash
make run
```

Or directly:

```bash
. .venv/bin/activate
python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

---

## Validation

```bash
make lint
```

You can also run the tests:

```bash
. .venv/bin/activate
python -m pytest -q
```

---

## Included Functions

The project includes 3 example functions:

- `get_weather` — returns the temperature and weather for a city
- `search_information` — searches general information about a topic or entity
- `get_current_time` — returns the current time for a location

---

## Expected Output

The final output is written to:

```text
data/output/function_calling_results.json
```

Each result contains:

- the original `prompt`;
- the selected function name;
- the extracted parameters.

---

## Project Highlights

This project was designed as a functional and educational base for function calling, with focus on:

- code organization by responsibility;
- schema validation and data integrity;
- minimal-environment execution;
- verification through tests, lint, and type checking.

---

## Example Result

Running the program produces output similar to this:

```json
[
  {
    "prompt": "What is the temperature in Lisbon today?",
    "name": "get_weather",
    "parameters": {
      "city": "Lisbon"
    }
  }
]
```