*This project has been created as part of the 42 curriculum by hmorita, daogawa.*

## Description

"A-Maze-ing" is a Python-based project focused on the algorithmic generation, solving, and visualization of mazes.

The primary goal of this project is to generate random yet reproducible mazes based on a user-provided configuration file (config.txt). The generated maze is output as hexadecimal data representing wall placements, and can be visualized through both a terminal and a graphical interface.

Key Features:

1. Maze Generation: Generates mazes based on specific width and height settings. When the "Perfect" flag is enabled, the tool creates a "Perfect Maze" with exactly one path between the entrance and the exit. Additionally, the maze features a visually integrated "42" pattern.

2. Solving & Visualization: Calculates the shortest path of the generated maze and presents it visually using ASCII art or the MiniLibX library.

3. Code Reusability: The maze generation logic is implemented as a standalone class, designed as a Python package to be easily integrated into future projects.

## Instructions
This project requires Python 3.10+ and a Linux environment as the MiniLibX binary is built for Linux.

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
Here is the config file format.
Note: # can be used for comments.
```bash
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
# Optional
SEED=42
ALGO=DFS
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

## Implementation
The mazegen module has two types of maze generation algorithm.

### Algorithm

The main(default) algorithm is Depth-First Search.

The alternative algorithm is Prim's Algorithm. It is chosen over Kruskal's Algorithm because path expansion of the Prim's is easier to implement constraints to prevent 2x2 open areas. This algorithm expands the maze by randomly selecting an unvisited cell adjacent to the current path and connecting them. \
Prim's Algorithm Workflow

1. Add the starting point (entry) to the visited set and add its adjacent cells to the options list.

2. Randomly pick a cell (current) from the options list.

3. Among the neighbors of the selected cell, randomly choose one that is already visited and break the wall to connect them.

4. Add the new cell to the visited and add its unvisited neighbors to the options list.

5. Repeat the process until the options list is empty.

### Reusability

The mazegen directory is a standalone module that can be integrated into any Python project. As it is mentioned above, `make build` build a reusable package from the directory. Maze generation and solving logic, which the module is responsible for, are entirely separated from the MLX display code. You can reuse the mazegen package by installing the built .whl file.

## Project Management
### What each member has done for this project
hmorita: Config file parse, Prim's maze generation, MiniLibX rendering, Makefile and setting files.
daogawa: DFS maze generation, BFS path search, terminal rendering(aborted), docstring.


## Resources

・Graph アルゴリズム入門：DFS/BFS などの探索アルゴリズム
https://qiita.com/Tadataka_Takahashi/items/90efc2fc862d32200a45
・【Pyxel】DFSを使ってランダムにダンジョンを生成する！
https://qiita.com/Prosamo/items/40f3847240f473edb209

42 Tokyoのプロジェクト報告書やREADMEに記載する「AI Usage（AI使用履歴）」として、適切で透明性の高い英語表現に翻訳しました。

AI Usage
In alignment with the project guidelines, AI tools (such as ChatGPT and GitHub Copilot) were utilized as supplementary aids for the following tasks. All AI-generated suggestions were thoroughly reviewed, verified, and understood before integration into the project.

Conceptual Understanding and Algorithm Selection:

Deepened understanding of the relationship between "Spanning Trees" in graph theory and maze generation.

Conducted a comparative analysis of the strengths and weaknesses of various algorithms (e.g., Prim’s Algorithm vs. Recursive Backtracker).

Testing and Debugging Support:

Consulted on design patterns, such as "effective testing strategies for sort functions" and "parsing logic," then implemented and refactored code based on these insights.

Used to interpret MyPy error messages and provide suggestions for correcting Type Hints.

Boilerplate Code Generation:

Streamlined repetitive, simple tasks and generated templates for documentation strings (docstrings) to improve development efficiency.