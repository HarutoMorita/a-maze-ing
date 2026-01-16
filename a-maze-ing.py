#!/usr/bin/env python3


class InvalidFormat(Exception):
    pass


class Config:
    """Configuration for maze generation.

    Raises:
        InvalidFormat: If the config file has syntax errors or missing keys.
        ValueError: If the config file cannot be found.
    """

    required_key = {
        "WIDTH", "HEIGHT",
        "ENTRY", "EXIT",
        "OUTPUT_FILE", "PERFECT"
    }

    def __init__(self, path: str):
        self.path = path
        self._data_str: dict[str, str] = {}
        self._read_file()
        self._validate_required_keys()
        self._parse()

    def _read_file(self) -> None:
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
        self.width = self._parse_int("WIDTH")
        self.height = self._parse_int("HEIGHT")
        self.entry = self._parse_tuple("ENTRY")
        self.exit = self._parse_tuple("EXIT")
        self.output_file = self._parse_filename("OUTPUT_FILE")
        self.perfect = self._parse_bool("PERFECT")
        if self.entry == self.exit:
            raise InvalidFormat("ENTRY and EXIT must be different")

    def _parse_int(self, key: str) -> int:
        try:
            return int(self._data_str[key])
        except ValueError:
            raise InvalidFormat(f"{key} must be an integer")

    def _parse_tuple(self, key: str) -> tuple[int, int]:
        value = self._data_str[key]
        try:
            x_str, y_str = value.split(",", 1)
            return int(x_str), int(y_str)
        except ValueError:
            raise InvalidFormat(f"{key} must be in format x,y")

    def _parse_bool(self, key: str) -> bool:
        value = self._data_str[key].lower()
        if value == "true":
            return True
        if value == "false":
            return False
        raise InvalidFormat(f"{key} must be True or False")

    def _parse_filename(self, key: str) -> str:
        value = self._data_str[key]
        if not value.endswith(".txt"):
            raise InvalidFormat("OUTPUT_FILE must end with .txt")
        return value

    def _validate_required_keys(self) -> None:
        missing = self.required_key - self._data_str.keys()
        if missing:
            raise InvalidFormat(
                f"Missing required keys: {', '.join(missing)}"
            )
