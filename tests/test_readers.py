from pathlib import Path

import pytest
import yaml

from app.exceptions import FileOperationError, UnsupportedFormatError
from app.files.readers import (
    CSVReader,
    ExcelReader,
    JSONReader,
    Reader,
    YAMLReader,
)


class TestExcelReader:
    def test_returns_first_column_as_list(self, xlsx_file: Path) -> None:
        result = ExcelReader.read(xlsx_file)
        assert result == ["Alice", "Bob", "Charlie"]

    def test_returns_list_of_strings(self, xlsx_file: Path) -> None:
        result = ExcelReader.read(xlsx_file)
        assert all(isinstance(item, str) for item in result)

    def test_missing_file_raises_file_operation_error(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileOperationError):
            ExcelReader.read(tmp_path / "missing.xlsx")


class TestCSVReader:
    def test_returns_first_column_as_list(self, csv_file: Path) -> None:
        result = CSVReader.read(csv_file)
        assert result == ["Alice", "Bob", "Charlie"]

    def test_returns_list_of_strings(self, csv_file: Path) -> None:
        result = CSVReader.read(csv_file)
        assert all(isinstance(item, str) for item in result)

    def test_missing_file_raises_file_operation_error(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileOperationError):
            CSVReader.read(tmp_path / "missing.csv")


class TestJSONReader:
    def test_returns_list_of_dicts(self, json_file: Path) -> None:
        result = JSONReader.read(json_file)
        assert isinstance(result, list)
        assert result[0]["name"] == "Alice"

    def test_broken_file_raises_file_operation_error(
        self, broken_json_file: Path
    ) -> None:
        with pytest.raises(FileOperationError):
            JSONReader.read(broken_json_file)

    def test_missing_file_raises_file_operation_error(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileOperationError):
            JSONReader.read(tmp_path / "missing.json")


class TestYAMLReader:
    def test_returns_list_of_dicts(self, yaml_file: Path) -> None:
        result = YAMLReader.read(yaml_file)
        assert isinstance(result, list)
        assert result[0]["name"] == "Alice"

    def test_broken_file_raises_file_operation_error(
        self, broken_yaml_file: Path
    ) -> None:
        with pytest.raises(FileOperationError):
            YAMLReader.read(broken_yaml_file)

    def test_missing_file_raises_file_operation_error(
        self, tmp_path: Path
    ) -> None:
        with pytest.raises(FileOperationError):
            YAMLReader.read(tmp_path / "missing.yaml")


class TestReader:
    def test_load_xlsx(self, xlsx_file: Path) -> None:
        result = Reader.load(xlsx_file)
        assert result == ["Alice", "Bob", "Charlie"]

    def test_load_csv(self, csv_file: Path) -> None:
        result = Reader.load(csv_file)
        assert result == ["Alice", "Bob", "Charlie"]

    def test_load_json(self, json_file: Path) -> None:
        result = Reader.load(json_file)
        assert isinstance(result, list)

    def test_load_yaml(self, yaml_file: Path) -> None:
        result = Reader.load(yaml_file)
        assert isinstance(result, list)

    def test_load_yml_extension(self, tmp_path: Path) -> None:
        path = tmp_path / "sample.yml"
        path.write_text(yaml.dump([{"key": "val"}]), encoding="UTF-8")
        result = Reader.load(path)
        assert isinstance(result, list)

    def test_unsupported_extension_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "file.txt"
        path.write_text("hello", encoding="UTF-8")
        with pytest.raises(UnsupportedFormatError):
            Reader.load(path)

    def test_unsupported_error_contains_hint(self, tmp_path: Path) -> None:
        path = tmp_path / "file.txt"
        path.write_text("hello", encoding="UTF-8")
        with pytest.raises(UnsupportedFormatError) as exc_info:
            Reader.load(path)
        assert exc_info.value.hint is not None
