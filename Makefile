.PHONY: install install-dev run \
        lint format check \
        test cov \
        pre-commit \
        clean project_tree project_tree_short \
        commit

# Variables
PYTHON     = poetry run python
LINT_DIRS  = app tests

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies only
	poetry install --without dev --no-root

install-dev: ## Install all dependencies including dev tools
	poetry install --no-root
	poetry run pre-commit install

run: ## Run the project
	$(PYTHON) main.py

format: ## Auto-format code with black and isort
	$(PYTHON) -m isort $(LINT_DIRS)
	$(PYTHON) -m black $(LINT_DIRS)

lint: ## Run flake8 linter
	$(PYTHON) -m flake8 $(LINT_DIRS)

check: ## Run all checks without modifying files
	$(PYTHON) -m flake8 $(LINT_DIRS)
	$(PYTHON) -m isort $(LINT_DIRS) --check-only
	$(PYTHON) -m black $(LINT_DIRS) --check

test: ## Run tests
	$(PYTHON) -m pytest

cov: ## Run tests with coverage report
	$(PYTHON) -m pytest --cov=app --cov-report=term-missing --cov-report=html
	@echo "Coverage report: htmlcov/index.html"

pre-commit: ## Run pre-commit hooks on all files
	poetry run pre-commit run --all-files

clean: ## Remove cache, build and temp files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name ".DS_Store" -delete
	rm -rf .mypy_cache .pytest_cache htmlcov .coverage
	@echo "Cleaned up."

project_tree: ## Show full project tree
	tree -a -I ".venv|.git|.vscode|.idea|.mypy_cache|__pycache__|htmlcov"

project_tree_short: ## Show project tree (depth 2)
	tree -a -L 2 -I ".venv|.git|.vscode|.idea|.mypy_cache|__pycache__|htmlcov|*.pyc|*.log|logs|.pytest_cache|.coverage|.DS_Store"

commit: ## Make a commit with commitizen
	poetry run cz commit
