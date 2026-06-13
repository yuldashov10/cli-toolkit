"""Application-level exception hierarchy.

Usage::

    from app.exceptions.base import AppError, FileOperationError

    raise FileOperationError("Cannot read file", path=Path("data.xlsx"))
"""

from pathlib import Path


class AppError(Exception):
    """Root exception for all application errors.

    All custom exceptions should inherit from this class so callers
    can catch everything with a single ``except AppError``.
    """

    def __init__(self, message: str, *, hint: str | None = None) -> None:
        super().__init__(message)
        self.hint = hint

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} — Hint: {self.hint}" if self.hint else base


class ConfigError(AppError):
    """Raised when configuration is missing or invalid."""


class FileOperationError(AppError):
    """Raised when a file cannot be read, written, or found.

    Args:
        message: Human-readable description of the problem.
        path:    The file path involved (optional).
    """

    def __init__(
        self,
        message: str,
        *,
        path: Path | None = None,
        hint: str | None = None,
    ) -> None:
        super().__init__(message, hint=hint)
        self.path = path

    def __str__(self) -> str:
        base = super().__str__()
        return f"{base} [path: {self.path}]" if self.path else base


class UnsupportedFormatError(FileOperationError):
    """Raised when a file format is not supported by a reader/writer."""


class ValidationError(AppError):
    """Raised when input data fails validation."""
