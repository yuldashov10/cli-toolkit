from pathlib import Path

import pytest

from app.paths import BASE_DIR, DataPath, LogsPath, ResourcesPath
from app.paths.base import BasePath


class TestBasePath:
    def test_cannot_instantiate_without_root(self) -> None:
        with pytest.raises(TypeError):

            class EmptyPath(BasePath):
                _root = ""

    def test_subclass_with_root_is_valid(self) -> None:
        class TempPath(BasePath):
            _root = "tmp"

        assert TempPath._root == "tmp"

    def test_get_returns_path_under_base_dir(self) -> None:
        class TempPath(BasePath):
            _root = "tmp"

        result = TempPath.get()
        assert result == BASE_DIR / "tmp"

    def test_get_with_subfolders(self) -> None:
        class TempPath(BasePath):
            _root = "tmp"

        result = TempPath.get("sub", "file.txt")
        assert result == BASE_DIR / "tmp" / "sub" / "file.txt"

    def test_get_with_ensure_creates_directory(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import app.paths.base as base_module

        monkeypatch.setattr(base_module, "BASE_DIR", tmp_path)

        class TempPath(BasePath):
            _root = "tmp_ensure"

        target = TempPath.get("subdir", ensure=True)
        assert target.exists()

    def test_get_with_ensure_creates_parent_for_file(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import app.paths.base as base_module

        monkeypatch.setattr(base_module, "BASE_DIR", tmp_path)

        class TempPath(BasePath):
            _root = "tmp_ensure"

        target = TempPath.get("subdir", "file.txt", ensure=True)
        assert target.parent.exists()
        assert not target.exists()

    def test_get_without_ensure_does_not_create_directory(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import app.paths.base as base_module

        monkeypatch.setattr(base_module, "BASE_DIR", tmp_path)

        class TempPath(BasePath):
            _root = "nonexistent"

        TempPath.get("subdir")
        assert not (tmp_path / "nonexistent" / "subdir").exists()

    def test_exists_returns_true_for_existing(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        import app.paths.base as base_module

        monkeypatch.setattr(base_module, "BASE_DIR", tmp_path)
        (tmp_path / "tmp_ex").mkdir()

        class TempPath(BasePath):
            _root = "tmp_ex"

        assert TempPath.exists() is True

    def test_exists_returns_false_for_nonexistent(self) -> None:
        class TempPath(BasePath):
            _root = "__nonexistent_path__"

        assert TempPath.exists() is False


class TestConcretePaths:
    def test_data_path_root(self) -> None:
        assert DataPath.get() == BASE_DIR / "data"

    def test_logs_path_root(self) -> None:
        assert LogsPath.get() == BASE_DIR / "logs"

    def test_resources_path_root(self) -> None:
        assert ResourcesPath.get() == BASE_DIR / "resources"

    def test_data_path_with_subfolders(self) -> None:
        result = DataPath.get("raw", "report.xlsx")
        assert result == BASE_DIR / "data" / "raw" / "report.xlsx"
