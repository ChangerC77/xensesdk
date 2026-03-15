from pathlib import Path
import yaml

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR / "config" / "config.yaml"

def load_sensor_id():
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    try:
        sensor_id = config["xense"]["sensor1_id"]
    except KeyError as exc:
        raise KeyError(
            f"未在 {CONFIG_PATH} 中找到 xense.sensor1_id 配置"
        ) from exc

    if not sensor_id:
        raise ValueError(f"{CONFIG_PATH} 中的 xense.sensor1_id 不能为空")

    return str(sensor_id)