#!/usr/bin/env python3
import sys
import signal
from typing import Iterator, Any
from config import Config, InvalidFormat
try:
    from mlx import Mlx
    from mazegen import MazeGenerator, MazeSolver, Maze, Cell
except ImportError as e:
    print(f"Critical Error: Missing dependency -> {e.name}", file=sys.stderr)
    print("Do 'make/make install' first.", file=sys.stderr)
    sys.exit(1)


class MlxMazeDisplay:
    """Handles only the visual rendering of the maze using MLX."""

    mlx: Mlx
    m_ptr: int
    c_size: int
    w_ptr: int
    palettes: list[int]
    pal_idx: int
    colors: dict[str, int]

    def __init__(
        self, mlx: Mlx, m_ptr: int, width: int, height: int, title: str
    ) -> None:
        """Initializes the display window and color palettes."""
        self.mlx = mlx
        self.m_ptr = m_ptr
        self.c_size = 20

        self.w_ptr = self.mlx.mlx_new_window(
            m_ptr, width * self.c_size + 1,
            height * self.c_size + 1,
            title
        )
        self.palettes = [0xFFFFFFFF, 0xFF00FFFF, 0xFFFFFF00]
        self.pal_idx = 0
        self.colors = {
            "WALL": self.palettes[self.pal_idx], "BG": 0xFF000000,
            "ENT": 0xFFFF00FF, "EXT": 0xFFFF0000, "PAT": 0xFF104E8B,
            "P1": 0xFF008000, "P2": 0xFFCC7000,
        }

    def render(self, maze: Maze) -> None:
        """Draws the entire maze structure and state to the window."""
        self.mlx.mlx_clear_window(self.m_ptr, self.w_ptr)
        for y in range(maze.height):
            for x in range(maze.width):
                self._draw_cell(x, y, maze[y][x])

    def rotate_colors(self) -> None:
        """Cycles through the wall color palette."""
        self.pal_idx = (self.pal_idx + 1) % len(self.palettes)
        self.colors["WALL"] = self.palettes[self.pal_idx]

    def _draw_cell(self, x: int, y: int, cell: Cell) -> None:
        """Draws a single maze cell and its four potential walls."""
        x0, y0 = x * self.c_size, y * self.c_size
        color: int = self.colors["BG"]
        if cell.is_entry:
            color = self.colors["ENT"]
        elif cell.is_exit:
            color = self.colors["EXT"]
        elif cell.is_pattern:
            color = self.colors["PAT"]
        elif cell.value & 32:
            color = self.colors["P1"]
        elif cell.value & 64:
            color = self.colors["P2"]

        for i in range(1, self.c_size):
            for j in range(1, self.c_size):
                self.mlx.mlx_pixel_put(
                    self.m_ptr, self.w_ptr, x0 + i, y0 + j, color
                )

        c_wall: int = self.colors["WALL"]
        if cell.value & 1:
            for i in range(self.c_size + 1):
                self.mlx.mlx_pixel_put(
                    self.m_ptr, self.w_ptr, x0 + i, y0, c_wall)
        if cell.value & 2:
            for i in range(self.c_size + 1):
                self.mlx.mlx_pixel_put(
                    self.m_ptr, self.w_ptr, x0 + self.c_size, y0 + i, c_wall)
        if cell.value & 4:
            for i in range(self.c_size + 1):
                self.mlx.mlx_pixel_put(
                    self.m_ptr, self.w_ptr, x0 + i, y0 + self.c_size, c_wall)
        if cell.value & 8:
            for i in range(self.c_size + 1):
                self.mlx.mlx_pixel_put(
                    self.m_ptr, self.w_ptr, x0, y0 + i, c_wall)


class MazeApp:
    """Main controller managing data, logic, and rendering coordination."""

    cfg: Config
    mlx: Mlx
    m_ptr: int
    maze: Maze
    anim_it: Iterator[None] | None
    show_p: bool
    display: MlxMazeDisplay

    def __init__(self, config: Config) -> None:
        """Initializes the application with the given configuration."""
        self.cfg = config
        self.mlx = Mlx()
        self.m_ptr = self.mlx.mlx_init()
        self.anim_it = None
        self.show_p = False
        self._print_guide()
        self._setup(animate=False)

    def _print_guide(self) -> None:
        """Prints a clean, formatted guide to the terminal."""
        print("----- Click window, then press the following keys -----")
        print("1: Regenerate a new maze.")
        print("2: Show/Hide path from entry to exit.")
        print("3: Change wall color.")
        print("4: Regenerate a new maze with animation.")
        print("Esc: Exit immediately.\n")

    def _str_maze_info(self) -> str:
        """Returns a formatted string describing the current maze config."""
        perf_str = "Perfect" if self.cfg.perfect else "Not-perfect"
        algo_str = "DFS" if self.cfg.algo == "DFS" else "Prim"
        return (f"{self.cfg.width}x{self.cfg.height} "
                f"{perf_str} {algo_str}")

    def _setup(self, animate: bool = False) -> None:
        """Initializes a new maze generation and window based on config."""
        self.show_p = False
        self.cfg.seed = None
        self.cfg.load_config()

        if hasattr(self, 'display') and self.display.w_ptr:
            self.mlx.mlx_destroy_window(self.m_ptr, self.display.w_ptr)

        gen = MazeGenerator(
            self.cfg.width, self.cfg.height, self.cfg.entry, self.cfg.exit,
            self.cfg.perfect, self.cfg.seed, self.cfg.algo
        )
        maze_data = self._str_maze_info()
        if animate:
            self.anim_it = gen.generate(animate=True)
        else:
            gen.generate(animate=False)
            self.anim_it = None
            self._save_maze(gen.maze)
            print(f"Generated: {maze_data} Maze")
        self.maze = gen.maze

        self.display = MlxMazeDisplay(
            self.mlx, self.m_ptr, self.maze.width, self.maze.height,
            maze_data
        )
        self.mlx.mlx_key_hook(
            self.display.w_ptr, self._key_handler, None
        )
        self.mlx.mlx_hook(
            self.display.w_ptr, 33, 0, self._exit_handler, None
        )

    def _save_maze(self, maze_to_save: Maze) -> None:
        """Saves current maze data and solution path to the output file."""
        solver = MazeSolver(maze_to_save)
        paths = solver.solve(count=1)
        path_str = "".join(paths[0]) if paths else ""
        try:
            with open(self.cfg.output_file, 'w', encoding='utf-8') as f:
                f.write(f"{maze_to_save}\n\n")
                f.write(f"{self.cfg.entry[0]},{self.cfg.entry[1]}\n")
                f.write(f"{self.cfg.exit[0]},{self.cfg.exit[1]}\n")
                f.write(f"{path_str}\n")
        except (PermissionError, OSError) as e:
            print(f"File save error: {e}", file=sys.stderr)

    def _toggle_path(self) -> None:
        """Toggles the visibility of the solution path in the maze."""
        self.show_p = not self.show_p
        if self.show_p:
            solver = MazeSolver(self.maze)
            paths = solver.solve(count=(1 if self.cfg.perfect else 2))
            bits = [32, 64]
            for i, p in enumerate(paths):
                if i < len(bits):
                    solver.apply_path_to_maze(p, bits[i])
        else:
            self.maze.clear_all_paths()

    def _exit_handler(self, params: Any) -> None:
        """Handles the window close event and initiates app termination."""
        if hasattr(self, 'display') and self.display.w_ptr:
            self.mlx.mlx_destroy_window(self.m_ptr, self.display.w_ptr)
            self.display.w_ptr = 0
        self.mlx.mlx_loop_exit(self.m_ptr)

    def _key_handler(self, key: int, param: Any) -> None:
        """Processes keyboard input using standard instance method."""
        try:
            if key == 65307:
                self._exit_handler(None)
            elif key == ord('1'):
                self._setup(animate=False)
                self.display.render(self.maze)
            elif key == ord('2'):
                self._toggle_path()
                self.display.render(self.maze)
            elif key == ord('3'):
                self.display.rotate_colors()
                self.display.render(self.maze)
            elif key == ord('4'):
                self._setup(animate=True)
        except Exception as e:
            print(f"Config error: {e}", file=sys.stderr)

    def _loop_handler(self, param: Any) -> None:
        """Processes animation steps during MLX idle time."""
        if self.anim_it:
            try:
                next(self.anim_it)
                self.display.render(self.maze)
            except StopIteration:
                self.anim_it = None
                self._save_maze(self.maze)
                print(f"Generated: {self._str_maze_info()} Maze")
            except Exception as e:
                print(f"Animation error: {e}", file=sys.stderr)
                self.anim_it = None

    def run(self) -> None:
        """Runs the MLX application loop."""
        self.mlx.mlx_loop_hook(self.m_ptr, self._loop_handler, None)
        self.display.render(self.maze)
        self.mlx.mlx_loop(self.m_ptr)
        self.mlx.mlx_release(self.m_ptr)
        sys.exit(0)


def sigint_handler(sig: int, frame: Any) -> None:
    """Display messages when Ctrl+C is sent to the program"""
    print("\nCtrl+C is disabled during MLX loop.", file=sys.stderr)
    print("Click window, then press 'Esc' to exit safely.", file=sys.stderr)
    print("Or press 'Ctrl + \\' to force kill (Core Dump).", file=sys.stderr)


def main() -> None:
    """Entry point with robust error handling for various failure modes."""
    signal.signal(signal.SIGINT, sigint_handler)
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <config_file>", file=sys.stderr)
        sys.exit(1)
    try:
        setting = Config(sys.argv[1])
        app = MazeApp(setting)
        app.run()
    except (InvalidFormat, ValueError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(1)
    except (FileNotFoundError, PermissionError) as e:
        print(f"File error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Critical error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
