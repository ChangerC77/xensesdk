import argparse
from pathlib import Path
import time

import yaml
from xensesdk import Sensor

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = ROOT_DIR / "config" / "config.yaml"


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG_PATH), help="YAML file path")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    sensor_id = config["xense"]["sensor1_id"]
    save_dir = Path(config["examples"]["record_data_dir"])
    if not save_dir.is_absolute():
        save_dir = ROOT_DIR / save_dir
    duration = float(config["examples"]["record_data_duration_seconds"])
    return sensor_id, save_dir, duration


if __name__ == '__main__':
    sensor_id, save_dir, duration = load_config()
    sensor = Sensor.create(sensor_id)

    sensor.startSaveSensorInfo(str(save_dir), [Sensor.OutputType.Difference, Sensor.OutputType.Rectify])
    time.sleep(duration)
    sensor.stopSaveSensorInfo()
    print("save ok")
    
    sensor.release()
