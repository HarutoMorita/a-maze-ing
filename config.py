from typing import ClassVar
import os


class InvalidFormat(Exception):
    pass


class Config:
    """Configuration for maze generation and validation.

    Attributes:
        required_key: Set of keys that must be present in the config file.
        path: Path to the configuration file.
        width: Maze width.
        height: Maze height.
        entry: Starting coordinates as (x, y).
        exit: Destination coordinates as (x, y).
        output_file: Path to the result text file.
        perfect: Whether the maze should be perfect (no loops).
        seed: Random seed for generation.
        algo: Algorithm name (DFS or PRIM).
    """

    required_key: ClassVar[set[str]] = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT",
        "OUTPUT_FILE", "PERFECT"
    }

    path: str
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None = None
    algo: str | None = None
    _data_str: dict[str, str]

    def __init__(self, path: str) -> None:
        """Initializes config by loading the specified file."""
        self.path = path
        self.load_config()

    def load_config(self) -> None:
        """Reads, validates, and parses the config file."""
        self._data_str = {}
        self._read_file()
        self._validate_required_keys()
        self._parse()

    def _read_file(self) -> None:
        """Reads the raw key-value pairs from the config file."""
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                for lineno, line in enumerate(file, start=1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    if any(c.isspace() for c in line):
                        raise InvalidFormat(f"Spaces are not allowed "
                                            f"at line {lineno}")
                    parts: list[str] = line.split("=")
                    if len(parts) != 2:
                        raise InvalidFormat(f"Invalid syntax at line {lineno}")
                    key, value = parts
                    self._data_str[key.upper()] = value
        except InvalidFormat:
            raise
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {self.path}")
        except PermissionError:
            raise PermissionError(f"Config not allowed to open: {self.path}")
        except IsADirectoryError:
            raise InvalidFormat(f"This program expected a file, "
                                f"not a directory: {self.path}")
        except Exception as e:
            raise Exception(f"Unexpected error concerning file: {e}")

    def _parse(self) -> None:
        """Parses raw strings into specific data types and validates values."""
        self.width = self._parse_int("WIDTH")
        self.height = self._parse_int("HEIGHT")
        self.entry = self._parse_tuple("ENTRY")
        self.exit = self._parse_tuple("EXIT")
        self.output_file = self._parse_filename("OUTPUT_FILE")
        self.perfect = self._parse_bool("PERFECT")
        if "SEED" in self._data_str:
            self.seed = self._parse_int("SEED")
        if "ALGO" in self._data_str:
            self.algo = self._parse_algo("ALGO")
        if self.entry == self.exit:
            raise InvalidFormat("ENTRY and EXIT must be different")

    def _parse_int(self, key: str) -> int:
        """Converts the specified config value to a positive integer."""
        try:
            val_i = int(self._data_str[key])
        except ValueError:
            raise InvalidFormat(f"{key} must be an integer")
        if key != "SEED" and val_i > 100:
            raise InvalidFormat(f"{key} must be at most 100")
        if val_i <= 0:
            raise InvalidFormat(f"{key} must be positive")
        return val_i

    def _parse_tuple(self, key: str) -> tuple[int, int]:
        """Converts the specified config value to a coordinate tuple (x, y)."""
        value = self._data_str[key]
        try:
            x_str, y_str = value.split(",", 1)
            x_val, y_val = int(x_str), int(y_str)
        except ValueError:
            raise InvalidFormat(f"{key} must be in format x,y")

        if not (0 <= x_val < self.width and 0 <= y_val < self.height):
            raise InvalidFormat(f"{key} is out of maze's bounds")
        return x_val, y_val

    def _parse_bool(self, key: str) -> bool:
        """Converts the specified config value to a boolean."""
        value = self._data_str[key].lower()
        if value == "true":
            return True
        if value == "false":
            return False
        raise InvalidFormat(f"{key} must be True or False")

    def _parse_algo(self, key: str) -> str:
        """Converts the specified config value to an algorithm name string."""
        value = self._data_str[key].upper()
        if value == "DFS" or value == "PRIM":
            return value
        else:
            raise InvalidFormat(f"{key} must be DFS or PRIM")

    def _parse_filename(self, key: str) -> str:
        """Validates and returns the output filename string."""
        value = self._data_str[key]
        if not value.endswith(".txt"):
            raise InvalidFormat("OUTPUT_FILE must end with .txt")
        if value == self.path:
            raise InvalidFormat(
                "OUTPUT_FILE must be different from the config file")
        if os.path.isdir(value):
            raise InvalidFormat(f"OUTPUT_FILE must be a file, "
                                f"not a directory: {value}")
        parent = os.path.dirname(value) or '.'
        if not os.access(parent, os.W_OK):
            raise InvalidFormat(f"Cannot write to the directory: {parent}")
        return value

    def _validate_required_keys(self) -> None:
        """Checks if all required keys are present in the config data."""
        missing = self.required_key - self._data_str.keys()
        if missing:
            raise InvalidFormat(
                f"Missing required keys: {', '.join(missing)}"
            )
