import argparse
from pathlib import Path
import yaml
import cv2
import time
import numpy as np

from xensesdk import Sensor

parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, default='config/config.yaml', help='YAML file path')
args = parser.parse_args()

with open(args.config, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)
    sensor_id = config['xense']['sensor1_id']
    fps = config['xense']['freq']

SAVE_DIR = Path(__file__).resolve().parent / "test_dir"  # Storage directory
SAVE_DIR.mkdir(parents=True, exist_ok=True)

def save_data():
    duration = 3   # seconds
    if fps <= 0:
        raise ValueError("config/config.yaml 中的 xense.freq 必须大于 0")
    frame_interval = 1.0 / fps
    total_frames = max(1, int(round(fps * duration)))

    sensor_0 = Sensor.create(sensor_id)
    for i in range(total_frames):
        start_time = time.time()

        # Capture one frame
        rec = sensor_0.selectSensorInfo(Sensor.OutputType.Rectify)  

        # Generate filename
        filename = SAVE_DIR / f"{sensor_id}_{i:03d}.png"

        # Save image
        cv2.imwrite(str(filename), rec)
        print(f"Saved {filename}")

        # Control frame rate
        elapsed = time.time() - start_time
        sleep_time = frame_interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    # Export configuration
    sensor_0.exportRuntimeConfig(SAVE_DIR)

    sensor_0.release()

def replay_data():
    sensor_solver = Sensor.createSolver(SAVE_DIR / f"runtime_{sensor_id}")
    for png_file in sorted(SAVE_DIR.glob("*.png")):
        if not png_file.name.endswith("_depth.png"):
            img = cv2.imread(str(png_file), cv2.IMREAD_UNCHANGED)
            depth, force, diff = sensor_solver.selectSensorInfo(
                Sensor.OutputType.Depth,
                Sensor.OutputType.Force,
                Sensor.OutputType.Difference,
                rectify_image=img
            )
            depth_vis = np.clip(depth*200, 0, 255)
            cv2.imwrite(SAVE_DIR / f"{png_file.stem}_depth.png", depth_vis)

    sensor_solver.release()

if __name__ == '__main__':
    save_data()
    replay_data()
    print("Data saved and replayed successfully.")
