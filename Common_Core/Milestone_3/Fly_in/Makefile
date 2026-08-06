VENV        = .venv
PYTHON      = $(VENV)/bin/python3
PIP         = $(VENV)/bin/pip3
MYPY        = $(VENV)/bin/mypy
FLAKE8      = $(VENV)/bin/flake8

all: install lint

install:
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
	fi
	@$(PIP) install --upgrade pip setuptools wheel >/dev/null 2>&1
	@$(PIP) install mypy flake8 Pillow pygame >/dev/null 2>&1

run: install
	@if [ ! -d "$(VENV)" ]; then exit 1; fi
	@args="$(filter-out run,$(MAKECMDGOALS))"; \
	if [ -z "$$args" ]; then \
		echo "❌ Erro: Falta especificar o mapa!"; \
		echo "👉 Uso correto: make run caminho/do/mapa.txt"; \
		exit 1; \
	fi; \
	mapa=$$(echo $$args | awk '{print $$1}'); \
	$(PYTHON) main.py $$mapa --visual

debug: install
	@if [ ! -d "$(VENV)" ]; then exit 1; fi
	@args="$(filter-out debug,$(MAKECMDGOALS))"; \
	mapa=$$(echo $$args | awk '{print $$1}'); \
	if [ -z "$$mapa" ]; then \
		echo "❌ Erro: Falta especificar o mapa!"; \
		exit 1; \
	fi; \
	$(PYTHON) -m pdb main.py $$mapa --visual

# Flags obrigatórias do Chapter III.2
lint:
	@if [ ! -d "$(VENV)" ]; then exit 1; fi
	$(FLAKE8) *.py
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs *.py

# Verificação estrita opcional recomendada
lint-strict:
	@if [ ! -d "$(VENV)" ]; then exit 1; fi
	$(FLAKE8) *.py
	$(MYPY) --strict *.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache *.pyc **/__pycache__

fclean: clean
	rm -rf $(VENV)

re: fclean all

%:
	@:

.PHONY: all install run debug lint lint-strict clean fclean re