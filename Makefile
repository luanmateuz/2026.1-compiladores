.PHONY: venv install fmt fmt-check lint lint-fix test check clean

venv:
	@uv venv --python=3.14

install:
	@uv pip install -e '.'

fmt:
	@ruff format src/

fmt-check:
	@ruff format --check src/

lint:
	@ruff check src/

lint-fix:
	@ruff check src/ --fix
	
test:
	@pytest -vv tests

check: fmt-check lint test

clean:
	@rm -rf .ruff_cache
	@rm -rf .venv
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info/
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
	@find ./ -name '*.pyc' -exec rm -f {} +
	@find ./ -name '*.egg-info' -exec rm -rf {} +
	@find ./ -name '__pycache__' -exec rm -rf {} +
	@find ./ -name 'Thumbs.db' -exec rm -f {} +
	@find ./ -name '*~' -exec rm -f {} +
