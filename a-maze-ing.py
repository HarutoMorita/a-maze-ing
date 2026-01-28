#!/usr/bin/env python3
import sys
import time
from config import Config, InvalidFormat
from mazegen import MazeGenerator, MazeSolver, Maze
from rendering import Renderer


def save_maze(config: Config, maze: Maze) -> None:
    solver = MazeSolver(maze)
    paths: list[list[str]] = solver.solve(count=1)
    path_str: str = "".join(paths[0]) if paths else ""
    try:
        with open(config.output_file, 'w', encoding='utf-8') as f:

            f.write(f"{maze}\n\n")
            f.write(f"{config.entry[0]} {config.entry[1]}\n")
            f.write(f"{config.exit[0]} {config.exit[1]}\n")
            f.write(f"{path_str}\n")
    except Exception as e:
        print(f"Save failed: {e}", file=sys.stderr)


def choice_prompt() -> int | None:
    print("=== A-Maze-ing ===")
    print("1. Re-generate a new maze")
    print("2. Show/Hide path from entry to exit")
    print("3. Rotate maze colors")
    print("4. Re-generate a new maze with animation.")
    print("5. Quit")
    line = input("Choice? (1-5): ")
    if not line:
        return None
    try:
        return int(line)
    except ValueError:
        raise ValueError("Invalid input. Please enter a number.\n")


def run_terminal(setting: Config, mazegen: MazeGenerator) -> None:
    renderer = Renderer()
    invert_color: bool = False
    show_path: bool = False
    gen_iter = mazegen.generate()
    list(gen_iter)
    save_maze(setting, mazegen.maze)
    renderer.display(mazegen.maze, invert=invert_color)
    while True:
        try:
            choice = choice_prompt()
        except ValueError as e:
            print(e)
            continue

        if choice is None:
            continue
        if not (1 <= choice <= 5):
            print("Please input a number between 1 and 5.\n")
            continue
        else:
            if choice in [1, 4]:
                show_path = False
                gen_iter = mazegen.generate()
                if choice == 1:
                    list(gen_iter)
                    renderer.display(mazegen.maze, invert=invert_color)
                else:
                    for _ in gen_iter:
                        print("\033[H\033[2J", end="")
                        renderer.display(mazegen.maze, invert=invert_color)
                        time.sleep(0.02)
            save_maze(setting, mazegen.maze)
            if choice == 2:
                show_path = not show_path
                if show_path:
                    solver = MazeSolver(mazegen.maze)
                    path_count: int = 1 if setting.perfect else 2
                    paths = solver.solve(count=path_count)
                    bits = [32, 64]
                    for i, p in enumerate(paths):
                        if i < len(bits):
                            solver.apply_path_to_maze(p, bits[i])
                else:
                    for row in mazegen.maze:
                        for cell in row:
                            cell.value &= ~96

                renderer.display(mazegen.maze, invert=invert_color)
            if choice == 3:
                invert_color = not invert_color
                renderer.display(mazegen.maze, invert=invert_color)
            if choice == 5:
                break


def main() -> None:
    argc = len(sys.argv)
    if argc == 1:
        print("No config file provided. ", end="")
        print("Usage: python3 a-maze-ing.py <config text file>")
        sys.exit(1)
    else:
        try:
            setting = Config(sys.argv[1])
            mazegen = MazeGenerator(
                setting.width, setting.height,
                setting.entry, setting.exit, setting.perfect,
                setting.seed, setting.algo)
            run_terminal(setting, mazegen)

        except (InvalidFormat, ValueError) as e:
            print(f"Config error: {e}", file=sys.stderr)
            sys.exit(1)
        except (FileNotFoundError, PermissionError) as e:
            print(f"File error: {e}", file=sys.stderr)
            sys.exit(1)
        except (KeyboardInterrupt, EOFError):
            print("\nInterrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"Fatal error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
