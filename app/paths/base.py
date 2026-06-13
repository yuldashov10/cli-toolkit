"""Project path registry.

A single place to define *where* the project stores its files.
Every directory is expressed as a class whose ``.get()`` method returns
an absolute :class:``pathlib.Path``, optionally creating the directory on
the fly.

Usage::

    from app.paths import DataPath, LogsPath, OutputPath

    raw_file = DataPath.get("raw", "report.xlsx")
    # → <project_root>/data/raw/report.xlsx

    out_dir = OutputPath.get("YYYY-MM", ensure=True)
    # → <project_root>/output/YYYY-MM/  (created if absent)

Adding a new directory
~~~~~~~~~~~~~~~~~~~~~~
Subclass :class:``BasePath`` and set ``_root``::

    class CachePath(BasePath):
        _root = "cache"

That's it. You get ``.get()``, ``.exists()``, and ``.__repr__`` for free.
"""

from pathlib import Path

# Project root – two levels up from this file (app/paths/base.py → project/)
BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent


class BasePath:
    """Abstract base for directory-scoped path helpers.

    Subclasses only need to define ``_root`` (relative to :data:``BASE_DIR``).
    All path helpers share the same interface so they're trivially swappable.

    Attributes:
        _root: Path fragment appended to ``BASE_DIR``, e.g. ``"data"`` or
               ``"resources/filters"``.
    """

    _root: str = ""

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        if not cls._root:
            raise TypeError(f"{cls.__name__} must define a non-empty '_root'")

    @classmethod
    def get(cls, *subfolders: str, ensure: bool = False) -> Path:
        """
        Return the absolute path for this directory,
        optionally with subfolders.

        Args:
            *subfolders: Additional path segments appended after ``_root``.
                         May include a filename as the last segment.
            ensure:      If ``True``, create the directory (or the file's
                         parent directory) when it does not exist yet.

        Returns:
            An absolute :class:``pathlib.Path``.

        Example::

            DataPath.get("raw", "report.xlsx", ensure=True)
            # creates  <root>/data/raw/  and returns the full file path
        """
        path: Path = BASE_DIR.joinpath(cls._root, *subfolders)

        if ensure:
            # If the last segment looks like a file, create its parent dir.
            target = path.parent if path.suffix else path
            target.mkdir(parents=True, exist_ok=True)

        return path

    @classmethod
    def exists(cls, *subfolders: str) -> bool:
        """Return ``True`` if the path exists on disk."""
        return cls.get(*subfolders).exists()

    @classmethod
    def __repr__(cls) -> str:
        return f"{cls.__name__}(root={BASE_DIR / cls._root})"
