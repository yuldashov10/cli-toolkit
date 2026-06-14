from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseReader(ABC):
    """Abstract file reader."""

    @classmethod
    @abstractmethod
    def read(cls, path: Path) -> Any:
        """Read *path* and return its contents."""
        raise NotImplementedError


class BaseWriter(ABC):
    """Abstract file writer."""

    @classmethod
    @abstractmethod
    def write(cls, data: Any, path: Path) -> None:
        """Write *data* to *path*."""
        raise NotImplementedError


class BaseSelectorAbstract(ABC):
    """Abstract base for interactive selectors."""

    @classmethod
    @abstractmethod
    def select(cls, path: Path) -> list[Path]:
        raise NotImplementedError
