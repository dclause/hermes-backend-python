APPLICATION := hermes
DOCUMENTATION := documentation
ROOT_FOLDER := .
SRC_FOLDER := $(APPLICATION)
TEST_FOLDER := tests
PYTHON=$(VENV)/python
PIP=$(VENV)/pip3

ifeq ($(OS),Windows_NT)     # is Windows_NT on XP, 2000, 7, Vista, 10...
    DETECTED_OS := Windows
else
    DETECTED_OS := $(shell uname)  # same as "uname -s"
endif

ifeq ($(DETECTED_OS),Windows)
	ACTIVATE := . .venv/Scripts/activate.bat
else
	ACTIVATE := @source ./.venv/Scripts/activate
endif

help: ## Print help for each target
	$(info Welcome to RMS - RobotManagmentSystem - makefile.)
	$(info =============================)
	$(info )
	$(info Available commands:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' Makefile \
		| awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'

doc: ## Open documentation
	@$(PYTHON) $(DOCUMENTATION)/main.py

env: ## Make virtual environment
	@$(PY) -m venv .venv

install: ## Install everything
	@make env
	@$(PIP) install -r requirements.txt
	@make clean

run: ## Run the code
	@if [ -d "./.venv" ]; then $(PYTHON) -m $(APPLICATION); \
	else echo "Run 'make install' command first" >&2 ; fi

dev: ## Run code in dev mode
	@if [ -d "./.venv" ]; then $(PYTHON) -m $(APPLICATION) --dev --debug ; \
	else echo "Run 'make install' command first" >&2 ; fi

clean: ## Cleanup
	@rm -f **/*.pyc
	@rm -rf **/__pycache__
	@rm -rf *.pyc __pycache__ .pytest_cache .mypy_cache .coverage coverage.xml
	@$(VENV)/ruff clean

test: ## Run all tests
	@type $(VENV)/pytest >/dev/null 2>&1 || (echo "Run 'make install' first." >&2 ; exit 1)
	$(VENV)/pytest
	@make clean

lint: ## Lint the code
	$(info Running Mypy against source files...)
	-@if type $(VENV)/mypy >/dev/null 2>&1 ; then $(VENV)/mypy --show-error-codes $(APPLICATION) ; \
	else echo "SKIPPED. Run 'make install' first." >&2 ; fi

	$(info Running Ruff against source files...)
	-@if type $(VENV)/ruff >/dev/null 2>&1 ; then $(VENV)/ruff check $(APPLICATION) ; \
	else echo "SKIPPED. Run 'make install' first." >&2 ; fi

	@make clean

update: ## Update the dependencies
	@make env
	@if type pur >/dev/null 2>&1 ; then pur -r requirements.txt ; \
	@if type pur >/dev/null 2>&1 ; then pur -o dev_requirements.txt -r dev_requirements.txt ; \
	else echo "SKIPPED. Run '$(PIP) install pur' first." >&2 ; fi

feedback: ## Provide feedback
	@$(PY) -m webbrowser https://github.com/dclause/hermes/issues

include Makefile.venv
