from typing import Iterator


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

    WALL_BITS = {"N": 1 << 0, "E": 1 << 1, "S": 1 << 2, "W": 1 << 3}

    value: int
    is_entry: bool
    is_exit: bool
    is_pattern: bool

    def __init__(self) -> None:
        self.value = 0xF
        self.is_entry = False
        self.is_exit = False
        self.is_pattern = False

    def remove_wall(self, direction: str) -> None:
        if direction in self.WALL_BITS:
            self.value &= ~self.WALL_BITS[direction]

    def set_path(self, bit: int) -> None:
        self.value |= bit

    def clear_path(self) -> None:
        self.value &= ~96


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

    def __iter__(self) -> Iterator[list[Cell]]:
        return iter(self.grid)

    def get_cell(self, pos: tuple[int, int]) -> Cell:
        """Return the cell at the given position.

        Args:
            pos (tuple[int, int]): Cell position(row, col).

        Returns:
            Cell: The cell located at the passed position.
        """
        x, y = pos
        return self.grid[y][x]

    def __getitem__(self, y: int) -> list[Cell]:
        return self.grid[y]

    def __str__(self) -> str:
        return "\n".join(
            "".join(format(c.value, "X") for c in row) for row in self.grid
        )

    def clear_all_paths(self) -> None:
        for row in self.grid:
            for cell in row:
                cell.clear_path()
