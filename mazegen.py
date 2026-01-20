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
        entry (tuple[int, int]): Entry cell coordinates (x, y).
        exit (tuple[int, int]): Exit cell coordinates (x, y).
        grid (list[list[Cell]]): 2D grid of maze cells.
    """
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    grid: list[list[Cell]]

    def __init__(
        self, width: int, height: int,
        entry: tuple[int, int], exit: tuple[int, int],
        grid: list[list[Cell]]
    ):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid: list[list[Cell]] = grid


class MazeGenerator:
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
        self.grid = [
                [Cell(True, True, True, True, True) for _ in range(width)]
                for _ in range(height)
            ]

        if seed is not None:
            import random
            random.seed(seed)
