from pathlib import Path
import sys

from xensesdk import Sensor


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config.config_loader import load_sensor_id


sensor_id = load_sensor_id()

# Create sensor instance
sensor = Sensor.create(sensor_id)

# Retrieve specified types of sensor data
rectify, difference, depth, force, force_norm, force_resultant, marker2d, mesh3d, mesh3dinit, mesh3dflow, timestamp = sensor.selectSensorInfo(
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
    Sensor.OutputType.TimeStamp

)

# Output data shapes (example)
print("Rectified image shape:", rectify.shape)                  # (700, 400, 3)
print("Difference image shape:", difference.shape)              # (700, 400, 3)
print("Depth image shape:", depth.shape)                        # (700, 400)
print("3D force distribution shape:", force.shape)              # (35, 20, 3)
print("Normal force component:", force_norm.shape)              # (35, 20, 3)
print("6-dimensional resultant force:", force_resultant.shape)  # (6,)
print("Tangential displacement shape:", marker2d.shape)         # (26,14,2)
print("Current frame 3D mesh shape:", mesh3d.shape)             # (35, 20, 3)
print("Initial 3D mesh shape:", mesh3dinit.shape)               # (35, 20, 3)
print("Mesh deformation vector:", mesh3dflow.shape)             # (35, 20, 3)
print("Sensor timestamp:", timestamp)                           # s
# Release resources
sensor.release()

"""
output
Found Xense devices: {'OG000708': 6, 'OG000703': 10}
Read config from OG000703: cam_id_10 success!
In SDK: [Network] Camera 10 connected
Init infer engine
infer session using GPU
Rectified image shape: (700, 400, 3)
Difference image shape: (700, 400, 3)
Depth image shape: (700, 400)
3D force distribution shape: (35, 20, 3)
Normal force component: (35, 20, 3)
6-dimensional resultant force: (6,)
Tangential displacement shape: (26, 14, 2)
Current frame 3D mesh shape: (35, 20, 3)
Initial 3D mesh shape: (35, 20, 3)
Mesh deformation vector: (35, 20, 3)
Sensor timestamp: 1770810092.601942
In SDK: [Network] Camera 10 disconnected
"""
