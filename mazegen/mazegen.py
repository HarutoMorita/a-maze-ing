#!/usr/bin/env python3
import random
import sys


class Cell:
    """
    A single maze cell.

    Each cell is encoded into a hex digit based on its walls.
    Bit 0 for North wall, bit 1 for East, bit 2 for South, bit 3 for West.
    For example, 9 represents a cell with walls on North(1) and West(8)


    Attributes:
        value (int): The hex value representing each wall's status.
        is_entry (bool): If the cell is entry.
        is_exit (bool): If the cell is exit.
        is_pattern (bool): If the cell is the part of pattern.
        is_path (bool): If the cell is the part of path.
    """
    WALL_BITS = {'N': 1 << 0, 'E': 1 << 1, 'S': 1 << 2, 'W': 1 << 3}

    value: int
    is_entry: bool
    is_exit: bool
    is_pattern: bool
    is_path: bool

    def __init__(self):
        self.value = 0xF
        self.is_entry = False
        self.is_exit = False
        self.is_pattern = False
        self.is_path = False

    def remove_wall(self, direction: str) -> None:
        if direction in self.WALL_BITS:
            self.value &= ~self.WALL_BITS[direction]


class Maze:
    """
    A rectangular maze grid.


    Attributes:
        width (int): Width of the maze in number of cells.
        height (int): Height of the maze in number of cells.
        entry (tuple[int, int]): Entry cell coordinates (row, col).
        exit (tuple[int, int]): Exit cell coordinates (row, col).
        grid (list[list[Cell]]): 2D grid of maze cells.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    grid: list[list[Cell]]

    def __init__(
        self, width: int, height: int,
        entry: tuple[int, int], exit_: tuple[int, int]
    ):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.get_cell(entry).is_entry = True
        self.get_cell(exit_).is_exit = True

    def get_cell(self, pos: tuple[int, int]) -> Cell:
        """Return the cell at the given position.

        Args:
            pos (tuple[int, int]): Cell position(row, col).

        Returns:
            Cell: The cell located at the passed position.
        """
        x, y = pos
        return self.grid[y][x]

    def open_wall(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
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
        cell1 = self.get_cell(pos1)
        cell2 = self.get_cell(pos2)

        if y1 > y2:
            cell1.remove_wall('N')
            cell2.remove_wall('S')
        elif x1 < x2:
            cell1.remove_wall('E')
            cell2.remove_wall('W')
        elif y1 < y2:
            cell1.remove_wall('S')
            cell2.remove_wall('N')
        elif x1 > x2:
            cell1.remove_wall('W')
            cell2.remove_wall('E')

    def __str__(self) -> str:
        return "\n".join(
            "".join(format(c.value, 'x') for c in row)
            for row in self.grid
        )


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
    _is_re: bool

    def __init__(
        self, width: int, height: int,
        entry: tuple[int, int], exit_: tuple[int, int],
        perfect: bool = True, seed: int | None = None,
        algo: str | None = None
    ):
        self._width = width
        self._height = height
        self._entry = entry
        self._exit = exit_
        self._perfect = perfect
        self._initial_seed = seed
        self._seed = random.Random(seed)
        self._algo = algo
        self._is_re = False

    def _make_pattern(self) -> set[tuple[int, int]]:
        """Return coordinates forming a '42' pattern.

        The pattern uses only horizontal and vertical strokes
        and is centered inside the maze.

        Returns:
            set[tuple[int, int]]: Set of (row, col) positions for pattern.
        """
        pattern = [
            [1, 0, 0, 0, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [0, 0, 1, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 1],
        ]

        pat_height = len(pattern)
        pat_width = len(pattern[0])

        if self._height < pat_height + 1 or self._width < pat_width + 2:
            print(f"Error: the '42' pattern is omitted "
                  f"because the {self._width}x{self._height} maze is "
                  f"too small to have it",
                  file=sys.stderr)
            return set()

        offset_y = (self._height - pat_height) // 2
        offset_x = (self._width - pat_width) // 2

        pattern_pos: set[tuple[int, int]] = set()

        for py in range(pat_height):
            for px in range(pat_width):
                if pattern[py][px]:
                    pattern_pos.add((offset_x + px, offset_y + py))
        if self._entry in pattern_pos:
            print(f"Error: the '42' pattern is omitted "
                  f"because it covers the entry position {self._entry}",
                  file=sys.stderr)
            return set()
        if self._exit in pattern_pos:
            print(f"Error: the '42' pattern is omitted "
                  f"because it covers the exit position {self._exit}",
                  file=sys.stderr)
            return set()

        for pos in pattern_pos:
            self._grid.get_cell(pos).is_pattern = True

        return pattern_pos

    def generate(self) -> Maze:
        """Generates a maze using Prim's algorithm.

        Returns:
            Maze: The generated maze object.
        """
        self._grid = Maze(self._width, self._height, self._entry, self._exit)
        self._pattern = self._make_pattern()
        if self._initial_seed is not None:
            self._seed = random.Random(self._initial_seed)
        else:
            pass

        visited: set[tuple[int, int]] = set()
        options: list[tuple[int, int]] = []

        start = self._entry
        visited.add(start)
        self._add_options(start, visited, options)

        while options:
            current = self._seed.choice(options)
            options.remove(current)
            if current in visited:
                continue

            neighbors = self._get_visited_neighbors(current, visited)
            if not neighbors:
                continue

            neighbor = self._seed.choice(neighbors)
            self._grid.open_wall(current, neighbor)

            visited.add(current)
            self._add_options(current, visited, options)

        if not self._perfect:
            self._add_loops()

        return self._grid

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
            pos_nei for pos_nei in self._get_neighbors(pos)
            if pos_nei in visited and pos_nei not in self._pattern
        ]

    def _get_neighbors(
        self, pos: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """Finds all valid adjacent cells within the maze boundaries.

        Args:
            pos: Target cell coordinates.

        Returns:
            list[tuple[int, int]]: List of valid neighbor coordinates.
        """
        x, y = pos
        neighbors = [
            (x, y - 1), (x, y + 1),
            (x - 1, y), (x + 1, y),
        ]
        return [
            (nx, ny)
            for nx, ny in neighbors
            if 0 <= nx < self._width and 0 <= ny < self._height
        ]

    def _add_loops(self) -> None:
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
        limit = (self._width * self._height) // 20
        broken = 0

        for pos1, pos2 in adjacent_pairs:
            if broken >= limit:
                break
            if pos1 in self._pattern or pos2 in self._pattern:
                continue
            if self._is_closed(pos1, pos2):
                if self._is_breakable(pos1, pos2):
                    self._grid.open_wall(pos1, pos2)
                    broken += 1

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
        cell1: Cell = self._grid.get_cell(pos1)
        cell2: Cell = self._grid.get_cell(pos2)
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
        left_top = self._grid.get_cell((x, y))
        right_top = self._grid.get_cell((x + 1, y))
        left_bot = self._grid.get_cell((x, y + 1))
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

    def _is_breakable(
            self, pos1: tuple[int, int], pos2: tuple[int, int]
    ) -> bool:
        """Checks if a wall can be broken without creating 2x2 area.

        Args:
            pos1: First cell coordinates.
            pos2: Second cell coordinates.

        Returns:
            bool: True if breaking the wall is not making 2x2 area.
        """

        x1, y1 = pos1
        x2, y2 = pos2
        if y1 < y2:
            if x1 > 0 and self._check_2x2(x1 - 1, y1):
                return False
            if x1 < self._width - 1 and self._check_2x2(x1, y1):
                return False
        else:
            if y1 > 0 and self._check_2x2(x1, y1 - 1):
                return False
            if y1 < self._height - 1 and self._check_2x2(x1, y1):
                return False

        return True
