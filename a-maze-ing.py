#!/usr/bin/env python3
import sys
import config
from mazegen import Maze, MazeGenerator


def print_maze(maze) -> None:
    print(" " + "--- " * maze.width)

    for row in range(maze.height):
        line_cells = "|"
        for col in range(maze.width):
            cell = maze.get_cell((row, col))
            line_cells += "   "
            line_cells += "|" if cell.east else " "
        print(line_cells)

        line_walls = " "
        for col in range(maze.width):
            cell = maze.get_cell((row, col))
            line_walls += "--- " if cell.south else "    "
        print(line_walls)


def main() -> None:
    argc = len(sys.argv)
    if argc == 1:
        print("No config file provided. ", end="")
        print("Usage: python3 a-maze-ing.py <config text file>")
    else:
        try:
            setting = config.Config(sys.argv[1])
            print(setting.width, setting.height, setting.entry, setting.exit,
                  setting.perfect, setting.output_file)
            mazegen = MazeGenerator(
                setting.width, setting.height,
                setting.entry, setting.exit, setting.perfect, 5)
            maze: Maze = mazegen.generate()
            print_maze(maze)
        except config.InvalidFormat as e:
            print(f"Config invalid format: {e}", file=sys.stderr)
        except ValueError as e:
            print(f"Config invalid values: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
