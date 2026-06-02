VENV        = .venv
PYTHON      = $(VENV)/bin/python3
PIP         = $(VENV)/bin/pip3
MYPY        = $(VENV)/bin/mypy
FLAKE8      = $(VENV)/bin/flake8
MAPA        = maps/challenger/01_the_impossible_dream.txt

all: install lint

install:
	@if [ ! -d "$(VENV)" ]; then \
		python3 -m venv $(VENV); \
	fi
	@$(PIP) install --upgrade pip setuptools wheel >/dev/null 2>&1
	@$(PIP) install mypy flake8 >/dev/null 2>&1

run: install
	@if [ ! -d "$(VENV)" ]; then exit 1; fi
	$(PYTHON) main.py $(MAPA)

debug:
	@if [ ! -d "$(VENV)" ]; then exit 1; fi
	$(PYTHON) -m pdb main.py $(MAPA)

lint:
	@if [ ! -d "$(VENV)" ]; then exit 1; fi
	$(FLAKE8) main.py simulation.py visualizer.py
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs main.py simulation.py visualizer.py

lint-strict:
	@if [ ! -d "$(VENV)" ]; then exit 1; fi
	$(FLAKE8) main.py simulation.py visualizer.py
	$(MYPY) --strict main.py simulation.py visualizer.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache *.pyc

fclean: clean
	rm -rf $(VENV)

re: fclean all

.PHONY: all install run debug lint lint-strict clean fclean re