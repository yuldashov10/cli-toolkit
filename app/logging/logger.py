"""Coloured, rotating-file logger.

Usage::

    from app.logging import get_logger

    logger = get_logger("my_module")
    logger.info("Processing started")
    logger.error("Something went wrong")

The logger is a singleton per name: calling ``get_logger("app")`` twice
returns the same :class:`logging.Logger` instance.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from colorama import Fore, Style, init

from ._constants import (
    LOG_BACKUP_COUNT,
    LOG_CONSOLE_DATE_FORMAT,
    LOG_CONSOLE_FORMAT,
    LOG_DATE_FORMAT,
    LOG_FILE_FORMAT,
    LOG_FILE_MAX_BYTES,
)

init(autoreset=True)


class ColoredFormatter(logging.Formatter):
    """Formatter that prepends ANSI colour codes based on log level."""

    _COLORS: dict[int, str] = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        color = self._COLORS.get(record.levelno, Fore.WHITE)
        return f"{color}{super().format(record)}{Style.RESET_ALL}"


class ProjectLogger:
    """Singleton-per-name logger factory.

    Creates a logger with two handlers:
        - **Console** – coloured output via :class:`ColoredFormatter`.
        - **File** – rotating file handler (plain text, no colours).
    """

    _loggers: dict[str, logging.Logger] = {}

    @classmethod
    def get_logger(
        cls,
        name: str = "app",
        log_file: str = "logs/app.log",
        level: int = logging.DEBUG,
    ) -> logging.Logger:
        """Return a named logger, creating it on first call.

        Subsequent calls with the same *name* return the cached instance
        without re-adding handlers.

        Args:
            name:     Logger name, typically the module or component name.
            log_file: Path to the log
            file (parent dirs are created automatically).
            level:    Minimum log level. Defaults to ``logging.DEBUG``.

        Example::

            logger = ProjectLogger.get_logger(
                    "data_handler", log_file="logs/data.log"
                )
            logger.warning("Large file detected")
        """
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.handlers.clear()

        log_path = cls._ensure_log_dir(log_file)
        logger.addHandler(cls._file_handler(log_path))
        logger.addHandler(cls._console_handler())
        logger.propagate = False  # avoid double output from root logger

        cls._loggers[name] = logger
        return logger

    @staticmethod
    def _file_handler(log_path: Path) -> RotatingFileHandler:
        handler = RotatingFileHandler(
            log_path,
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="UTF-8",
        )
        handler.setFormatter(
            logging.Formatter(LOG_FILE_FORMAT, datefmt=LOG_DATE_FORMAT)
        )
        return handler

    @staticmethod
    def _console_handler() -> logging.StreamHandler:
        handler = logging.StreamHandler()
        handler.setFormatter(
            ColoredFormatter(
                LOG_CONSOLE_FORMAT, datefmt=LOG_CONSOLE_DATE_FORMAT
            )
        )
        return handler

    @staticmethod
    def _ensure_log_dir(file: str) -> Path:
        log_path = Path(file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        return log_path


def get_logger(
    name: str = "app", log_file: str = "logs/app.log"
) -> logging.Logger:
    """Module-level shortcut for :meth:`ProjectLogger.get_logger`.

    Prefer this in application code::

        from app.logging import get_logger
        logger = get_logger(__name__)
    """
    return ProjectLogger.get_logger(name, log_file)
