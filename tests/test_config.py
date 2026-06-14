from pathlib import Path

import pytest

from app.config.loader import AppConfig, load_config
from app.exceptions import ConfigError


class TestAppConfig:
    def test_default_app_name(self) -> None:
        cfg = AppConfig()
        assert cfg.app_name == "cli-toolkit"

    def test_default_log_level(self) -> None:
        cfg = AppConfig()
        assert cfg.log_level == "INFO"

    def test_default_downloads_dir(self) -> None:
        cfg = AppConfig()
        assert cfg.downloads_dir == Path.home() / "Downloads"

    def test_custom_values(self) -> None:
        cfg = AppConfig(app_name="my-app", log_level="DEBUG")
        assert cfg.app_name == "my-app"
        assert cfg.log_level == "DEBUG"


class TestLoadConfig:
    def test_returns_defaults_when_no_files(self, tmp_path: Path) -> None:
        cfg = load_config(
            env_file=tmp_path / ".env",
            yaml_file=tmp_path / "config.yaml",
        )
        assert cfg.app_name == "cli-toolkit"
        assert cfg.log_level == "INFO"

    def test_yaml_overrides_defaults(
        self,
        yaml_config_file: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("APP_NAME", raising=False)
        monkeypatch.delenv("LOG_LEVEL", raising=False)
        cfg = load_config(
            env_file=tmp_path / ".env",
            yaml_file=yaml_config_file,
        )
        assert cfg.app_name == "yaml-app"
        assert cfg.log_level == "WARNING"

    def test_env_overrides_yaml(
        self,
        env_file: Path,
        yaml_config_file: Path,
    ) -> None:
        cfg = load_config(env_file=env_file, yaml_file=yaml_config_file)
        # env has APP_NAME=env-app, yaml has app_name=yaml-app
        assert cfg.app_name == "env-app"

    def test_env_log_level_uppercased(self, tmp_path: Path) -> None:
        env = tmp_path / ".env"
        env.write_text("LOG_LEVEL=debug\n", encoding="UTF-8")
        cfg = load_config(
            env_file=env,
            yaml_file=tmp_path / "config.yaml",
        )
        assert cfg.log_level == "DEBUG"

    def test_broken_yaml_raises_config_error(
        self, broken_yaml_config: Path, tmp_path: Path
    ) -> None:
        with pytest.raises(ConfigError):
            load_config(
                env_file=tmp_path / ".env",
                yaml_file=broken_yaml_config,
            )

    def test_env_variable_overrides_yaml(
        self,
        yaml_config_file: Path,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("APP_NAME", "env-override")
        cfg = load_config(
            env_file=tmp_path / ".env",
            yaml_file=yaml_config_file,
        )
        assert cfg.app_name == "env-override"

    def test_downloads_dir_is_path(self, tmp_path: Path) -> None:
        cfg = load_config(
            env_file=tmp_path / ".env",
            yaml_file=tmp_path / "config.yaml",
        )
        assert isinstance(cfg.downloads_dir, Path)
