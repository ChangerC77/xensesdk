from pathlib import Path

import yaml


CONFIG_DIR = Path(__file__).resolve().parent
ROOT_DIR = CONFIG_DIR.parent
CONFIG_PATH = CONFIG_DIR / "config.yaml"
_MISSING = object()


def load_config():
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file) or {}


def get_config_value(path, default=_MISSING):
    value = load_config()
    for key in path.split("."):
        if not isinstance(value, dict) or key not in value:
            if default is _MISSING:
                raise KeyError(f"未在 {CONFIG_PATH} 中找到 {path} 配置")
            return default
        value = value[key]
    return value


def load_sensor_id():
    sensor_id = get_config_value("xense.sensor_id", default=None)
    if not sensor_id:
        sensor_id = get_config_value("xense.sensor1_id", default=None)
    if not sensor_id:
        raise ValueError(f"{CONFIG_PATH} 中的 xense.sensor_id 不能为空")
    return str(sensor_id)


def load_string(path, default=_MISSING):
    value = get_config_value(path, default=default)
    if value in (None, ""):
        if default is _MISSING:
            raise ValueError(f"{CONFIG_PATH} 中的 {path} 不能为空")
        return None if default in (None, "") else str(default)
    return str(value)


def load_path(path, default=_MISSING):
    value = load_string(path, default=default)
    if value is None:
        return None
    path_value = Path(value)
    return path_value if path_value.is_absolute() else ROOT_DIR / path_value


def load_float(path, default=_MISSING):
    value = get_config_value(path, default=default)
    if value in (None, ""):
        if default is _MISSING:
            raise ValueError(f"{CONFIG_PATH} 中的 {path} 不能为空")
        value = default
    return float(value)
