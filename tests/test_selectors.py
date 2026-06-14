from pathlib import Path
from unittest.mock import patch

import pytest

from app.exceptions import FileOperationError
from app.files.selectors import (
    CSVFileSelector,
    DefaultFileSelector,
    DirSelector,
    ExcelFileSelector,
    FileSelector,
)


class TestDefaultFileSelector:
    def test_returns_all_files(self, tmp_path: Path) -> None:
        (tmp_path / "a.txt").touch()
        (tmp_path / "b.csv").touch()
        result = DefaultFileSelector.select(tmp_path)
        assert len(result) == 2

    def test_excludes_directories(self, tmp_path: Path) -> None:
        (tmp_path / "file.txt").touch()
        (tmp_path / "subdir").mkdir()
        result = DefaultFileSelector.select(tmp_path)
        assert all(p.is_file() for p in result)

    def test_returns_sorted(self, tmp_path: Path) -> None:
        (tmp_path / "b.txt").touch()
        (tmp_path / "a.txt").touch()
        result = DefaultFileSelector.select(tmp_path)
        assert result == sorted(result)

    def test_empty_directory_returns_empty_list(self, empty_dir: Path) -> None:
        assert DefaultFileSelector.select(empty_dir) == []


class TestExcelFileSelector:
    def test_returns_only_excel_files(self, dir_with_xlsx: Path) -> None:
        result = ExcelFileSelector.select(dir_with_xlsx)
        assert all(p.suffix in (".xlsx", ".xls") for p in result)

    def test_excludes_non_excel_files(self, dir_with_xlsx: Path) -> None:
        result = ExcelFileSelector.select(dir_with_xlsx)
        names = [p.name for p in result]
        assert "notes.txt" not in names

    def test_returns_sorted(self, dir_with_xlsx: Path) -> None:
        result = ExcelFileSelector.select(dir_with_xlsx)
        assert result == sorted(result)

    def test_does_not_match_xlsm_or_other(self, tmp_path: Path) -> None:
        (tmp_path / "file.xlsm").touch()
        (tmp_path / "file.xlsb").touch()
        (tmp_path / "file.xlsx").touch()
        result = ExcelFileSelector.select(tmp_path)
        assert len(result) == 1
        assert result[0].suffix == ".xlsx"


class TestCSVFileSelector:
    def test_returns_only_csv_files(self, dir_with_csv: Path) -> None:
        result = CSVFileSelector.select(dir_with_csv)
        assert all(p.suffix == ".csv" for p in result)

    def test_returns_sorted(self, dir_with_csv: Path) -> None:
        result = CSVFileSelector.select(dir_with_csv)
        assert result == sorted(result)

    def test_empty_directory_returns_empty_list(self, empty_dir: Path) -> None:
        assert CSVFileSelector.select(empty_dir) == []


class TestFileSelector:
    def test_raises_when_no_files_found(self, empty_dir: Path) -> None:
        with pytest.raises(FileOperationError):
            FileSelector.select(empty_dir, ext="xlsx")

    def test_error_message_contains_ext(self, empty_dir: Path) -> None:
        with pytest.raises(FileOperationError) as exc_info:
            FileSelector.select(empty_dir, ext="xlsx")
        assert "xlsx" in str(exc_info.value)

    def test_error_message_any_when_no_ext(self, empty_dir: Path) -> None:
        with pytest.raises(FileOperationError) as exc_info:
            FileSelector.select(empty_dir, ext="")
        assert "any" in str(exc_info.value)

    def test_raises_stop_iteration_on_back(self, dir_with_xlsx: Path) -> None:
        with patch("inquirer.prompt", return_value={"file": "← Back"}):
            with pytest.raises(StopIteration):
                FileSelector.select(dir_with_xlsx, ext="xlsx")

    def test_raises_stop_iteration_on_none_answer(
        self, dir_with_xlsx: Path
    ) -> None:
        with patch("inquirer.prompt", return_value=None):
            with pytest.raises(StopIteration):
                FileSelector.select(dir_with_xlsx, ext="xlsx")

    def test_returns_selected_file(self, dir_with_xlsx: Path) -> None:
        files = ExcelFileSelector.select(dir_with_xlsx)
        selected_name = files[0].name
        with patch("inquirer.prompt", return_value={"file": selected_name}):
            result = FileSelector.select(dir_with_xlsx, ext="xlsx")
        assert result.name == selected_name

    def test_all_raises_when_empty(self, empty_dir: Path) -> None:
        with pytest.raises(FileOperationError):
            FileSelector.all(empty_dir)

    def test_all_returns_all_files(self, dir_with_xlsx: Path) -> None:
        result = FileSelector.all(dir_with_xlsx)
        assert len(result) > 0


class TestDirSelector:
    def test_raises_when_no_subdirs(self, empty_dir: Path) -> None:
        with pytest.raises(FileOperationError):
            DirSelector.select(empty_dir)

    def test_raises_stop_iteration_on_back(
        self, dir_with_subdirs: Path
    ) -> None:
        with patch("inquirer.prompt", return_value={"dir": "← Back"}):
            with pytest.raises(StopIteration):
                DirSelector.select(dir_with_subdirs)

    def test_raises_stop_iteration_on_none_answer(
        self, dir_with_subdirs: Path
    ) -> None:
        with patch("inquirer.prompt", return_value=None):
            with pytest.raises(StopIteration):
                DirSelector.select(dir_with_subdirs)

    def test_returns_selected_directory(self, dir_with_subdirs: Path) -> None:
        dirs = sorted(p for p in dir_with_subdirs.iterdir() if p.is_dir())
        selected_name = dirs[0].name
        with patch("inquirer.prompt", return_value={"dir": selected_name}):
            result = DirSelector.select(dir_with_subdirs)
        assert result.name == selected_name
        assert result.is_dir()
