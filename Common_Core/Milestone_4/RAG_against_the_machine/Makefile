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
	uv sync --python 3.10 --link-mode=copy

run: install
	uv run python -m src

test: install
	uv run pytest tests/ -v

debug: install
	uv run python -m pdb -m src index --max_chunk_size 2000

clean:
	@rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache
	@find . -type d -name '__pycache__' -prune -exec rm -rf {} +
	@find . -type f -name '*.pyc' -delete
	@rm -rf .venv 2>/dev/null || true

fclean: clean
	@rm -rf data/output data/processed
	@rm -f uv.lock

lint: install
	uv run flake8 src tests
	uv run mypy src tests \
		--warn-return-any --warn-unused-ignores \
		--ignore-missing-imports --disallow-untyped-defs \
		--check-untyped-defs

lint-strict: install
	uv run flake8 src tests
	uv run mypy src tests --strict

re: fclean
	@$(MAKE) install

.PHONY: install run debug clean lint lint-strict re setup-cache test