PYTHON = python3
VENV = venv
PIP = $(VENV)/bin/pip
PY = $(VENV)/bin/python

install:
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy

run: install
	$(PY) a_maze_ing.py config.txt

debug: install
	$(PY) -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf venv

lint: install
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict: install
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

.PHONY: install run debug clean lint lint-strict