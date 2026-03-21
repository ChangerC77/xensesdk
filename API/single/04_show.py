from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = next(
    parent for parent in (SCRIPT_DIR, *SCRIPT_DIR.parents)
    if (parent / "config" / "config_loader.py").exists()
)
SAVE_DIR = SCRIPT_DIR / "test_dir"  # Storage directory
SAVE_DIR.mkdir(parents=True, exist_ok=True)
import cv2
import sys
import time
import numpy as np

from xensesdk import Sensor


if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config_loader import load_float, load_sensor_id

sensor_id = load_sensor_id()


def get_runtime_dir():
    return SAVE_DIR / f"runtime_{sensor_id}"


def create_solver():
    runtime_dir = get_runtime_dir()
    if not runtime_dir.exists():
        raise FileNotFoundError(f"未找到运行时配置: {runtime_dir}，请先执行保存数据。")
    return Sensor.createSolver(runtime_dir)


def solve_depth(sensor_solver, rectify_image):
    depth, _, _ = sensor_solver.selectSensorInfo(
        Sensor.OutputType.Depth,
        Sensor.OutputType.Force,
        Sensor.OutputType.Difference,
        rectify_image=rectify_image
    )
    return np.clip(depth * 200, 0, 255).astype(np.uint8)


def window_closed(window_name):
    return cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1


def process_window_events(frame_interval, start_time):
    elapsed = time.time() - start_time
    wait_ms = max(1, int((frame_interval - elapsed) * 1000))
    cv2.waitKeyEx(wait_ms)

def realtime_display():
    fps = load_float("xense.freq", default=30.0)
    frame_interval = 1.0 / fps if fps > 0 else 0.0
    sensor = Sensor.create(sensor_id)

    sensor.exportRuntimeConfig(SAVE_DIR)
    sensor_solver = create_solver()

    cv2.namedWindow('Rectify', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Depth', cv2.WINDOW_NORMAL)

    print("press Ctrl+C to exit real-time display")

    try:
        while True:
            start_time = time.time()
            rectify = sensor.selectSensorInfo(Sensor.OutputType.Rectify)
            depth_vis = solve_depth(sensor_solver, rectify)

            cv2.imshow('Rectify', rectify)
            cv2.imshow('Depth', depth_vis)

            if window_closed('Rectify') or window_closed('Depth'):
                break

            process_window_events(frame_interval, start_time)
    except KeyboardInterrupt:
        print("\n realtime display stopped by user.")
    except Exception as e:
        print(f"error occurs: {e}")
    finally:
        cv2.destroyAllWindows()
        sensor_solver.release()
        sensor.release()
        print("sensor relase")

if __name__ == '__main__':
    realtime_display()
