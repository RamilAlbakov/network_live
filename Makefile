install:
	poetry install

lint:
	poetry run flake8 network_live

selfcheck:
	poetry check

check: selfcheck lint

build: check
	poetry build

isort:
	poetry run isort network_live

.PHONY: install lint selfcheck check build isort
