MODULE := hermes
SRC_FOLDER := $(MODULE)
TEST_FOLDER := tests
PYTHON=python
PIP=pip3

help: ## Print help for each target
	$(info Welcome to RMS - RobotManagmentSystem - makefile.)
	$(info =============================)
	$(info )
	$(info Available commands:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'

run: ## Run the code
	@$(PYTHON) -m $(MODULE) -w

test: ## Test the code
	@type pytest >/dev/null 2>&1 || (echo "Run '$(PIP) install pytest' first." >&2 ; exit 1)
	@pytest --cov-report term-missing:skip-covered; rm -rf .coverage

lint: ## Lint the code
	$(info Running Pylint against source and test files...)
	@if type pylint >/dev/null 2>&1 ; then pylint --rcfile=setup.cfg **/*.py ; \
	else echo "SKIPPED. Run '$(PIP) install pylint' first." >&2 ; fi

	$(info Running Flake8 against source and test files...)
	@if type flake8 >/dev/null 2>&1 ; then flake8 --max-complexity 10 $(MODULE) ; \
	else echo "SKIPPED. Run '$(PIP) install flake8' first." >&2 ; fi

	$(info Running Bandit against source files...)
	@if type bandit >/dev/null 2>&1 ; then bandit -r --ini setup.cfg ; \
	else echo "SKIPPED. Run '$(PIP) install bandit' first." >&2 ; fi

	$(info Running Mypy against source files...)
	@if type mypy >/dev/null 2>&1 ; then mypy --show-error-codes --ignore-missing-imports $(MODULE) ; \
	else echo "SKIPPED. Run '$(PIP) install mypy' first." >&2 ; fi

clean: ## Cleanup
	@rm -f $(SRC_FOLDER)/*.pyc
	@rm -rf $(SRC_FOLDER)/__pycache__
	@rm -f $(TEST_FOLDER)/*.pyc
	@rm -rf $(TEST_FOLDER)/__pycache__
	@rm -rf .pytest_cache .mypy_cache .coverage coverage.xml

deps-update: ## Update the dependencies
	@if type pur >/dev/null 2>&1 ; then pur -r requirements.txt ; \
	else echo "SKIPPED. Run '$(PIP) install pur' first." >&2 ; fi

deps-install: ## Install the dependencies
	@type $(PIP) >/dev/null 2>&1 || (echo "Run 'curl https://bootstrap.pypa.io/get-pip.py|sudo python3' first." >&2 ; exit 1)
	@$(PIP) install -r requirements.txt

dev-deps-install: ## Install the dependencies
	@type $(PIP) >/dev/null 2>&1 || (echo "Run 'curl https://bootstrap.pypa.io/get-pip.py|sudo python3' first." >&2 ; exit 1)
	@$(PIP) install -r dev_requirements.txt

dev-deps-update: ## Update the dependencies
	@if type pur >/dev/null 2>&1 ; then pur -o dev_requirements.txt -r dev_requirements.txt ; \
	else echo "SKIPPED. Run '$(PIP) install pur' first." >&2 ; fi

feedback: ## Provide feedback
	@$(PYTHON) -m webbrowser https://github.com/dclause/hermes/issues
