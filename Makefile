NAME = mazegen-1.0.0.whl
PACKAGE_NAME = mazegen

.PHONY: all install run debug clean lint lint-strict build

all: lint build

install:
	pip install .
	pip install flake8 mypy build

run:
	python3 a-maze-ing.py

debug:
	python3 -m pdb a-maze-ing.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache dist build *.egg-info
	rm -f $(NAME)

lint:
	python3 -m flake8 . --exclude=.venv
	python3 -m mypy . --exclude "(.venv|build|DFS_amazing)" \
			--warn-return-any \
			--warn-unused-ignores \
			--ignore-missing-imports \
			--disallow-untyped-defs \
			--check-untyped-defs

lint-strict:
	python3 -m flake8 . --exclude=.venv,build
	python3 -m mypy . --exclude "(.venv|build)" --strict

build: clean
	python3 -m build
	cp dist/*.whl ./$(NAME)
