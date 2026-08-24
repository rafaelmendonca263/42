PYTHON_SYS ?= /usr/bin/python3
VENV        = .venv
PYTHON      = $(VENV)/bin/python3
PIP         = $(VENV)/bin/pip3
MYPY        = $(VENV)/bin/mypy
FLAKE8      = $(VENV)/bin/flake8
FLAKE8_FLAGS = --exclude=$(VENV),.venv,__pycache__

all: install lint

install:
	@if [ ! -d "$(VENV)" ]; then \
		$(PYTHON_SYS) -m venv --without-pip $(VENV); \
		curl -sS https://bootstrap.pypa.io/get-pip.py | $(PYTHON); \
	fi
	@$(PIP) install --upgrade pip setuptools wheel >/dev/null 2>&1
	@$(PIP) install mypy flake8 Pillow pygame >/dev/null 2>&1

run: install
	@args="$(filter-out run,$(MAKECMDGOALS))"; \
	if [ -z "$$args" ]; then \
		echo "Error: Map not specified!"; \
		echo "Correct usage: make run path/to/map.txt"; \
		exit 1; \
	fi; \
	$(PYTHON) main.py $$args --visual

debug: install
	@args="$(filter-out debug,$(MAKECMDGOALS))"; \
	if [ -z "$$args" ]; then \
		echo "Error: Map not specified!"; \
		echo "Correct usage: make debug path/to/map.txt"; \
		exit 1; \
	fi; \
	$(PYTHON) -m pdb main.py $$args --visual

lint: install
	@$(FLAKE8) $(FLAKE8_FLAGS) *.py
	@$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs *.py

lint-strict: install
	@$(FLAKE8) $(FLAKE8_FLAGS) *.py
	@$(MYPY) --strict *.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache *.pyc **/__pycache__

fclean: clean
	rm -rf $(VENV) .venv

re: fclean all

%:
	@:

.PHONY: all install run debug lint lint-strict clean fclean re