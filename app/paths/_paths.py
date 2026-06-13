from .base import BasePath


class DataPath(BasePath):
    """Raw input data: ``<root>/data/``."""

    _root = "data"


class LogsPath(BasePath):
    """Log files: ``<root>/logs/``."""

    _root = "logs"


class ResourcesPath(BasePath):
    """Static resources: ``<root>/resources/``."""

    _root = "resources"
