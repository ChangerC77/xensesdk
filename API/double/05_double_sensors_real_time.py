import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
import time

import numpy as np
from xensesdk import Sensor


# Add the repo root to sys.path so this example can reuse shared config helpers.
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = next(
    parent for parent in (SCRIPT_DIR, *SCRIPT_DIR.parents)
    if (parent / "config" / "config_loader.py").exists()
)
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config_loader import load_float, load_sensor_ids

# Only request the outputs that this demo actually prints.
OUTPUT_TYPES = (
    Sensor.OutputType.Rectify,
    Sensor.OutputType.ForceResultant,
    Sensor.OutputType.Marker2D,
)


def read_sensor_info(sensor):
    """Read one frame of the requested outputs from a sensor."""
    return sensor.selectSensorInfo(*OUTPUT_TYPES)


def main():
    parser = argparse.ArgumentParser(
        description="read two Xense sensors simultaneously, write the sensor id in config/config.yaml."
    )
    parser.add_argument("sensor_ids", nargs="*")
    parser.add_argument("--fps", type=float, default=None)
    args = parser.parse_args()

    # Prefer command-line values; otherwise fall back to config/config.yaml.
    sensor_ids = args.sensor_ids or load_sensor_ids(required_count=2)
    if len(sensor_ids) != 2:
        raise ValueError(f"must connect 2 sensors, but got {len(sensor_ids)}")

    fps = args.fps if args.fps is not None else load_float("xense.freq", default=60.0)
    frame_interval = 1.0 / fps
    sensors = []

    try:
        # Create both sensor instances once and reuse them in the loop.
        sensors = [Sensor.create(sensor_id) for sensor_id in sensor_ids]
        print("Press Ctrl+C to stop realtime reading.")

        with ThreadPoolExecutor(max_workers=2) as executor:
            frame_index = 0
            while True:
                loop_start = time.perf_counter()
                frame_index += 1

                # Read both sensors in parallel so their frames stay close in time.
                sensor_infos = list(executor.map(read_sensor_info, sensors))
                print(f"\nFrame {frame_index}")

                for sensor_id, sensor_info in zip(sensor_ids, sensor_infos):
                    rectify, force_resultant, marker2d = sensor_info
                    print(
                        f"[Sensor {sensor_id}] "
                        f"rectify_shape={rectify.shape}, "
                        f"force_resultant={np.array2string(force_resultant, precision=3, suppress_small=True)}, "
                        f"marker2d_shape={marker2d.shape}"
                    )

                # Sleep the remaining time so the loop roughly follows the target fps.
                remaining = frame_interval - (time.perf_counter() - loop_start)
                if remaining > 0:
                    time.sleep(remaining)
    except KeyboardInterrupt:
        print("\nRealtime reading stopped by user.")
    finally:
        # Always release sensor handles before exiting.
        for sensor in sensors:
            sensor.release()


if __name__ == "__main__":
    main()
