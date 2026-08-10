.PHONY: install run debug clean lint lint-strict re


venv:
	python3 -m venv .venv

install: venv
	.venv/bin/python3 -m pip install --upgrade pip
	.venv/bin/python3 -m pip install flake8 mypy

run: install
	.venv/bin/python3 -m src --input input/Prompt.json --output output/Results.json

debug: install
	.venv/bin/python3 -m pdb -m src

clean:
	rm -rf .venv __pycache__ .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict

re: clean
	$(MAKE) install