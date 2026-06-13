"""
Abstract base classes for CLI commands.
"""

from abc import ABC, abstractmethod


class Command(ABC):
    """Base class for all CLI commands.

    Every command must define a `label` (shown in the menu)
    and an `execute` method (called when the user selects it).
    """

    @property
    @abstractmethod
    def label(self) -> str:
        """Label displayed in the interactive menu."""
        raise NotImplementedError

    @abstractmethod
    def execute(self) -> None:
        """Execute the command logic."""
        raise NotImplementedError
