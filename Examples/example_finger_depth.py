import argparse
from pathlib import Path
import sys

import yaml
from xensesdk import ExampleView
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
    finger_config_path = config["examples"]["finger_config_path"]
    if finger_config_path in (None, ""):
        return sensor_id, None

    finger_config_path = Path(finger_config_path)
    if not finger_config_path.is_absolute():
        finger_config_path = ROOT_DIR / finger_config_path
    return sensor_id, finger_config_path


def main():
    sensor_id, finger_config_path = load_config()
    if finger_config_path is None:
        sensor_0 = Sensor.create(sensor_id)
    else:
        sensor_0 = Sensor.create(
            sensor_id,
            config_path=str(finger_config_path)
        )
    View = ExampleView(sensor_0)
    View2d = View.create2d(Sensor.OutputType.Difference, Sensor.OutputType.Depth)

    def callback():
        diff, depth = sensor_0.selectSensorInfo(
            Sensor.OutputType.Difference, 
            Sensor.OutputType.Depth,
        )
        View2d.setData(Sensor.OutputType.Difference, diff)
        View2d.setData(Sensor.OutputType.Depth, depth)
        View.setDepth(depth)

    View.setCallback(callback)
    View.show()
    sensor_0.release()
    sys.exit()

if __name__ == '__main__':
    main()
