#!/usr/bin/env python3
from typing import ClassVar


class InvalidFormat(Exception):
    pass


class Config:
    """Configuration for maze generation.

    Raises:
        InvalidFormat: If the config file has syntax errors or missing keys.
        ValueError: If the config file cannot be found.
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
    _data_str: dict[str, str]

    def __init__(self, path: str) -> None:
        self.path = path
        self._data_str = {}
        self._read_file()
        self._validate_required_keys()
        self._parse()

    def _read_file(self) -> None:
        """Reads the configuration file and stores raw key-value pairs.

        Raises:
            InvalidFormat: If a line is missing an '=' sign.
            ValueError: If the file is not found.
        """
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                for lineno, line in enumerate(file, start=1):
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        raise InvalidFormat(f"Invalid syntax at line {lineno}")
                    key, value = line.split("=", 1)
                    self._data_str[key.strip().upper()] = value.strip()
        except FileNotFoundError:
            raise ValueError(f"Config file not found: {self.path}")

    def _parse(self) -> None:
        """Parses raw strings into specific data types and validates them.

        Raises:
            InvalidFormat: If data is invalid or ENTRY and EXIT are the same.
        """
        self.width = self._parse_int("WIDTH")
        self.height = self._parse_int("HEIGHT")
        self.entry = self._parse_tuple("ENTRY")
        self.exit = self._parse_tuple("EXIT")
        self.output_file = self._parse_filename("OUTPUT_FILE")
        self.perfect = self._parse_bool("PERFECT")
        if self.entry == self.exit:
            raise InvalidFormat("ENTRY and EXIT must be different")

    def _parse_int(self, key: str) -> int:
        """Converts a config value to a positive integer.

        Args:
            key: The config key to parse.

        Returns:
            The positive integer.

        Raises:
            InvalidFormat: If the value is not a positive integer.
        """
        try:
            val_i = int(self._data_str[key])
        except ValueError:
            raise InvalidFormat(f"{key} must be an integer")

        if val_i <= 0:
            raise InvalidFormat(f"{key} must be positive")
        return val_i

    def _parse_tuple(self, key: str) -> tuple[int, int]:
        """Converts a config value to a coordinate tuple.

        Args:
            key: The config key to parse.

        Returns:
            A tuple of (x, y) coordinates.

        Raises:
            InvalidFormat: If the format is wrong or
                           coordinates are out of bounds.
        """
        value = self._data_str[key]
        try:
            x_str, y_str = value.split(",", 1)
            x_val, y_val = int(x_str), int(y_str)
        except ValueError:
            raise InvalidFormat(f"{key} must be in format x,y")

        if not (0 <= x_val < self.width and 0 <= y_val < self.height):
            raise InvalidFormat(f"{key} is out of maze bounds")
        return x_val, y_val

    def _parse_bool(self, key: str) -> bool:
        """Converts a config value to a boolean.

        Args:
            key: The config key to parse.

        Returns:
            True if value is "true", False if "false".

        Raises:
            InvalidFormat: If the value is neither "true" nor "false".
        """
        value = self._data_str[key].lower()
        if value == "true":
            return True
        if value == "false":
            return False
        raise InvalidFormat(f"{key} must be True or False")

    def _parse_filename(self, key: str) -> str:
        """Validates the output filename.

        Args:
            key: The config key to parse.

        Returns:
            The validated filename string.

        Raises:
            InvalidFormat: If the filename does not end with '.txt'.
        """
        value = self._data_str[key]
        if not value.endswith(".txt"):
            raise InvalidFormat("OUTPUT_FILE must end with .txt")
        return value

    def _validate_required_keys(self) -> None:
        """Checks if the config data has all required keys.

        Raises:
            InvalidFormat: If any required keys are missing.
        """
        missing = self.required_key - self._data_str.keys()
        if missing:
            raise InvalidFormat(
                f"Missing required keys: {', '.join(missing)}"
            )
