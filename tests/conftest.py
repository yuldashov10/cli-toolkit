import json
from pathlib import Path

import pandas as pd
import pytest
import yaml


@pytest.fixture()
def xlsx_file(tmp_path: Path) -> Path:
    path = tmp_path / "sample.xlsx"
    pd.DataFrame(
        {"name": ["Alice", "Bob", "Charlie"], "value": [1, 2, 3]}
    ).to_excel(path, index=False, engine="openpyxl")
    return path


@pytest.fixture()
def csv_file(tmp_path: Path) -> Path:
    path = tmp_path / "sample.csv"
    pd.DataFrame(
        {"name": ["Alice", "Bob", "Charlie"], "value": [1, 2, 3]}
    ).to_csv(path, index=False)
    return path


@pytest.fixture()
def json_file(tmp_path: Path) -> Path:
    path = tmp_path / "sample.json"
    path.write_text(
        json.dumps([{"name": "Alice"}, {"name": "Bob"}]), encoding="UTF-8"
    )
    return path


@pytest.fixture()
def yaml_file(tmp_path: Path) -> Path:
    path = tmp_path / "sample.yaml"
    path.write_text(
        yaml.dump([{"name": "Alice"}, {"name": "Bob"}]), encoding="UTF-8"
    )
    return path


@pytest.fixture()
def broken_json_file(tmp_path: Path) -> Path:
    path = tmp_path / "broken.json"
    path.write_text("{invalid json", encoding="UTF-8")
    return path


@pytest.fixture()
def broken_yaml_file(tmp_path: Path) -> Path:
    path = tmp_path / "broken.yaml"
    path.write_text("key: [unclosed", encoding="UTF-8")
    return path


@pytest.fixture()
def dir_with_xlsx(tmp_path: Path) -> Path:
    (tmp_path / "report.xlsx").touch()
    (tmp_path / "data.xlsx").touch()
    (tmp_path / "notes.txt").touch()
    return tmp_path


@pytest.fixture()
def dir_with_csv(tmp_path: Path) -> Path:
    (tmp_path / "file1.csv").touch()
    (tmp_path / "file2.csv").touch()
    return tmp_path


@pytest.fixture()
def dir_with_subdirs(tmp_path: Path) -> Path:
    (tmp_path / "subdir_a").mkdir()
    (tmp_path / "subdir_b").mkdir()
    return tmp_path


@pytest.fixture()
def empty_dir(tmp_path: Path) -> Path:
    return tmp_path


@pytest.fixture()
def env_file(tmp_path: Path) -> Path:
    path = tmp_path / ".env"
    path.write_text("APP_NAME=env-app\nLOG_LEVEL=DEBUG\n", encoding="UTF-8")
    return path


@pytest.fixture()
def yaml_config_file(tmp_path: Path) -> Path:
    path = tmp_path / "config.yaml"
    path.write_text(
        "app_name: yaml-app\nlog_level: WARNING\n", encoding="UTF-8"
    )
    return path


@pytest.fixture()
def broken_yaml_config(tmp_path: Path) -> Path:
    path = tmp_path / "config.yaml"
    path.write_text("key: [unclosed", encoding="UTF-8")
    return path
