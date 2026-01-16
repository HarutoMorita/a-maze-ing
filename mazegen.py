#!/usr/bin/env python3


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
        closed (bool): If the cell is fully closed.
    """

    def __init__(
        self, north: bool, east: bool, south: bool, west: bool, closed: bool
    ):
        self.north = north
        self.east = east
        self.south = south
        self.west = west
        self.closed = closed


class Maze:
    """
    A rectangular maze grid.

    Invariants:
        - The maze is a width x height grid.
        - cells is a 2D list indexed as cells[y][x].
        - Each cell initially has all four walls closed.
        - entry and exit are distinct and inside maze bounds.

    Attributes:
        width (int): Width of the maze in number of cells.
        height (int): Height of the maze in number of cells.
        entry (tuple[int, int]): Entry cell coordinates (x, y).
        exit (tuple[int, int]): Exit cell coordinates (x, y).
        cells (list[list[Cell]]): 2D grid of maze cells.
    """

    def __init__(
        self, width: int, height: int,
        entry: tuple[int, int], exit: tuple[int, int]
    ):
        self._validate_dimensions(width, height)

        self.width = width
        self.height = height

        self._validate_point(entry, "entry")
        self._validate_point(exit, "exit")

        if entry == exit:
            raise ValueError("entry and exit must be different")

        self.entry = entry
        self.exit = exit

        self.cells = [
            [
                Cell(True, True, True, True, False)
                for _ in range(width)
            ]
            for _ in range(height)
        ]

    def _validate_dimensions(self, width: int, height: int) -> None:
        """Validate maze dimensions.

        Args:
            width (int): Maze width.
            height (int): Maze height.

        Raises:
            ValueError: If width or height is not a positive integer.
        """
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive integers")

    def _validate_point(
        self, point: tuple[int, int], name: str
    ) -> None:
        """Validate a point inside the maze bounds.

        Args:
            point (tuple[int, int]): Coordinates (x, y) to validate.
            name (str): Name of the point for error messages.

        Raises:
            ValueError: If the point is outside the maze bounds.
        """
        x, y = point
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError(f"{name} is out of maze bounds")


class MazeGenerator:
    def __init__(
        self, width: int, height: int, entry: int, exit: int,
        perfect: bool = True, seed: int | None = None
    ):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.grid = [
                [Cell(True, True, True, True, True) for _ in range(width)]
                for _ in range(height)
            ]

        if seed is not None:
            import random
            random.seed(seed)

        def as_hex_grid(self) -> list[list[str]]:
            hex_grid = []
            for row in self.grid:
                hex_row = []
                for cell in row:
                    bits = ((cell.west << 3) |
                            (cell.south << 2) |
                            (cell.east << 1) |
                            (cell.north))
                    hex_row.append(format(bits, "X"))
                hex_grid.append(hex_row)
            return hex_grid
