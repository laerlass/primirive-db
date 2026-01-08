install:
	poetry install

run:
	poetry run database

lint:
	poetry run ruff check .

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install dist/*.whl

clean:
	rm -rf dist
	rm -rf .venv
