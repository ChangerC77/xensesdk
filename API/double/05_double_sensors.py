import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
from xensesdk import Sensor

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = next(
    parent for parent in (SCRIPT_DIR, *SCRIPT_DIR.parents)
    if (parent / "config" / "config_loader.py").exists()
)
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config_loader import load_sensor_ids

OUTPUT_TYPES = (
    Sensor.OutputType.Rectify,
    Sensor.OutputType.Difference,
    Sensor.OutputType.Depth,
    Sensor.OutputType.Force,
    Sensor.OutputType.ForceNorm,
    Sensor.OutputType.ForceResultant,
    Sensor.OutputType.Marker2D,
    Sensor.OutputType.Mesh3D,
    Sensor.OutputType.Mesh3DInit,
    Sensor.OutputType.Mesh3DFlow,
    Sensor.OutputType.TimeStamp,
)

def parse_args():
    parser = argparse.ArgumentParser(description="read two Xense sensors simultaneously, write the sensor id in config/config.yaml.")
    parser.add_argument("sensor_ids",nargs="*",)
    return parser.parse_args()

def normalize_sensor_id(sensor_id):
    return int(sensor_id) if isinstance(sensor_id, str) and sensor_id.isdigit() else sensor_id


def resolve_sensor_ids():
    args = parse_args()
    if args.sensor_ids:
        if len(args.sensor_ids) != 2:
            raise ValueError("must connect 2 sensors, but got {}".format(len(args.sensor_ids)))
        return [normalize_sensor_id(sensor_id) for sensor_id in args.sensor_ids]
    return load_sensor_ids(required_count=2)

def read_sensor_info(sensor):
    return sensor.selectSensorInfo(*OUTPUT_TYPES)

def print_sensor_info(sensor_name, sensor_info):
    rectify, difference, depth, force, force_norm, force_resultant, marker2d, mesh3d, mesh3dinit, mesh3dflow, timestamp = sensor_info
    print(f"[{sensor_name}] Rectified image shape:", rectify.shape)                  # (700, 400, 3)
    print(f"[{sensor_name}] Difference image shape:", difference.shape)              # (700, 400, 3)
    print(f"[{sensor_name}] Depth image shape:", depth.shape)                        # (700, 400)
    print(f"[{sensor_name}] 3D force distribution shape:", force.shape)              # (35, 20, 3)
    print(f"[{sensor_name}] Normal force component:", force_norm.shape)              # (35, 20, 3)
    print(f"[{sensor_name}] 6-dimensional resultant force:", force_resultant.shape)  # (6,)
    print(f"[{sensor_name}] Tangential displacement shape:", marker2d.shape)         # (26, 14, 2)
    print(f"[{sensor_name}] Current frame 3D mesh shape:", mesh3d.shape)             # (35, 20, 3)
    print(f"[{sensor_name}] Initial 3D mesh shape:", mesh3dinit.shape)               # (35, 20, 3)
    print(f"[{sensor_name}] Mesh deformation vector:", mesh3dflow.shape)             # (35, 20, 3)
    print(f"[{sensor_name}] Sensor timestamp:", timestamp)                           # s


def main():
    sensor_ids = resolve_sensor_ids()
    sensors = []

    try:
        for sensor_id in sensor_ids:
            sensors.append(Sensor.create(sensor_id))

        with ThreadPoolExecutor(max_workers=2) as executor:
            sensor_infos = list(executor.map(read_sensor_info, sensors))

        for sensor_id, sensor_info in zip(sensor_ids, sensor_infos):
            print(f"\n===== Sensor {sensor_id} =====")
            print_sensor_info(sensor_id, sensor_info)
    finally:
        for sensor in sensors:
            sensor.release()

if __name__ == "__main__":
    main()
