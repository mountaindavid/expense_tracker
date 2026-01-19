.PHONY: test test-cov test-integration test-all-cov lint format format-check clean help

help:
	@echo "Available commands:"
	@echo "  make test            - Run all unit tests"
	@echo "  make test-cov        - Run unit tests with coverage report"
	@echo "  make test-integration - Run integration tests (requires test DB)"
	@echo "  make test-all-cov    - Run ALL tests (unit + integration) with coverage"
	@echo "  make lint            - Run flake8 linter"
	@echo "  make format          - Format code with black"
	@echo "  make format-check    - Check code formatting without changes"
	@echo "  make clean           - Remove coverage and cache files"
	@echo "  make all             - Run format, lint, and test-all-cov"

test:
	pytest app/tests/unit/ -v

test-cov:
	pytest app/tests/unit/ --cov=app --cov-report=term-missing --cov-report=html

test-integration:
	pytest app/tests/integration/ -v

test-all-cov:
	pytest app/tests/ --cov=app --cov-report=term-missing --cov-report=html

lint:
	flake8 app/ --count --statistics

format:
	black app/

format-check:
	black app/ --check

clean:
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

all: format lint test-all-cov
