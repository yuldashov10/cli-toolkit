"""
Interactive CLI menu built on top of inquirer.
"""

import inquirer

from .abstract import Command


class Menu(Command):
    """Recursive interactive menu.

    Displays a list of commands using `inquirer.List` and executes
    the selected one. Exits the current menu loop when a child command
    raises ``StopIteration`` (i.e. "Back").

    Example::

        menu = Menu("Main menu", [
            Menu("Sub-menu", [HelpCommand(), BackCommand()]),
            ExitCommand(),
        ])
        menu.execute()
    """

    def __init__(self, title: str, items: list[Command]) -> None:
        self._title = title
        self.items = items

    @property
    def label(self) -> str:
        return self._title

    def execute(self) -> None:
        """Run the menu loop until the user goes back or exits."""
        while True:
            mapping: dict[str, Command] = {
                item.label: item for item in self.items
            }

            answer = inquirer.prompt(
                [
                    inquirer.List(
                        "choice", message=self._title, choices=list(mapping)
                    )
                ]
            )

            if not answer:
                break

            try:
                mapping[answer["choice"]].execute()
            except StopIteration:
                break
