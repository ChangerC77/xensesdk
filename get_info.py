import sys
from xensesdk.omni.widgets import ExampleView
from xensesdk.xenseInterface.XenseSensor import Sensor

def main(sensor_0):
    
    force, res_force, mesh_init, src, diff, depth = sensor_0.selectSensorInfo(
        Sensor.OutputType.Force, 
        Sensor.OutputType.ForceResultant,
        Sensor.OutputType.Mesh3DInit,
        Sensor.OutputType.Rectify, 
        Sensor.OutputType.Difference, 
        Sensor.OutputType.Depth,
    )
    print("force", force) # (35, 20, 3)
    print("res_force", res_force) # (6,)
    print("mesh_init", mesh_init) # (35, 20, 3)
    print("src", src) # (700, 400, 3)
    print("diff", diff) # (700, 400, 3)
    print("depth", depth) # (700, 400)
    # print("force", force.shape)
    # print("res_force", res_force.shape)
    # print("mesh_init", mesh_init.shape)
    # print("src", src.shape)
    # print("diff", diff.shape)
    # print("depth", depth.shape)

    sensor_0.release()
    sys.exit()

if __name__ == '__main__':
    sensor_0 = Sensor.create(0, config_path="config/OG000027")
    main(sensor_0)