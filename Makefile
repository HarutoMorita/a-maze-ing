.PHONY: install run debug clean lint

install:
	pip install .
	pip install flake8 mypy build

run:
	python3 a-maze-ing.py

debug:
	python3 -m pdb a-maze-ing.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache dist build *.egg-info

lint:
	python3 -m flake8 . --exclude=.venv
	python3 -m mypy . --exclude .venv --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
