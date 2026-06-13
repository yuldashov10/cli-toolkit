import json
from pathlib import Path
from typing import Any

import pandas as pd
import yaml

from app.exceptions import FileOperationError, UnsupportedFormatError

from .abstract import BaseWriter


class ExcelWriter(BaseWriter):
    """Write a list of rows or a DataFrame to an Excel file."""

    @classmethod
    def write(cls, data: Any, path: Path) -> None:
        try:
            df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
            df.to_excel(path, index=False, engine="openpyxl")
        except Exception as exc:
            raise FileOperationError(
                "Failed to write Excel file", path=path
            ) from exc


class CSVWriter(BaseWriter):
    """Write a list of rows or a DataFrame to a CSV file."""

    @classmethod
    def write(cls, data: Any, path: Path) -> None:
        try:
            df = data if isinstance(data, pd.DataFrame) else pd.DataFrame(data)
            df.to_csv(path, index=False, encoding="UTF-8")
        except Exception as exc:
            raise FileOperationError(
                "Failed to write CSV file", path=path
            ) from exc


class JSONWriter(BaseWriter):
    """Write a dict or list to a pretty-printed JSON file."""

    @classmethod
    def write(cls, data: Any, path: Path) -> None:
        try:
            with open(path, "w", encoding="UTF-8") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
        except Exception as exc:
            raise FileOperationError(
                "Failed to write JSON file", path=path
            ) from exc


class YAMLWriter(BaseWriter):
    """Write a dict or list to a YAML file."""

    @classmethod
    def write(cls, data: Any, path: Path) -> None:
        try:
            with open(path, "w", encoding="UTF-8") as fh:
                yaml.dump(
                    data, fh, allow_unicode=True, default_flow_style=False
                )
        except Exception as exc:
            raise FileOperationError(
                "Failed to write YAML file", path=path
            ) from exc


class Writer:
    """Dispatcher that selects the correct writer by file extension."""

    _writers: dict[str, type[BaseWriter]] = {
        ".xlsx": ExcelWriter,
        ".xls": ExcelWriter,
        ".csv": CSVWriter,
        ".json": JSONWriter,
        ".yaml": YAMLWriter,
        ".yml": YAMLWriter,
    }

    @classmethod
    def save(cls, data: Any, path: Path) -> None:
        """Save *data* to *path* using the appropriate writer.

        The output directory is created automatically if it does not exist.

        Args:
            data: Data to serialise (DataFrame, list, dict, etc.).
            path: Destination file path.

        Raises:
            UnsupportedFormatError: If the file extension is not recognised.
            FileOperationError: If the file cannot be written.
        """
        ext = Path(path).suffix.lower()
        writer = cls._writers.get(ext)

        if writer is None:
            raise UnsupportedFormatError(
                f"Unsupported file format: '{ext}'",
                path=path,
                hint=f"Supported formats: {', '.join(cls._writers)}",
            )

        Path(path).parent.mkdir(parents=True, exist_ok=True)
        writer.write(data, path)
