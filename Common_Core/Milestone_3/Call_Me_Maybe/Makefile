.PHONY: install run debug clean lint lint-strict re


venv:
	python3 -m venv .venv

install: venv
	@.venv/bin/python3 -m pip install --upgrade pip
	@.venv/bin/python3 -m pip install "torch==2.3.1"
	@.venv/bin/python3 -m pip install "transformers<5.0.0"
	@.venv/bin/python3 -m pip install -e ./llm_sdk
	@.venv/bin/python3 -m pip install -e .
	@.venv/bin/python3 -m pip install flake8 mypy pytest

run: install
	.venv/bin/python3 -m src \
		--functions_definition data/input/functions_definition.json \
		--input data/input/function_calling_tests.json \
		--output data/output/function_calling_results.json

test: install
	.venv/bin/python3 -m pytest tests/ -v

debug: install
	.venv/bin/python3 -m pdb -m src --functions_definition data/input/functions_definition.json --input data/input/function_calling_tests.json --output data/output/function_calling_results.json

clean:
	@rm -rf .venv __pycache__ .mypy_cache .pytest_cache .ruff_cache
	@find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	@find . -type f -name '*.pyc' -delete

fclean: clean
	@rm -rf $(VENV) .venv
	@rm -rf data/output

lint: install
	.venv/bin/python3 -m flake8 src tests
	.venv/bin/python3 -m mypy src tests \
		--warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict: install
	.venv/bin/python3 -m flake8 src tests
	.venv/bin/python3 -m mypy src tests --strict

re: clean
	$(MAKE) install