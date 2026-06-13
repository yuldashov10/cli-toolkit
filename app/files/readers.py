"""File readers for Excel, CSV, JSON, and YAML formats.

Usage::

    from app.files.readers import Reader

    data = Reader.load(Path("report.xlsx"))   # returns list[str] (1st column)
    data = Reader.load(Path("config.yaml"))   # returns dict
"""

import json
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from app.exceptions import FileOperationError, UnsupportedFormatError

from .abstract import BaseReader


class ExcelReader(BaseReader):
    """Read the first column of an Excel file as a list of strings."""

    @classmethod
    def read(cls, path: Path) -> list[str]:
        try:
            df = pd.read_excel(path, engine="openpyxl")
        except Exception as exc:
            raise FileOperationError(
                "Failed to read Excel file", path=path
            ) from exc
        return df.iloc[:, 0].dropna().astype(str).tolist()


class CSVReader(BaseReader):
    """Read the first column of a CSV file as a list of strings."""

    @classmethod
    def read(cls, path: Path) -> list[str]:
        try:
            df = pd.read_csv(path)
        except Exception as exc:
            raise FileOperationError(
                "Failed to read CSV file", path=path
            ) from exc
        return df.iloc[:, 0].dropna().astype(str).tolist()


class JSONReader(BaseReader):
    """Read a JSON file and return a dict or list."""

    @classmethod
    def read(cls, path: Path) -> Any:

        try:
            with open(path, encoding="UTF-8") as fh:
                return json.load(fh)
        except Exception as exc:
            raise FileOperationError(
                "Failed to read JSON file", path=path
            ) from exc


class YAMLReader(BaseReader):
    """Read a YAML file and return a dict or list."""

    @classmethod
    def read(cls, path: Path) -> Any:
        try:
            with open(path, encoding="UTF-8") as fh:
                return yaml.safe_load(fh)
        except Exception as exc:
            raise FileOperationError(
                "Failed to read YAML file", path=path
            ) from exc


class Reader:
    """Dispatcher that selects the correct reader by file extension.

    Supported extensions: ``.xlsx``, ``.xls``, ``.csv``, ``.json``,
    ``.yaml``, ``.yml``.
    """

    _readers: dict[str, type[BaseReader]] = {
        ".xlsx": ExcelReader,
        ".xls": ExcelReader,
        ".csv": CSVReader,
        ".json": JSONReader,
        ".yaml": YAMLReader,
        ".yml": YAMLReader,
    }

    @classmethod
    def load(cls, path: Path) -> Any:
        """Load *path* using the appropriate reader.

        Args:
            path: Path to the file.

        Returns:
            Parsed file contents (type depends on format).

        Raises:
            UnsupportedFormatError: If the file extension is not recognised.
            FileOperationError: If the file cannot be read.
        """
        ext = Path(path).suffix.lower()
        reader = cls._readers.get(ext)

        if reader is None:
            raise UnsupportedFormatError(
                f"Unsupported file format: '{ext}'",
                path=path,
                hint=f"Supported formats: {', '.join(cls._readers)}",
            )

        return reader.read(path)
