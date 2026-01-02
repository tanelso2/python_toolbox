default: pr-prep

pr-prep: format lint test

checks: check-format lint test

format:
	black .

check-format:
	black --check .

lint:
	flake8 .

test:
	python -m pytest test/
