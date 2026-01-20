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
    """

    north: bool
    east: bool
    south: bool
    west: bool
    closed: bool

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
    exit: tuple[int, int]
    grid: list[list[Cell]]

    def __init__(
        self, width: int, height: int,
        entry: tuple[int, int], exit: tuple[int, int]
    ):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid = [
            [Cell(True, True, True, True, True) for _ in range(width)]
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


class MazeGenerator:
    """Maze generator controller.

    This class handles maze generation logic and produces a Maze instance
    based on given parameters.

    Attributes:
        width (int): Width of the maze in number of cells.
        height (int): Height of the maze in number of cells.
        entry (tuple[int, int]): Entry cell position (row, col).
        exit (tuple[int, int]): Exit cell position (row, col).
        perfect (bool): Whether the generated maze is perfect.
        seed (int | None): Random seed for maze generation.
        grid (Maze): Generated maze structure.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    perfect: bool
    seed: int
    grid: Maze

    def __init__(
        self, width: int, height: int,
        entry: tuple[int, int], exit: tuple[int, int],
        perfect: bool = True, seed: int | None = None
    ):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed
        self.grid = Maze(width, height, entry, exit)

        if seed is not None:
            import random
            random.seed(seed)
