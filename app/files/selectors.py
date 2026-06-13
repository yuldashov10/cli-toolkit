from pathlib import Path

import inquirer

from app.exceptions.base import FileOperationError

from .abstract import BaseSelectorAbstract


class DefaultFileSelector(BaseSelectorAbstract):
    """List all files in a directory (no extension filter)."""

    @classmethod
    def select(cls, path: Path) -> list[Path]:
        return sorted(p for p in Path(path).iterdir() if p.is_file())


class ExcelFileSelector(BaseSelectorAbstract):
    """List ``.xlsx`` and ``.xls`` files in a directory."""

    @classmethod
    def select(cls, path: Path) -> list[Path]:
        base = Path(path)
        return sorted([*base.glob("*.xlsx"), *base.glob("*.xls")])


class CSVFileSelector(BaseSelectorAbstract):
    """List ``.csv`` files in a directory."""

    @classmethod
    def select(cls, path: Path) -> list[Path]:
        return sorted(Path(path).glob("*.csv"))


class FileSelector:
    """Interactive file picker.

    Presents an ``inquirer.List`` of files in *path* filtered by *ext*,
    and returns the selected :class:`pathlib.Path`.

    Raises ``StopIteration`` if the user selects "Back".
    """

    _selectors: dict[str, type[BaseSelectorAbstract]] = {
        "xlsx": ExcelFileSelector,
        "xls": ExcelFileSelector,
        "csv": CSVFileSelector,
    }

    @classmethod
    def select(cls, path: Path, ext: str = "") -> Path:
        """Prompt the user to choose a file.

        Args:
            path: Directory to list files from.
            ext: Extension filter (e.g. ``"xlsx"``).
                Pass ``""`` for all files.

        Returns:
            The selected file path.

        Raises:
            FileOperationError: If no matching files are found.
            StopIteration: If the user selects "← Back".
        """
        selector = cls._selectors.get(ext, DefaultFileSelector)
        files = selector.select(path)

        if not files:
            label = f"'{ext}'" if ext else "any"
            raise FileOperationError(
                f"No {label} files found in {path}",
                path=path,
                hint="Check the directory or choose a different folder.",
            )

        choices = [f.name for f in files] + ["← Back"]

        answer = inquirer.prompt(
            [inquirer.List("file", message="Select a file", choices=choices)]
        )

        if not answer or answer["file"] == "← Back":
            raise StopIteration

        return next(f for f in files if f.name == answer["file"])

    @classmethod
    def all(cls, path: Path) -> list[Path]:
        """Return all files in *path* without prompting."""
        files = DefaultFileSelector.select(path)
        if not files:
            raise FileOperationError(f"No files found in {path}", path=path)
        return files


class DirSelector:
    """Interactive directory picker.

    Lists immediate subdirectories of *path* and lets the user choose one.
    """

    @classmethod
    def select(cls, path: Path) -> Path:
        """Prompt the user to choose a subdirectory.

        Args:
            path: Parent directory to list subdirectories from.

        Returns:
            The selected directory path.

        Raises:
            FileOperationError: If no subdirectories are found.
            StopIteration: If the user selects "← Back".
        """
        dirs = sorted(p for p in Path(path).iterdir() if p.is_dir())

        if not dirs:
            raise FileOperationError(
                f"No subdirectories found in {path}", path=path
            )

        choices = [d.name for d in dirs] + ["← Back"]

        answer = inquirer.prompt(
            [
                inquirer.List(
                    "dir", message="Select a directory", choices=choices
                )
            ]
        )

        if not answer or answer["dir"] == "← Back":
            raise StopIteration

        return next(d for d in dirs if d.name == answer["dir"])
