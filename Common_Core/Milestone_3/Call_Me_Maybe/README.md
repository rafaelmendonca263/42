*This project has been created as part of the 42 curriculum by rmedonca.*

# Call Me Maybe

![Python](https://img.shields.io/badge/Python-3.12-blue) ![Build](https://img.shields.io/badge/Build-Makefile-orange) ![Code Style](https://img.shields.io/badge/Code%20Style-Flake8-green) ![Typing](https://img.shields.io/badge/Type%20Checking-MyPy-blueviolet) ![Testing](https://img.shields.io/badge/Testing-Pytest-brightgreen) ![Status](https://img.shields.io/badge/Status-Completed-success) ![42](https://img.shields.io/badge/School-42-black) ![Language](https://img.shields.io/badge/Language-Python-blue)

---

## Description

**Call Me Maybe** is an introduction to function calling in Large Language Models (LLMs). The primary goal of this project is to bridge the gap between natural human language requests and structured, machine-executable outputs using a small language model (`Qwen/Qwen3-0.6B`). 

Small models are notoriously unreliable at generating valid JSON structures spontaneously (often succeeding only ~30% of the time). To overcome this, the project implements **constrained decoding**, a technique that guides the model's output token-by-token to guarantee 100% valid JSON structures and strict schema compliance without relying on open-ended prompting alone.

---

## Instructions

### Prerequisites

* Python 3.10 or later
* `uv` package manager

### Installation & Setup

1. Clone the repository.
2. Ensure the `llm_sdk` package and input directories are properly placed.
3. Install project dependencies using the Makefile or `uv sync`:
  ```bash
  make install
  ```

### Execution
Run the main program using default paths (data/input/ and data/output/):

  ```bash
  make run
  ```

  Alternatively, execute it manually with custom parameters:

  ```bash
  uv run python -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calling_results.json
  ```

### Makefile Rules
* make install: Sets up the virtual environment (.venv), installs PyTorch, transformers, the llm_sdk package, project dependencies via uv, and linting/testing tools.

* make run: Executes the main script using default file locations.

* make test: Runs the test suite via pytest.

* make debug: Runs the main script using Python's built-in debugger (pdb).

* make clean: Cleans up temporary caches (__pycache__, .mypy_cache, .pytest_cache, etc.).

* make fclean: Deep cleans virtual environments and output data folders.

* make lint: Performs static code analysis using flake8 and mypy with strict typing checks.

* make lint-strict: Runs full strict mypy type checking alongside flake8.

## Algorithm Explanation

My implementation relies on advanced logit-masking constrained decoding across two critical phases:

1. Constrained Function Selection (ConstrainedFunctionSelector):

  * Maps user requests to available function definitions.
  * Dynamically tracks valid function name prefixes against the vocabulary using VocabularyManager.
  * Restricts token logits to only permit characters that build valid function names, completely eliminating invalid hallucinations.

2. Constrained JSON Parameter Extraction (ConstrainedJSONDecoder):

  * State Machine Tracking: Analyzes the generated string layout (in_str, escape characters, structural markers like {, :, ,, }) to determine whether the model is building a parameter key or a value.
  * Type-Aware Gating: Restricts character tokens based on the parameter's schema definition (e.g., locking number types to digits/decimals/signs, booleans to specific flags, and strings to text/quote constraints).
  * Logit Masking: Sets invalid token probabilities to negative infinity (-inf), guaranteeing that only structurally and semantically valid tokens are sampled.
  * Safe Parsing (_safe_loads): Sanitizes and parses completed JSON strings safely, managing trailing commas or escape characters.

## Design Decisions

* Centralized Vocabulary Indexing (VocabularyManager): Instead of performing expensive linear scans over the entire model vocabulary for every generated token, the vocabulary is indexed once at startup (char_to_tokens), caching clean token-string mappings to maintain blazing-fast execution speeds well under the 5-minute evaluation limit.

* Pydantic Validation Models (models.py): Leveraged Pydantic (BaseModel, Field) across function definitions, parameter schemas, test prompts, and output results to ensure robust runtime data validation and clean typing.

* Modular Code Architecture: Divided concerns neatly into dedicated modules:
  * __main__.py: CLI argument parsing and main execution pipeline coordination.

  * constrained_decoder.py: JSON constraint logic and logit masking.

  * llm_selector.py: Function selection logic using prefix constraints.

  * parser.py: Robust file input/output handling with error exceptions.

  * structure.py: Vocabulary management and triage utilities.

## Performance Analysis
* Accuracy: Consistently achieves high accuracy (>90%) in selecting the correct functions and extracting accurate arguments due to deterministic programmatic logit masking.

* Reliability: Guarantees 100% valid JSON output schemas, eliminating runtime parsing failures or malformed outputs.

* Speed: Processes entire test batches in seconds on standard CPU/GPU configurations, easily passing performance requirements.

## Challenges Faced

* Vocabulary Traversal Overhead: Iterating over tens of thousands of subword tokens at every generation step caused severe latency early on. This was solved by introducing VocabularyManager to pre-group token IDs by character prefixes at startup.

* Small Model Drift: The 0.6B parameter model has a tendency to output conversational prose when left unconstrained. Implementing state-aware token restriction successfully forced the model to remain locked within precise JSON syntax boundaries.

## Testing Strategy

* Unit Testing (tests/test_selection.py): Implemented a comprehensive suite using pytest covering diverse scenarios:

  * Small and large number extractions (e.g., addition calculations).
  * String parsing and string reversal tasks.
  * Complex parameters (e.g., regex substitutions with multiple arguments).
  * Edge cases including special characters, spaces, and formatting quirks.

* Error Handling: Validates robust handling of missing files, invalid JSON structures, and unexpected input formats with clear error messages.

## Example Usage

Input (function_calling_tests.json)
[
  {
    "prompt": "What is the sum of 2 and 3?"
  },
  {
    "prompt": "Reverse the string 'hello'"
  }
]

Output (function_calling_results.json)
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {
      "s": "hello"
    }
  }
]

## Resources & AI Usage
### References
* Python Typing Module Documentation

* Pydantic Documentation

* Hugging Face Tokenizer Concepts

### AI Usage Disclosure
* Architecture Design & Brainstorming: Discussing strategies for efficient token-level logit manipulation and vocabulary indexing patterns.

* Documentation Support: Structuring and drafting comprehensive technical explanations for this README.md file.