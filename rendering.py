from mazegen import Maze, Cell


class Renderer:

    def __init__(self) -> None:
        self._reset = "\033[0m"
        self._s = "\033[48;5;13m  \033[0m"
        self._g = "\033[48;5;196m  \033[0m"
        self._p1 = "\033[48;5;46m  \033[0m"
        self._p2 = "\033[48;5;208m  \033[0m"
        self._v = "\033[48;5;21m  \033[0m"

    def render(self, maze: Maze, wall_color: str, path_color: str) -> None:
        top: str = wall_color
        for cell in maze[0]:
            top += wall_color + (wall_color if cell.value & 1 else path_color)
        print(top)

        for r in range(maze.height):
            left_border = wall_color
            if (0, r) == maze.entry:
                left_border = wall_color
            elif (0, r) == maze.exit_:
                left_border = wall_color

            line_mid: str = left_border
            line_btm: str = wall_color

            for c in range(maze.width):
                cell = maze[r][c]
                cell_c = self._get_cell_color(maze, cell, c, r, path_color)
                line_mid += cell_c
                if cell.value & 2:
                    line_mid += wall_color
                else:
                    east_c = path_color
                    if c + 1 < maze.width:
                        nxt = maze[r][c + 1]
                        if (cell.value & 32) and (nxt.value & 32):
                            east_c = self._p1
                        elif (cell.value & 64) and (nxt.value & 64):
                            east_c = self._p2
                        elif cell.is_pattern and nxt.is_pattern:
                            east_c = self._v
                    line_mid += east_c

                if cell.value & 4:
                    line_btm += wall_color
                else:
                    south_c = path_color
                    if r + 1 < maze.height:
                        nxt = maze[r + 1][c]
                        if (cell.value & 32) and (nxt.value & 32):
                            south_c = self._p1
                        elif (cell.value & 64) and (nxt.value & 64):
                            south_c = self._p2
                        elif cell.is_pattern and nxt.is_pattern:
                            south_c = self._v
                    line_btm += south_c
                line_btm += wall_color

            print(line_mid)
            print(line_btm)

    def _get_cell_color(
        self, maze: Maze, cell: Cell, x: int, y: int, default: str
    ) -> str:
        if (x, y) == maze.entry:
            return self._s
        if (x, y) == maze.exit_:
            return self._g
        if getattr(cell, 'is_pattern', False):
            return self._v
        if cell.value & 32:
            return self._p1
        if cell.value & 64:
            return self._p2
        if (cell.value & 16) and (cell.value & 15):
            return self._v
        return default

    def display(self, maze: Maze, invert: bool = False) -> None:
        white: str = "\033[48;5;255m  \033[0m"
        black: str = "\033[48;5;232m  \033[0m"

        if invert:
            self.render(maze, black, white)
        else:
            self.render(maze, white, black)
