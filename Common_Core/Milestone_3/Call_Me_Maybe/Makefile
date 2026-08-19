.PHONY: install run debug clean lint lint-strict re


venv:
	python3 -m venv .venv

install: venv
	.venv/bin/python3 -m pip install --upgrade pip
	.venv/bin/python3 -m pip install -e ./llm_sdk
	.venv/bin/python3 -m pip install -e .
	.venv/bin/python3 -m pip install flake8 mypy

run: install
	.venv/bin/python3 -m src \
		--functions_definition data/input/functions_definition.json \
		--input data/input/function_calling_tests.json \
		--output data/output/function_calling_results.json

debug: install
	.venv/bin/python3 -m pdb -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calling_results.json

clean:
	rm -rf .venv __pycache__ .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	find . -type f -name '*.pyc' -delete

lint:
	.venv/bin/python3 -m flake8 src tests llm_sdk
	.venv/bin/python3 -m mypy src tests llm_sdk \
		--warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict:
	.venv/bin/python3 -m flake8 src tests llm_sdk
	.venv/bin/python3 -m mypy src tests llm_sdk --strict

re: clean
	$(MAKE) install