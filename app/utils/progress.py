"""Progress bar utilities built on top of ``tqdm``.

All project progress bars go through :class:`ProgressBar` to keep a
consistent visual style.

Usage::

    from app.utils.progress import ProgressBar

    # Wrap an iterable
    for item in ProgressBar.wrap(items, desc="Processing"):
        process(item)

    # Manual control
    with ProgressBar.manual(total=100, desc="Uploading") as bar:
        for chunk in chunks:
            upload(chunk)
            bar.update(1)
"""

from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from typing import Any, TypeVar

from tqdm import tqdm

from ._constants import BAR_FORMAT

T = TypeVar("T")


class ProgressBar:
    """
    Wrapper around ``tqdm`` for a uniform progress bar style
    across the project.
    """

    @staticmethod
    def wrap(
        iterable: Iterable[T],
        desc: str = "",
        total: int | None = None,
        colour: str = "cyan",
        **kwargs: Any,
    ) -> Iterable[T]:
        """Wrap *iterable* with a progress bar.

        Args:
            iterable: Any iterable to iterate over.
            desc: Label shown to the left of the bar.
            total: Override total count (useful for generators).
            colour: Bar colour name supported by ``tqdm``.
            **kwargs: Forwarded to :class:`tqdm.tqdm`.

        Returns:
            A ``tqdm``-wrapped iterable.
        """
        defaults: dict[str, Any] = {
            "desc": desc,
            "total": total,
            "bar_format": BAR_FORMAT,
            "colour": colour,
            "leave": True,
        }
        defaults.update(kwargs)
        return tqdm(iterable, **defaults)

    @staticmethod
    @contextmanager
    def manual(
        total: int,
        desc: str = "Working",
        colour: str = "cyan",
        **kwargs: Any,
    ) -> Iterator[tqdm]:
        """Context manager for a manually controlled progress bar.

        Args:
            total: Total number of steps.
            desc: Label shown to the left of the bar.
            colour: Bar colour.
            **kwargs: Forwarded to :class:`tqdm.tqdm`.

        Yields:
            A :class:`tqdm.tqdm` instance; call ``.update(n)`` to advance.

        Example::

            with ProgressBar.manual(total=len(rows), desc="Saving") as bar:
                for row in rows:
                    save(row)
                    bar.update(1)
        """
        bar = tqdm(
            total=total,
            desc=desc,
            colour=colour,
            bar_format=BAR_FORMAT,
            **kwargs,
        )
        try:
            yield bar
        finally:
            bar.close()
