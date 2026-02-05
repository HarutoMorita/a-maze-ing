from typing import Iterator


class Cell:
    """
    A single maze cell.

    Each cell is encoded into a hex digit based on its walls:
    Bit 0 (1): North wall
    Bit 1 (2): East wall
    Bit 2 (4): South wall
    Bit 3 (8): West wall
    For example, 9 (1001 in binary) represents walls on North and West.


    Attributes:
        value: The hex value representing each wall's status.
        is_entry: If the cell is entry.
        is_exit: If the cell is exit.
        is_pattern: If the cell is the part of pattern.
    """

    WALL_BITS = {"N": 1 << 0, "E": 1 << 1, "S": 1 << 2, "W": 1 << 3}

    value: int
    is_entry: bool
    is_exit: bool
    is_pattern: bool

    def __init__(self) -> None:
        """Initializes a cell with all walls closed and no status."""
        self.value = 0xF
        self.is_entry = False
        self.is_exit = False
        self.is_pattern = False

    def remove_wall(self, direction: str) -> None:
        """Removes the wall in the given direction."""
        if direction in self.WALL_BITS:
            self.value &= ~self.WALL_BITS[direction]

    def set_path(self, bit: int) -> None:
        """Marks the cell as part of a path using the given bit.

        Args:
            bit: The bit flag to set for path marking.
        """
        self.value |= bit

    def clear_path(self) -> None:
        """Clears any path markings from the cell."""
        self.value &= ~96


class Maze:
    """
    A rectangular maze grid.


    Attributes:
        width: Width of the maze in number of cells.
        height: Height of the maze in number of cells.
        entry: Entry cell coordinates (row, col).
        exit_ : Exit cell coordinates (row, col).
        grid: 2D grid of maze cells.
    """

    width: int
    height: int
    entry: tuple[int, int]
    exit_: tuple[int, int]
    grid: list[list[Cell]]

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit_: tuple[int, int]
    ) -> None:
        """Initializes the maze with dimensions and entry/exit points."""
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_ = exit_
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.get_cell(entry).is_entry = True
        self.get_cell(exit_).is_exit = True

    def __iter__(self) -> Iterator[list[Cell]]:
        """Returns an iterator over the maze rows."""
        return iter(self.grid)

    def get_cell(self, pos: tuple[int, int]) -> Cell:
        """Return the cell at the given position."""
        x, y = pos
        return self.grid[y][x]

    def __getitem__(self, y: int) -> list[Cell]:
        """Returns the row at the given y-coordinate."""
        return self.grid[y]

    def __str__(self) -> str:
        """Returns a string representation of the maze."""
        return "\n".join(
            "".join(format(c.value, "X") for c in row) for row in self.grid
        )

    def clear_all_paths(self) -> None:
        """Clears all path markings from the maze."""
        for row in self.grid:
            for cell in row:
                cell.clear_path()
