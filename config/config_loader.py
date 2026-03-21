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
    if sensor_id not in (None, ""):
        return str(sensor_id)
    return load_sensor_ids(required_count=1)[0]


def load_sensor_ids(required_count=None):
    sensor_ids = get_config_value("xense.sensor_ids", default=None)
    if sensor_ids not in (None, ""):
        if not isinstance(sensor_ids, (list, tuple)):
            raise TypeError(f"{CONFIG_PATH} 中的 xense.sensor_ids 必须是列表")
        sensor_ids = [str(sensor_id) for sensor_id in sensor_ids if sensor_id not in (None, "")]
    else:
        sensor_ids = []
        for index in range(1, 9):
            sensor_id = get_config_value(f"xense.sensor{index}_id", default=None)
            if sensor_id not in (None, ""):
                sensor_ids.append(str(sensor_id))

        if not sensor_ids:
            sensor_id = get_config_value("xense.sensor_id", default=None)
            if sensor_id not in (None, ""):
                sensor_ids.append(str(sensor_id))

    if required_count is not None and len(sensor_ids) < required_count:
        raise ValueError(
            f"{CONFIG_PATH} 中至少需要配置 {required_count} 个传感器 ID，可使用 "
            "xense.sensor_ids 或 xense.sensor1_id/xense.sensor2_id"
        )

    if not sensor_ids:
        raise ValueError(
            f"{CONFIG_PATH} 中的 xense.sensor_id、xense.sensor_ids 或 "
            "xense.sensor1_id/xense.sensor2_id 不能为空"
        )

    return sensor_ids[:required_count] if required_count is not None else sensor_ids


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
