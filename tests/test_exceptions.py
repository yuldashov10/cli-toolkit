from pathlib import Path

import pytest

from app.exceptions import (
    AppError,
    ConfigError,
    FileOperationError,
    UnsupportedFormatError,
    ValidationError,
)


class TestAppError:
    def test_message_only(self) -> None:
        exc = AppError("something went wrong")
        assert str(exc) == "something went wrong"

    def test_with_hint(self) -> None:
        exc = AppError("something went wrong", hint="try again")
        assert "something went wrong" in str(exc)
        assert "try again" in str(exc)

    def test_hint_is_none_by_default(self) -> None:
        exc = AppError("error")
        assert exc.hint is None

    def test_is_exception(self) -> None:
        with pytest.raises(AppError):
            raise AppError("error")


class TestConfigError:
    def test_inherits_from_app_error(self) -> None:
        exc = ConfigError("bad config")
        assert isinstance(exc, AppError)

    def test_with_hint(self) -> None:
        exc = ConfigError("bad config", hint="check yaml syntax")
        assert "check yaml syntax" in str(exc)


class TestFileOperationError:
    def test_message_only(self) -> None:
        exc = FileOperationError("read failed")
        assert str(exc) == "read failed"

    def test_with_path(self) -> None:
        path = Path("data/file.xlsx")
        exc = FileOperationError("read failed", path=path)
        assert "data/file.xlsx" in str(exc)

    def test_with_hint(self) -> None:
        exc = FileOperationError("read failed", hint="check permissions")
        assert "check permissions" in str(exc)

    def test_with_path_and_hint(self) -> None:
        path = Path("file.csv")
        exc = FileOperationError("read failed", path=path, hint="check file")
        result = str(exc)
        assert "file.csv" in result
        assert "check file" in result

    def test_path_is_none_by_default(self) -> None:
        exc = FileOperationError("error")
        assert exc.path is None

    def test_inherits_from_app_error(self) -> None:
        exc = FileOperationError("error")
        assert isinstance(exc, AppError)


class TestUnsupportedFormatError:
    def test_inherits_from_file_operation_error(self) -> None:
        exc = UnsupportedFormatError("bad format")
        assert isinstance(exc, FileOperationError)
        assert isinstance(exc, AppError)

    def test_with_path_and_hint(self) -> None:
        path = Path("file.txt")
        exc = UnsupportedFormatError(
            "bad format", path=path, hint="use xlsx instead"
        )
        assert "file.txt" in str(exc)
        assert "use xlsx instead" in str(exc)


class TestValidationError:
    def test_inherits_from_app_error(self) -> None:
        exc = ValidationError("invalid data")
        assert isinstance(exc, AppError)

    def test_message(self) -> None:
        exc = ValidationError("field required")
        assert str(exc) == "field required"
