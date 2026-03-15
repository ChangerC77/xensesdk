from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config_loader import load_sensor_id, load_string
from xensesdk import ExampleView
from xensesdk import Sensor
from xensesdk import call_service


def main():
    master_ip = load_string("examples.remote_ip", default="192.168.1.120")
    preferred_sensor_id = load_sensor_id()
    
    # find all sensors
    ret = call_service(master_ip, "MasterService", "scan_sensor_sn")
    if ret["success"] is False:
        print(f"Failed to scan sensors: {ret['ret']}")
        sys.exit(1)
    else:
        print(f"Found sensors: {ret['ret']}")

    if preferred_sensor_id in ret["ret"]:
        serial_number = preferred_sensor_id
        print(f"Using configured sensor: {serial_number}")
    else:
        serial_number = list(ret["ret"].keys())[0]
        print(f"Configured sensor not found, using the first one: {serial_number}")

    # create a sensor
    sensor_0 = Sensor.create(serial_number, ip_address=master_ip)
    View = ExampleView(sensor_0)
    View2d = View.create2d(Sensor.OutputType.Difference, Sensor.OutputType.Depth)
    
    def callback():
        diff, depth = sensor_0.selectSensorInfo(Sensor.OutputType.Difference, Sensor.OutputType.Depth)
        View2d.setData(Sensor.OutputType.Difference, diff)
        View2d.setData(Sensor.OutputType.Depth, depth)
        View.setDepth(depth)
    View.setCallback(callback)

    View.show()
    sensor_0.release()
    sys.exit()


if __name__ == '__main__':
    main()
