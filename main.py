"""Application entry point.

Run with::

    poetry run python main.py
    # or
    make run
"""

from app.cli.commands import BackCommand, ExitCommand, HelpCommand
from app.cli.menu import Menu
from app.config.loader import load_config
from app.logging import get_logger
from app.paths import LogsPath

cfg = load_config()
logger = get_logger("app", log_file=str(LogsPath.get("app.log")))


def build_menu() -> Menu:
    """Construct the main menu tree."""
    file_menu = Menu(
        title="Files",
        items=[
            HelpCommand(),
            BackCommand(),
        ],
    )

    return Menu(
        title="Main Menu",
        items=[
            file_menu,
            ExitCommand(),
        ],
    )


def main() -> None:
    logger.info("Starting %s", cfg.app_name)
    menu = build_menu()

    while True:
        try:
            menu.execute()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Shutting down.")
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
