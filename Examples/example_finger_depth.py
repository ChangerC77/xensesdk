from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config_loader import load_path, load_sensor_id
from xensesdk import ExampleView
from xensesdk import Sensor


def main():
    finger_config_path = load_path("examples.finger_config_path", default=None)
    if finger_config_path is None:
        sensor_0 = Sensor.create(load_sensor_id())
    else:
        sensor_0 = Sensor.create(
            load_sensor_id(),
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
