# Makefile for Document Parser project

.PHONY: help install install-dev test test-cov lint format type-check clean build run-example

# Default target
help:
	@echo "Document Parser - Available commands:"
	@echo ""
	@echo "  install      Install the package and dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage report"
	@echo "  lint         Run linting (flake8)"
	@echo "  format       Format code with black"
	@echo "  type-check   Run type checking with mypy"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build the package"
	@echo "  run-example  Run the example script"
	@echo "  all-checks   Run all code quality checks"

# Installation
install:
	pip install -r requirements.txt
	pip install -e .

install-dev:
	pip install -r requirements.txt
	pip install -e .[dev]

# Testing
test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=document_parser --cov-report=html --cov-report=term

# Code quality
lint:
	flake8 document_parser/ tests/

format:
	black document_parser/ tests/ *.py

type-check:
	mypy document_parser/

# All checks
all-checks: lint type-check test

# Cleanup
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build
build: clean
	python setup.py sdist bdist_wheel

# Example
run-example:
	python example_usage.py

# Development setup
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make run-example' to test the installation."
