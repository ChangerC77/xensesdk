"""
Here are three methods to connect tactile sensors

Example 1: Start Sensor via Serial Number (SN)

Example 2: Start Sensor via Camera ID

Example 3: Open Stored Offline Data

Example 4: Connect to Sensor on Remote Computing Board

"""

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

from config.config_loader import load_sensor_id


sensor_id = load_sensor_id()

# Example 1: Start Sensor via Serial Number (SN)
# Create an instance using the sensor serial number (SN) from /config/config.yaml
sensor = Sensor.create(sensor_id)

# Create an instance using the camera ID (e.g., 0, 1)
# Example 2: Start Sensor via Camera ID
# sensor = Sensor.create(0)

# Example 3: Open Stored Offline Data
# Load local data via video_path (set cam_id to None)
# sensor = Sensor.create(None, video_path=r"data.h5")

# Example 4: Connect to Sensor on Remote Computing Board
# Specify the IP address to connect to the remote sensor
# sensor = Sensor.create('OP000064', ip_address="192.168.66.66")

# Release resources after use
sensor.release()

"""
output
Found Xense devices: {'OG000708': 6, 'OG000703': 10}
Read config from OG000703: cam_id_10 success!
In SDK: [Network] Camera 10 connected
Init infer engine
infer session using GPU
In SDK: [Network] Camera 10 disconnected
"""
