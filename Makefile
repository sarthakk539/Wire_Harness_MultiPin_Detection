.PHONY: help install dev test build clean run

help:
	@echo "Wire Harness Detector - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install      Install dependencies"
	@echo "  make dev          Install in development mode"
	@echo ""
	@echo "Development:"
	@echo "  make test         Run tests"
	@echo "  make lint         Run linting"
	@echo ""
	@echo "Build:"
	@echo "  make build        Build wheel package"
	@echo "  make exe          Build standalone executable"
	@echo ""
	@echo "Run:"
	@echo "  make run          Run application"
	@echo "  make clean        Clean build artifacts"

install:
	pip install -r requirements.txt

dev:
	pip install -e .
	pip install pytest pytest-cov

test:
	pytest backend/test_multipin.py -v

lint:
	pylint backend/*.py app.py || true

build: clean
	python build_wheel.py

exe: clean
	python build_executable.py

run:
	python app.py --help

clean:
	rm -rf build/ dist/ *.egg-info __pycache__ .pytest_cache *.spec
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
