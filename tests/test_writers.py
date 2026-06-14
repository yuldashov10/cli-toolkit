from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from app.exceptions import UnsupportedFormatError
from app.files.readers import Reader
from app.files.writers import (
    CSVWriter,
    ExcelWriter,
    JSONWriter,
    Writer,
    YAMLWriter,
)


class TestExcelWriter:
    def test_writes_file(self, tmp_path: Path) -> None:
        path = tmp_path / "out.xlsx"
        ExcelWriter.write([["Alice"], ["Bob"]], path)
        assert path.exists()

    def test_roundtrip_with_reader(self, tmp_path: Path) -> None:
        path = tmp_path / "out.xlsx"
        ExcelWriter.write([["Alice"], ["Bob"]], path)
        assert Reader.load(path) == ["Alice", "Bob"]

    def test_accepts_dataframe(self, tmp_path: Path) -> None:
        path = tmp_path / "out.xlsx"
        df = pd.DataFrame({"name": ["Alice", "Bob"]})
        ExcelWriter.write(df, path)
        assert path.exists()


class TestCSVWriter:
    def test_writes_file(self, tmp_path: Path) -> None:
        path = tmp_path / "out.csv"
        CSVWriter.write([["Alice"], ["Bob"]], path)
        assert path.exists()

    def test_roundtrip_with_reader(self, tmp_path: Path) -> None:
        path = tmp_path / "out.csv"
        CSVWriter.write([["Alice"], ["Bob"]], path)
        assert Reader.load(path) == ["Alice", "Bob"]

    def test_accepts_dataframe(self, tmp_path: Path) -> None:
        path = tmp_path / "out.csv"
        df = pd.DataFrame({"name": ["Alice"]})
        CSVWriter.write(df, path)
        assert path.exists()


class TestJSONWriter:
    def test_writes_file(self, tmp_path: Path) -> None:
        path = tmp_path / "out.json"
        JSONWriter.write({"key": "value"}, path)
        assert path.exists()

    def test_roundtrip_with_reader(self, tmp_path: Path) -> None:
        path = tmp_path / "out.json"
        data: dict[str, Any] = {"key": "value"}
        JSONWriter.write(data, path)
        assert Reader.load(path) == data

    def test_list_roundtrip(self, tmp_path: Path) -> None:
        path = tmp_path / "out.json"
        data = [{"name": "Alice"}, {"name": "Bob"}]
        JSONWriter.write(data, path)
        assert Reader.load(path) == data

    def test_unicode_preserved(self, tmp_path: Path) -> None:
        path = tmp_path / "out.json"
        data = {"name": "Алиса"}
        JSONWriter.write(data, path)
        result = Reader.load(path)
        assert result["name"] == "Алиса"


class TestYAMLWriter:
    def test_writes_file(self, tmp_path: Path) -> None:
        path = tmp_path / "out.yaml"
        YAMLWriter.write({"key": "value"}, path)
        assert path.exists()

    def test_roundtrip_with_reader(self, tmp_path: Path) -> None:
        path = tmp_path / "out.yaml"
        data: dict[str, Any] = {"key": "value"}
        YAMLWriter.write(data, path)
        assert Reader.load(path) == data

    def test_unicode_preserved(self, tmp_path: Path) -> None:
        path = tmp_path / "out.yaml"
        data = {"name": "Алиса"}
        YAMLWriter.write(data, path)
        result = Reader.load(path)
        assert result["name"] == "Алиса"


class TestWriter:
    def test_save_xlsx(self, tmp_path: Path) -> None:
        path = tmp_path / "out.xlsx"
        Writer.save([["Alice"]], path)
        assert path.exists()

    def test_save_csv(self, tmp_path: Path) -> None:
        path = tmp_path / "out.csv"
        Writer.save([["Alice"]], path)
        assert path.exists()

    def test_save_json(self, tmp_path: Path) -> None:
        path = tmp_path / "out.json"
        Writer.save({"key": "val"}, path)
        assert path.exists()

    def test_save_yaml(self, tmp_path: Path) -> None:
        path = tmp_path / "out.yaml"
        Writer.save({"key": "val"}, path)
        assert path.exists()

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        path = tmp_path / "nested" / "deep" / "out.json"
        Writer.save({"key": "val"}, path)
        assert path.exists()

    def test_unsupported_extension_raises(self, tmp_path: Path) -> None:
        with pytest.raises(UnsupportedFormatError):
            Writer.save("data", tmp_path / "out.txt")

    def test_unsupported_error_contains_hint(self, tmp_path: Path) -> None:
        with pytest.raises(UnsupportedFormatError) as exc_info:
            Writer.save("data", tmp_path / "out.txt")
        assert exc_info.value.hint is not None
