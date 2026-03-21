import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import time

import numpy as np
from xensesdk import Sensor


SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = next(
    parent for parent in (SCRIPT_DIR, *SCRIPT_DIR.parents)
    if (parent / "config" / "config_loader.py").exists()
)
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config_loader import load_float, load_sensor_ids


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
    parser.add_argument("sensor_ids", nargs="*",)
    parser.add_argument("--fps", type=float, default=None,)
    return parser.parse_args()

def normalize_sensor_id(sensor_id):
    return int(sensor_id) if isinstance(sensor_id, str) and sensor_id.isdigit() else sensor_id

def resolve_sensor_ids(args):
    if args.sensor_ids:
        if len(args.sensor_ids) != 2:
            raise ValueError(
                "need two sensors, you should input exactly 2 sensors IDs in config/config.yaml"
            )
        return [normalize_sensor_id(sensor_id) for sensor_id in args.sensor_ids]
    return load_sensor_ids(required_count=2)


def read_sensor_info(sensor):
    return sensor.selectSensorInfo(*OUTPUT_TYPES)


def print_sensor_shapes(sensor_name, sensor_info):
    rectify, difference, depth, force, force_norm, force_resultant, marker2d, mesh3d, mesh3dinit, mesh3dflow, timestamp = sensor_info
    print(f"[{sensor_name}] Rectified image shape:", rectify.shape)
    print(f"[{sensor_name}] Difference image shape:", difference.shape)
    print(f"[{sensor_name}] Depth image shape:", depth.shape)
    print(f"[{sensor_name}] 3D force distribution shape:", force.shape)
    print(f"[{sensor_name}] Normal force component:", force_norm.shape)
    print(f"[{sensor_name}] 6-dimensional resultant force shape:", force_resultant.shape)
    print(f"[{sensor_name}] Tangential displacement shape:", marker2d.shape)
    print(f"[{sensor_name}] Current frame 3D mesh shape:", mesh3d.shape)
    print(f"[{sensor_name}] Initial 3D mesh shape:", mesh3dinit.shape)
    print(f"[{sensor_name}] Mesh deformation vector shape:", mesh3dflow.shape)
    print(f"[{sensor_name}] Sensor timestamp:", timestamp)


def format_force_resultant(force_resultant):
    return np.array2string(force_resultant, precision=3, suppress_small=True)


def calculate_frequency(current_timestamp, previous_timestamp):
    if previous_timestamp is None:
        return None

    delta = current_timestamp - previous_timestamp
    if delta <= 0:
        return None
    return 1.0 / delta

def format_frequency(frequency):
    return "N/A" if frequency is None else f"{frequency:.2f} Hz"

def print_frame_summary(frame_index, sensor_ids, sensor_infos, elapsed, loop_frequency, sensor_frequencies):
    print(
        f"\nFrame {frame_index} | loop_time={elapsed:.4f}s | "
        f"loop_fps={format_frequency(loop_frequency)}"
    )
    for sensor_id, sensor_info, sensor_frequency in zip(sensor_ids, sensor_infos, sensor_frequencies):
        _, _, depth, _, _, force_resultant, _, _, _, _, timestamp = sensor_info
        print(
            f"[{sensor_id}] timestamp={timestamp:.6f}, "
            f"sensor_fps={format_frequency(sensor_frequency)}, "
            f"depth_shape={depth.shape}, "
            f"force_resultant={format_force_resultant(force_resultant)}"
        )

def main():
    args = parse_args()
    sensor_ids = resolve_sensor_ids(args)
    sensors = []
    fps = args.fps if args.fps is not None else load_float("xense.freq", default=60.0)
    frame_interval = 1.0 / fps if fps > 0 else 0.0
    previous_timestamps = [None, None]
    previous_loop_start = None

    try:
        for sensor_id in sensor_ids:
            sensors.append(Sensor.create(sensor_id))

        print("Press Ctrl+C to stop realtime reading.")

        with ThreadPoolExecutor(max_workers=2) as executor:
            frame_index = 0
            while True:
                loop_start = time.perf_counter()
                futures = [executor.submit(read_sensor_info, sensor) for sensor in sensors]
                sensor_infos = [future.result() for future in futures]
                frame_index += 1
                sensor_frequencies = []

                for index, sensor_info in enumerate(sensor_infos):
                    timestamp = sensor_info[-1]
                    sensor_frequencies.append(
                        calculate_frequency(timestamp, previous_timestamps[index])
                    )
                    previous_timestamps[index] = timestamp

                if frame_index == 1:
                    print("\nFirst frame data shapes:")
                    for sensor_id, sensor_info in zip(sensor_ids, sensor_infos):
                        print(f"\n===== Sensor {sensor_id} =====")
                        print_sensor_shapes(sensor_id, sensor_info)

                elapsed = time.perf_counter() - loop_start
                loop_frequency = calculate_frequency(loop_start, previous_loop_start)
                print_frame_summary(
                    frame_index,
                    sensor_ids,
                    sensor_infos,
                    elapsed,
                    loop_frequency,
                    sensor_frequencies,
                )
                previous_loop_start = loop_start

                remaining = frame_interval - (time.perf_counter() - loop_start)
                if remaining > 0:
                    time.sleep(remaining)
    except KeyboardInterrupt:
        print("\nRealtime reading stopped by user.")
    finally:
        for sensor in sensors:
            sensor.release()


if __name__ == "__main__":
    main()
