## Instructions

This project requires Python 3.10+ and a Linux environment as the MiniLibX binary is built for Linux.

### Installation
Before running the program, you must set up the environment using `make` or `make install`.

- `make` sets up the environment (`make install`) and check the code quality (`make lint`).
- `make install` creates **venv**, installs the **MiniLibX** library from **mlx-2.2-py3-none-any.whl** and installs dependencies from **requirements.txt**.
```bash
% make		    # Setup environment and run linter
% make install  # Install dependencies and package using pip
```
### Code Quality Check
This project adopts **flake8** for the coding standard and **mypy** for the static type checking.

- `make lint` runs flake8 and mypy with specific options.
- `make lint-strict` runs flake8 and mypy with the strict option.

Options for `lint`:
- --warn-return-any, --warn-unused-ignores
- --ignore-missing-imports
- --disallow-untyped-defs, --check-untyped-defs
```bash
% make lint			# Format and type check.
% make lint-strict	# Format and strict type check
```

### Execution and Usage
The main program **a_maze_ing.py** takes **config.txt** as an argument.

- `make run` executes the main program under venv.
- `make debug` runs the program with debugger (pdb)

```bash
% make run		# Execute the main program
% make debug	# Run in debug mode
```

On execution, a window will pop up and display a maze generated with the settings specified in the config.txt. \
The following guide for window operations will be displayed on your terminal.
```zsh
----- Click window, then press following keys -----
1: Regenerate a new maze.
2: Show/Hide path from entry to exit.
3: Change wall color.
4: Regenerate a new maze with animation.
Esc: Exit immediately.
```

You can create your own maze by modifying **config.txt**. \
Or you can manually execute the program with your own config file.
```bash
% .venv/bin/python3 a_maze_ing.py your_config.txt
```

### Maintenance
`make clean` deletes temporary files, Python artifacts, and caches.
`make fclean`runs `make clean` and resets the project to its initial state.
```bash
% make clean	# Remove temporary files and caches
% make fclean	# Clean + remove venv, build artifacts, and caches
```
- `make build` build the mazegen package with extension **.whl** and **.tar.gz** and place them at the root directory. \
- `make test-pkg` Verify if the built package properly works as a package in a clean temporary environment.
```bash
% make build		# Build the mazegen package
% make test-pkg		# Verify the .whl installation
```
