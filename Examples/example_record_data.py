from pathlib import Path
import sys
from xensesdk import Sensor
import time 

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config_loader import load_float, load_path, load_sensor_id

if __name__ == '__main__':
    sensor = Sensor.create(load_sensor_id())
    save_dir = load_path("examples.record_data_dir", default="Examples/output")
    duration = load_float("examples.record_data_duration_seconds", default=5)

    sensor.startSaveSensorInfo(str(save_dir), [Sensor.OutputType.Difference, Sensor.OutputType.Rectify])
    time.sleep(duration)
    sensor.stopSaveSensorInfo()
    print("save ok")
    
    sensor.release()
