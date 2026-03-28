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

    video_path = config["examples"]["data_processing_video_path"]
    video_path = Path(video_path)
    if not video_path.is_absolute():
        video_path = ROOT_DIR / video_path
    return video_path


def main():
    video_path = load_config()
    sensor_0 = Sensor.create(
        None,
        video_path=str(video_path)
    )
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
