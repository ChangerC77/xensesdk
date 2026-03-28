import argparse
from pathlib import Path
import sys

import yaml
from xensesdk import ExampleView
from xensesdk import Sensor

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = ROOT_DIR / "config" / "config.yaml"


def load_sensor_id():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default=str(DEFAULT_CONFIG_PATH), help="YAML file path")
    args = parser.parse_args()

    with open(args.config, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    return config["xense"]["sensor1_id"]


def main():
    sensor_0 = Sensor.create(load_sensor_id())
    View = ExampleView(sensor_0)
    View2d = View.create2d(Sensor.OutputType.Difference, Sensor.OutputType.Depth, Sensor.OutputType.Marker2D)

    def callback():
        force, res_force, mesh_init, src, diff, depth = sensor_0.selectSensorInfo(
            Sensor.OutputType.Force, 
            Sensor.OutputType.ForceResultant,
            Sensor.OutputType.Mesh3DInit,
            Sensor.OutputType.Rectify, 
            Sensor.OutputType.Difference, 
            Sensor.OutputType.Depth,
        )
        marker_img = sensor_0.drawMarkerMove(src)
        View2d.setData(Sensor.OutputType.Marker2D, marker_img)
        View2d.setData(Sensor.OutputType.Difference, diff)
        View2d.setData(Sensor.OutputType.Depth, depth)
        View.setForceFlow(force, res_force, mesh_init)
        View.setDepth(depth)

    View.setCallback(callback)
    View.show()
    sensor_0.release()
    sys.exit()

if __name__ == '__main__':
    main()
