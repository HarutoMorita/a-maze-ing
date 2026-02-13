
MAIN_PROGRAM = a_maze_ing.py
ARG_FILE = config.txt
PACKAGE_NAME = mazegen

VENV = .venv
PYTHON_VER = python3
PYTHON_EXEC = $(VENV)/bin/$(PYTHON_VER)
PIP = $(VENV)/bin/pip
MLX_WHL      = mlx-2.2-py3-none-any.whl
REQUIREMENTS = requirements.txt

MYPY_OPTION = --warn-return-any \
				--warn-unused-ignores \
				--ignore-missing-imports \
				--disallow-untyped-defs \
				--check-untyped-defs

.PHONY: all install run debug clean fclean lint lint-strict build test-pkg

all: install lint

install:
	$(PYTHON_VER) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install ./mlx-2.2-py3-none-any.whl
	$(PIP) install -r $(REQUIREMENTS)
	$(PIP) install .

run:
	$(PYTHON_EXEC) $(MAIN_PROGRAM) $(ARG_FILE)

debug:
	$(PYTHON_EXEC) -m pdb $(MAIN_PROGRAM) $(ARG_FILE)

clean:
	rm -rf .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)
	rm -rf dist build *.egg-info
	rm -f mazegen-*.whl mazegen-*.tar.gz

lint:
	$(PYTHON_EXEC) -m flake8 .
	$(PYTHON_EXEC) -m mypy . $(MYPY_OPTION)

lint-strict:
	$(PYTHON_EXEC) -m flake8 .
	$(PYTHON_EXEC) -m mypy . --strict

build: clean
	$(PYTHON_EXEC) -m build
	cp dist/*.whl ./
	cp dist/*.tar.gz ./

test-pkg: build
	rm -rf test_dir
	mkdir test_dir
	$(PYTHON_VER) -m venv test_dir/venv
	test_dir/venv/bin/pip install *.whl
	cp a_maze_ing.py config.txt config.py test_dir/
	cd test_dir && ./venv/bin/python3 a_maze_ing.py config.txt
	rm -rf test_dir
