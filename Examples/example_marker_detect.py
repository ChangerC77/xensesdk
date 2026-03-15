from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config_loader import load_sensor_id
from xensesdk import ExampleView
from xensesdk import Sensor


def main():
    sensor_0 = Sensor.create(load_sensor_id())
    View = ExampleView(sensor_0)
    View2d = View.create2d(Sensor.OutputType.Rectify, Sensor.OutputType.MarkerUnorder)
    
    def callback():
        src, depth, marker_unordered= sensor_0.selectSensorInfo(Sensor.OutputType.Rectify, Sensor.OutputType.Depth, Sensor.OutputType.MarkerUnorder)
        marker_img = sensor_0.drawMarker(src, marker_unordered)
        View2d.setData(Sensor.OutputType.Rectify, src)
        View2d.setData(Sensor.OutputType.MarkerUnorder, marker_img)
        View.setDepth(depth)
        View.setMarkerUnorder(marker_unordered)

    View.setCallback(callback)
    View.show()
    sensor_0.release()
    sys.exit()

if __name__ == '__main__':
    main()
