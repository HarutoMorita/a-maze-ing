#!/usr/bin/env python3
import random
import sys


class Cell:
    """
    A single maze cell.

    Each cell has up to four walls, one for each direction.
    A wall is True if closed, False if open.

    Attributes:
        north (bool): If the north wall is closed.
        east (bool): If the east wall is closed.
        south (bool): If the south wall is closed.
        west (bool): If the west wall is closed.
    """

    north: bool
    east: bool
    south: bool
    west: bool

    def __init__(
        self, north: bool, east: bool, south: bool, west: bool
    ):
        self.north = north
        self.east = east
        self.south = south
        self.west = west


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
        self.grid = [
            [Cell(True, True, True, True) for _ in range(width)]
            for _ in range(height)
        ]

    def get_cell(self, pos: tuple[int, int]) -> Cell:
        """Return the cell at the given position.

        Args:
            pos (tuple[int, int]): Cell position(row, col).

        Returns:
            Cell: The cell located at the passed position.
        """
        row, col = pos
        return self.grid[row][col]

    def open_wall(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
        """Open the wall between two adjacent cells.

        The wall is opened only if the two positions are
        vertically or horizontally adjacent.
        If the cells are not adjacent, nothing happens.

        Args:
            pos1 (tuple[int, int]): Position of the first cell(row, col).
            pos2 (tuple[int, int]): Position of the second cell(row, col).
        """
        row1, col1 = pos1
        row2, col2 = pos2
        if abs(row1 - row2) + abs(col1 - col2) != 1:
            return
        cell1 = self.get_cell(pos1)
        cell2 = self.get_cell(pos2)

        if col1 + 1 == col2:
            cell1.east = False
            cell2.west = False
        elif col1 - 1 == col2:
            cell1.west = False
            cell2.east = False
        elif row1 + 1 == row2:
            cell1.south = False
            cell2.north = False
        elif row1 - 1 == row2:
            cell1.north = False
            cell2.south = False

    def to_hex_str(self) -> str:
        """Converts the maze structure into a hexadecimal string.

        Each cell is encoded into a hex digit based on its walls.
        Bit 0 for North wall, bit 1 for East, bit 2 for South, bit 3 for West.
        For example, 9 represents a cell with walls on North(1) and West(8)
        Rows are separated by newlines.

        Returns:
            str: The maze encoded as hexadecimal digits.
        """
        lines = []
        for row in range(self.height):
            row_data = []
            for col in range(self.width):
                cell = self.get_cell((row, col))

                val = 0
                if cell.north:
                    val |= (1 << 0)
                if cell.east:
                    val |= (1 << 1)
                if cell.south:
                    val |= (1 << 2)
                if cell.west:
                    val |= (1 << 3)

                row_data.append(format(val, 'x'))

            lines.append("".join(row_data))

        return "\n".join(lines)


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
        self._seed = random.Random(seed)
        self._grid = Maze(width, height, entry, exit_)
        self._pattern = self._make_pattern()
        self._algo = algo

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

        offset_row = (self._height - pat_height) // 2
        offset_col = (self._width - pat_width) // 2

        pattern_pos: set[tuple[int, int]] = set()

        for row in range(pat_height):
            for col in range(pat_width):
                if pattern[row][col]:
                    pattern_pos.add((offset_row + row, offset_col + col))
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

        return pattern_pos

    def generate(self) -> Maze:
        """Generates a maze using Prim's algorithm.

        Returns:
            Maze: The generated maze object.
        """
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
        row, col = pos
        neighbors = [
            (row - 1, col), (row + 1, col),
            (row, col - 1), (row, col + 1),
        ]
        return [
            (row_nei, col_nei)
            for row_nei, col_nei in neighbors
            if 0 <= row_nei < self._height and 0 <= col_nei < self._width
        ]

    def _add_loops(self) -> None:
        """Adds loops to make the maze imperfect.

        It opens some walls without creating 2x2 area.
        """
        adjacent_pairs = []
        for row in range(self._height):
            for col in range(self._width):
                if row < self._height - 1:
                    adjacent_pairs.append(((row, col), (row + 1, col)))
                if col < self._width - 1:
                    adjacent_pairs.append(((row, col), (row, col + 1)))

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
        row1, col1 = pos1
        row2, col2 = pos2
        cell1: Cell = self._grid.get_cell(pos1)
        if row1 < row2:
            return cell1.south
        if col1 < col2:
            return cell1.east
        return False

    def _check_2x2(self, row: int, col: int) -> bool:
        """Checks if breaking a wall creates a 2x2 area.

        Args:
            row: Top-left row index of the 2x2 area.
            col: Top-left column index of the 2x2 area.

        Returns:
            bool: True if three or more walls are already open in the 2x2 area.
        """
        left_top = self._grid.get_cell((row, col))
        right_top = self._grid.get_cell((row, col + 1))
        left_bot = self._grid.get_cell((row + 1, col))
        counter = 0
        if not left_top.east:
            counter += 1
        if not left_top.south:
            counter += 1
        if not right_top.south:
            counter += 1
        if not left_bot.east:
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

        row1, col1 = pos1
        row2, _ = pos2
        if row1 < row2:
            if col1 > 0 and self._check_2x2(row1, col1 - 1):
                return False
            if col1 < self._width - 1 and self._check_2x2(row1, col1):
                return False
        else:
            if row1 > 0 and self._check_2x2(row1 - 1, col1):
                return False
            if row1 < self._height - 1 and self._check_2x2(row1, col1):
                return False

        return True
