default: pr-prep

pr-prep: format lint typecheck test

checks: check-format lint typecheck test

format:
	black .

check-format:
	black --check .

lint:
	flake8 --show-source --statistics --extend-exclude=.venv --max-line-length 120 .

test:
	python -m pytest tests/

typecheck:
	mypy .

install-dev:
	pip install -r requirements.txt