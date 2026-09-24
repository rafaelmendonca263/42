.PHONY: install run debug clean lint lint-strict re setup-cache test

setup-cache:
	@if [ -d $$HOME/sgoinfre ]; then \
		mkdir -p $$HOME/sgoinfre/.cache; \
		if [ -d $$HOME/.cache ] && [ ! -L $$HOME/.cache ]; then \
			cp -rn $$HOME/.cache/. $$HOME/sgoinfre/.cache/ 2>/dev/null || true; \
			rm -rf $$HOME/.cache; \
		fi; \
		if [ ! -e $$HOME/.cache ]; then \
			ln -s $$HOME/sgoinfre/.cache $$HOME/.cache; \
		fi; \
	else \
		echo "AVISO: sgoinfre não encontrado. A usar cache local."; \
		mkdir -p $$HOME/.cache; \
	fi

install: setup-cache
	@uv sync --python 3.10

run: install
	@.venv/bin/python -m src \
		--functions_definition data/input/functions_definition.json \
		--input data/input/function_calling_tests.json \
		--output data/output/function_calling_results.json

test: install
	@.venv/bin/pytest tests/ -v

debug: install
	@.venv/bin/python -m pdb -m src \
		--functions_definition data/input/functions_definition.json \
		--input data/input/function_calling_tests.json \
		--output data/output/function_calling_results.json

clean:
	@rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache
	@find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	@find . -type f -name '*.pyc' -delete
	@rm -rf .venv 2>/dev/null || true

fclean: clean
	@rm -rf data/output
	@rm -rf .venv 2>/dev/null || true
	@rm -f uv.lock
	@rm -rf llm_sdk/uv.lock

lint: install
	@.venv/bin/flake8 src tests
	@.venv/bin/mypy src tests \
		--warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict: install
	@.venv/bin/flake8 src tests
	@.venv/bin/mypy src tests --strict

re: fclean
	@$(MAKE) install
