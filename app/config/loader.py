"""Configuration loader: merges ``.env`` and ``config.yaml``.

Usage::

    from app.config.loader import load_config

    cfg = load_config()
    print(cfg.app_name)
    print(cfg.log_level)
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from dotenv import load_dotenv

from app.paths import BASE_DIR


@dataclass
class AppConfig:
    """Typed application configuration.

    Extend this dataclass to add project-specific settings.
    All path fields default to values from :mod:``app.paths``.
    """

    app_name: str = "cli-toolkit"
    log_level: str = "INFO"
    downloads_dir: Path = field(
        default_factory=lambda: Path.home() / "Downloads"
    )

    # --- Add your own settings below ---
    # api_key: str = ""
    # db_url: str = ""


def load_config(
    env_file: Path | None = None,
    yaml_file: Path | None = None,
) -> AppConfig:
    """Load configuration from ``.env`` and ``config.yaml``.

    Precedence (highest → lowest):
    1. Environment variables (including those from ``.env``)
    2. ``config.yaml`` values
    3. ``AppConfig`` dataclass defaults

    Args:
        env_file:  Path to ``.env``. Defaults to ``<BASE_DIR>/.env``.
        yaml_file: Path
        to ``config.yaml``. Defaults to ``<BASE_DIR>/config.yaml``.

    Raises:
        ConfigError: If ``config.yaml`` exists but cannot be parsed.
    """
    from app.exceptions import ConfigError

    load_dotenv(dotenv_path=env_file or BASE_DIR / ".env", override=False)

    yaml_data: dict = {}
    yaml_path = yaml_file or BASE_DIR / "config.yaml"
    if yaml_path.exists():
        try:
            with open(yaml_path, encoding="utf-8") as fh:
                yaml_data = yaml.safe_load(fh) or {}
        except yaml.YAMLError as exc:
            raise ConfigError(
                f"Failed to parse {yaml_path}", hint=str(exc)
            ) from exc

    def _get(key: str, fallback: str) -> str:
        return os.environ.get(key.upper()) or str(
            yaml_data.get(key.lower(), fallback)
        )

    return AppConfig(
        app_name=_get("APP_NAME", "cli-toolkit"),
        log_level=_get("LOG_LEVEL", "INFO").upper(),
        downloads_dir=Path(
            _get("DOWNLOADS_DIR", str(Path.home() / "Downloads"))
        ),
    )
