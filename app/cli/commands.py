"""
Built-in CLI commands available in every project.
"""

from .abstract import Command


class BackCommand(Command):
    """Navigate one level up in the menu hierarchy."""

    label: str = "← Back"

    def execute(self) -> None:
        raise StopIteration


class ExitCommand(Command):
    """Terminate the application."""

    label: str = "✕ Exit"

    def execute(self) -> None:
        raise SystemExit


class HelpCommand(Command):
    """Display a help message. Override ``message`` in subclasses."""

    label: str = "? Help"
    message: str = "No help text provided."

    def execute(self) -> None:
        print(f"\n{self.message}\n")
