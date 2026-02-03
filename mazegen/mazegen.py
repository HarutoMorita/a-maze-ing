import random
import sys
from .maze import Cell, Maze
from typing import Iterator


class MazeGenerator:
    """Maze generator controller.

    This class handles maze generation logic and produces a Maze instance
    based on given parameters.

    Attributes:
        _width (int): Width of the maze in number of cells.
        _height (int): Height of the maze in number of cells.
        _entry (tuple[int, int]): Entry cell position (row, col).
        _exit (tuple[int, int]): Exit cell position (row, col).
        _perfect (bool): Whether the generated maze is perfect.
        _seed (int | None): Random seed for maze generation.
        _grid (Maze): Generated maze structure.
    """

    _width: int
    _height: int
    _entry: tuple[int, int]
    _exit: tuple[int, int]
    _perfect: bool
    _seed: random.Random
    _grid: Maze
    _pattern: set[tuple[int, int]]
    _algo: str | None

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        perfect: bool = True,
        seed: int | None = None,
        algo: str | None = None,
    ):
        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit_
        self._perfect = perfect
        self._initial_seed = seed
        self._seed = random.Random(seed)
        self._algo = algo
        self._grid: Maze = Maze(width, height, entry, exit_)

    @property
    def maze(self) -> Maze:
        return self._grid

    def generate(self, animate: bool = False) -> Iterator[None] | None:
        self._grid = Maze(self._width, self._height, self._entry, self._exit)
        self._pattern = self._make_pattern()
        if self._initial_seed is not None:
            self._seed = random.Random(self._initial_seed)

        def generation_iter() -> Iterator[None]:
            if self._algo == "DFS":
                yield from self.generate_dfs_step()
            else:
                yield from self.generate_prim_step()

            if not self._perfect:
                yield from self._add_loops_step()
        gen = generation_iter()
        if animate:
            return gen
        else:
            for _ in gen:
                pass
            return None

    def generate_dfs_step(self) -> Iterator[None]:
        dirs: list[tuple[int, int]] = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        stack: list[tuple[int, int]] = [self._entry]
        visited: set[tuple[int, int]] = {self._entry}

        while stack:
            x, y = stack[-1]
            neighbors: list[int] = []

            for i, (dx, dy) in enumerate(dirs):
                nx, ny = x + dx, y + dy
                if (0 <= nx < self._width and 0 <= ny < self._height and
                        (nx, ny) not in self._pattern and
                        (nx, ny) not in visited):
                    neighbors.append(i)

            if neighbors:
                idx: int = self._seed.choice(neighbors)
                dx, dy = dirs[idx]
                nx, ny = x + dx, y + dy
                self._open_wall((x, y), (nx, ny))

                visited.add((nx, ny))
                stack.append((nx, ny))

                yield None
            else:
                stack.pop()
                yield None

    def _make_pattern(self) -> set[tuple[int, int]]:
        """Return coordinates forming a '42' pattern.

        The pattern uses only horizontal and vertical strokes
        and is centered inside the maze.

        Returns:
            set[tuple[int, int]]: Set of (row, col) positions for pattern.
        """
        pattern: list[list[int]] = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        pat_height = len(pattern)
        pat_width = len(pattern[0])

        if self._height < pat_height + 1 or self._width < pat_width + 2:
            print(
                f"Error: the '42' pattern is omitted "
                f"because the {self._width}x{self._height} maze is "
                f"too small to have it",
                file=sys.stderr,
            )
            return set()

        offset_y = (self._height - pat_height) // 2
        offset_x = (self._width - pat_width) // 2

        pattern_pos: set[tuple[int, int]] = set()

        for py in range(pat_height):
            for px in range(pat_width):
                if pattern[py][px]:
                    pattern_pos.add((offset_x + px, offset_y + py))
        if self._entry in pattern_pos:
            print(
                f"Error: the '42' pattern is omitted "
                f"because it covers the entry position {self._entry}",
                file=sys.stderr,
            )
            return set()
        if self._exit in pattern_pos:
            print(
                f"Error: the '42' pattern is omitted "
                f"because it covers the exit position {self._exit}",
                file=sys.stderr,
            )
            return set()

        for x, y in pattern_pos:
            self._grid[y][x].is_pattern = True

        return pattern_pos

    def _open_wall(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
        """Open the wall between two adjacent cells.

        The wall is opened only if the two positions are
        vertically or horizontally adjacent.
        If the cells are not adjacent, nothing happens.

        Args:
            pos1 (tuple[int, int]): Position of the first cell(row, col).
            pos2 (tuple[int, int]): Position of the second cell(row, col).
        """
        x1, y1 = pos1
        x2, y2 = pos2
        if abs(x1 - x2) + abs(y1 - y2) != 1:
            return
        cell1: Cell = self._grid[y1][x1]
        cell2: Cell = self._grid[y2][x2]

        if y1 > y2:
            cell1.remove_wall("N")
            cell2.remove_wall("S")
        elif x1 < x2:
            cell1.remove_wall("E")
            cell2.remove_wall("W")
        elif y1 < y2:
            cell1.remove_wall("S")
            cell2.remove_wall("N")
        elif x1 > x2:
            cell1.remove_wall("W")
            cell2.remove_wall("E")

    def generate_prim_step(self) -> Iterator[None]:
        """Generates a maze using Prim's algorithm.

        Returns:
            Maze: The generated maze object.
        """
        visited: set[tuple[int, int]] = {self._entry}
        options: list[tuple[int, int]] = []

        self._add_options(self._entry, visited, options)

        while options:
            current = self._seed.choice(options)
            options.remove(current)
            if current in visited:
                continue

            neighbors = self._get_visited_neighbors(current, visited)
            if not neighbors:
                continue

            neighbor = self._seed.choice(neighbors)
            self._open_wall(current, neighbor)

            visited.add(current)
            self._add_options(current, visited, options)

            yield None

        if not self._perfect:
            self._add_loops_step()
            yield None

    def _add_options(
        self,
        pos: tuple[int, int],
        visited: set[tuple[int, int]],
        options: list[tuple[int, int]],
    ) -> None:
        """Adds unvisited neighbors of a cell to the options list.

        Args:
            pos: Current cell coordinates.
            visited: Set of already visited cells.
            options: List of potential cells to connect next.
        """
        for neighbor in self._get_neighbors(pos):
            if neighbor not in visited and neighbor not in self._pattern:
                options.append(neighbor)

    def _get_visited_neighbors(
        self,
        pos: tuple[int, int],
        visited: set[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        """Returns neighbors of a cell that have already been visited.

        Args:
            pos: Target cell coordinates.
            visited: Set of visited cells.

        Returns:
            list[tuple[int, int]]: List of visited neighbor coordinates.
        """
        return [
            pos_nei
            for pos_nei in self._get_neighbors(pos)
            if pos_nei in visited and pos_nei not in self._pattern
        ]

    def _get_neighbors(self, pos: tuple[int, int]) -> list[tuple[int, int]]:
        """Finds all valid adjacent cells within the maze boundaries.

        Args:
            pos: Target cell coordinates.

        Returns:
            list[tuple[int, int]]: List of valid neighbor coordinates.
        """
        x, y = pos
        neighbors = [
            (x, y - 1),
            (x, y + 1),
            (x - 1, y),
            (x + 1, y),
        ]
        return [
            (nx, ny)
            for nx, ny in neighbors
            if 0 <= nx < self._width and 0 <= ny < self._height
        ]

    def _add_loops_step(self) -> Iterator[None]:
        """Adds loops to make the maze imperfect.

        It opens some walls without creating 2x2 area.
        """
        adjacent_pairs = []
        for y in range(self._height):
            for x in range(self._width):
                if y < self._height - 1:
                    adjacent_pairs.append(((x, y), (x, y + 1)))
                if x < self._width - 1:
                    adjacent_pairs.append(((x, y), (x + 1, y)))

        self._seed.shuffle(adjacent_pairs)
        limit = (self._width * self._height) // 10
        broken = 0

        for pos1, pos2 in adjacent_pairs:
            if broken >= limit:
                break
            if pos1 in self._pattern or pos2 in self._pattern:
                continue
            if self._is_closed(pos1, pos2):
                if self._is_breakable(pos1, pos2):
                    self._open_wall(pos1, pos2)
                    broken += 1
                    yield None

    def _is_closed(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
        """Checks if a wall exists between two adjacent cells.

        Args:
            pos1: First cell coordinates.
            pos2: Second cell coordinates.

        Returns:
            bool: True if the wall is closed, False otherwise.
        """
        x1, y1 = pos1
        x2, y2 = pos2
        cell1: Cell = self._grid[y1][x1]
        cell2: Cell = self._grid[y2][x2]
        if y1 < y2:
            return bool(cell1.value & (1 << 2))
        if y1 > y2:
            return bool(cell2.value & (1 << 2))
        if x1 < x2:
            return bool(cell1.value & (1 << 1))
        if x1 > x2:
            return bool(cell2.value & (1 << 1))
        return False

    def _check_2x2(self, x: int, y: int) -> bool:
        """Checks if breaking a wall creates a 2x2 area.

        Args:
            row: Top-left row index of the 2x2 area.
            col: Top-left column index of the 2x2 area.

        Returns:
            bool: True if three or more walls are already open in the 2x2 area.
        """
        left_top: Cell = self._grid[y][x]
        right_top: Cell = self._grid[y][x + 1]
        left_bot: Cell = self._grid[y + 1][x]
        counter = 0
        if not (left_top.value & (1 << 1)):
            counter += 1
        if not (left_top.value & (1 << 2)):
            counter += 1
        if not (right_top.value & (1 << 2)):
            counter += 1
        if not (left_bot.value & (1 << 1)):
            counter += 1
        return counter >= 3

    def _is_breakable(self,
                      pos1: tuple[int, int], pos2: tuple[int, int]) -> bool:
        """Checks if a wall can be broken without creating 2x2 area.

        Args:
            pos1: First cell coordinates.
            pos2: Second cell coordinates.

        Returns:
            bool: True if breaking the wall is not making 2x2 area.
        """

        x1, y1 = pos1
        x2, y2 = pos2
        if x1 == x2:
            top_y = min(y1, y2)
            if x1 > 0 and self._check_2x2(x1 - 1, top_y):
                return False
            if x1 < self._width - 1 and self._check_2x2(x1, top_y):
                return False
        elif y1 == y2:
            left_x = min(x1, x2)
            if y1 > 0 and self._check_2x2(left_x, y1 - 1):
                return False
            if y1 < self._height - 1 and self._check_2x2(left_x, y1):
                return False

        return True
