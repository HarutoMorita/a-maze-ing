#!/usr/bin/env python3
import sys
import time
from config import Config, InvalidFormat
from mazegen import MazeGenerator, MazeSolver
from rendering import Renderer


def main() -> None:
    argc = len(sys.argv)
    if argc == 1:
        print("No config file provided. ", end="")
        print("Usage: python3 a-maze-ing.py <config text file>")
    else:
        try:
            setting = Config(sys.argv[1])
            mazegen = MazeGenerator(
                setting.width, setting.height,
                setting.entry, setting.exit, setting.perfect,
                setting.seed, setting.algo)
        except InvalidFormat as e:
            print(f"Config invalid format: {e}", file=sys.stderr)
        except ValueError as e:
            print(f"Config invalid values: {e}", file=sys.stderr)
        except FileNotFoundError as e:
            print(f"{e}", file=sys.stderr)

        renderer = Renderer()
        invert_color: bool = False
        show_path: bool = False
        mazegen.generate()
        renderer.display(mazegen.maze, invert=invert_color)
        while True:
            print("=== A-Maze-ing ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide path from entry to exit")
            print("3. Rotate maze colors")
            print("4. Quit")
            print("5. animation of maze generation.")
            try:
                line = input("Choice? (1-4): ")
                if not line:
                    continue
                choice: int = int(line)
                if not (1 <= choice <= 5):
                    print("Please input a number between 1 and 4")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            except Exception as e:
                print(e)
                break
            else:
                if choice in [1, 5]:
                    show_path = False
                    gen_iter = mazegen.generate()

                    if choice == 1:
                        list(gen_iter)
                        renderer.display(mazegen.maze, invert=invert_color)
                    else:
                        for _ in gen_iter:
                            print("\033[H\033[J", end="")
                            renderer.display(mazegen.maze, invert=invert_color)
                            time.sleep(0.02)

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
                if choice == 4:
                    break


if __name__ == "__main__":
    main()
