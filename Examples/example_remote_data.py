import argparse
from pathlib import Path
import sys

import yaml
from xensesdk import ExampleView
from xensesdk import Sensor
from xensesdk import call_service

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = ROOT_DIR / "config" / "config.yaml"


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG_PATH), help="YAML file path")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    return config["xense"]["sensor1_id"], config["examples"]["remote_ip"]


def main():
    preferred_sensor_id, master_ip = load_config()
    
    # find all sensors
    ret = call_service(master_ip, "MasterService", "scan_sensor_sn")
    if ret["success"] is False:
        print(f"Failed to scan sensors: {ret['ret']}")
        sys.exit(1)
    else:
        print(f"Found sensors: {ret['ret']}")

    if preferred_sensor_id in ret["ret"]:
        serial_number = preferred_sensor_id
        print(f"Using configured sensor: {serial_number}")
    else:
        serial_number = list(ret["ret"].keys())[0]
        print(f"Configured sensor not found, using the first one: {serial_number}")

    # create a sensor
    sensor_0 = Sensor.create(serial_number, ip_address=master_ip)
    View = ExampleView(sensor_0)
    View2d = View.create2d(Sensor.OutputType.Difference, Sensor.OutputType.Depth)
    
    def callback():
        diff, depth = sensor_0.selectSensorInfo(Sensor.OutputType.Difference, Sensor.OutputType.Depth)
        View2d.setData(Sensor.OutputType.Difference, diff)
        View2d.setData(Sensor.OutputType.Depth, depth)
        View.setDepth(depth)
    View.setCallback(callback)

    View.show()
    sensor_0.release()
    sys.exit()


if __name__ == '__main__':
    main()
