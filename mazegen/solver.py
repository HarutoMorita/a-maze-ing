from collections import deque as deq
from .maze import Maze


class MazeSolver:
    """Solves a maze using BFS to find paths from entry to exit."""

    _maze: Maze
    _dirs: list[tuple[int, int]]
    _dir_names: list[str]
    _wall_bits: list[int]

    def __init__(self, maze: Maze) -> None:
        """Initializes the solver with a maze instance."""
        self._maze = maze
        self._dirs = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        self._dir_names = ["N", "S", "E", "W"]
        self._wall_bits = [1, 4, 2, 8]

    def solve(self, count: int = 1) -> list[list[str]]:
        """Finds paths from entry to exit in the maze.

        Args:
            count: The maximum number of distinct paths to find.

        Returns:
            A list of paths, where each path is a list of direction strings.
        """
        all_paths: list[list[str]] = []
        queue: deq[tuple[int, int, list[str], set[tuple[int, int]]]] = deq([
            (self._maze.entry[0], self._maze.entry[1], [], {self._maze.entry})
        ])

        while queue and len(all_paths) < count:
            x, y, path, visited = queue.popleft()

            if (x, y) == self._maze.exit_:
                all_paths.append(path)
                continue

            for i in range(4):
                dx, dy = self._dirs[i]
                nx, ny = x + dx, y + dy

                if 0 <= nx < self._maze.width and 0 <= ny < self._maze.height:
                    if not (self._maze[y][x].value & self._wall_bits[i]):
                        if (nx, ny) not in visited:
                            new_path = path + [self._dir_names[i]]
                            new_visited = visited | {(nx, ny)}
                            queue.append((nx, ny, new_path, new_visited))
        return all_paths

    def apply_path_to_maze(self, path: list[str], bit: int) -> None:
        """Marks the cells along the given path using the specified bit.

        Args:
            path: A list of direction strings representing the route.
            bit: The bit flag to be added to each cell's value.
        """
        x, y = self._maze.entry
        self._maze[y][x].value |= bit
        for direction in path:
            if direction == "N":
                y -= 1
            elif direction == "S":
                y += 1
            elif direction == "E":
                x += 1
            elif direction == "W":
                x -= 1
            self._maze[y][x].value |= bit
