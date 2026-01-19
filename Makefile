.PHONY: test test-cov lint format format-check clean help

help:
	@echo "Available commands:"
	@echo "  make test          - Run all tests"
	@echo "  make test-cov      - Run tests with coverage report"
	@echo "  make lint          - Run flake8 linter"
	@echo "  make format        - Format code with black"
	@echo "  make format-check  - Check code formatting without changes"
	@echo "  make clean         - Remove coverage and cache files"
	@echo "  make all           - Run format, lint, and test-cov"

test:
	pytest app/tests/unit/ -v

test-cov:
	pytest app/tests/unit/ --cov=app --cov-report=term-missing --cov-report=html

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

all: format lint test-cov
