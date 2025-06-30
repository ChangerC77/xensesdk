import sys
from xensesdk.omni.widgets import ExampleView
from xensesdk.xenseInterface.XenseSensor import Sensor

def main(sensor_0):
    
    rectify, difference, depth, force, forcenormal, forceresultant, mesh3d, mesh3dinit, mesh3dflow = sensor_0.selectSensorInfo(
        Sensor.OutputType.Rectify, # [np.ndarray] # 校正图像, shape=(700, 400, 3), RGB
        Sensor.OutputType.Difference, # [np.ndarray] # 差分图像, shape=(700, 400, 3), RGB
        Sensor.OutputType.Depth, # [np.ndarray] # 深度图像, shape=(700, 400), 单位mm
        Sensor.OutputType.Force, # [np.ndarray] # 三维力分布, shape=(35, 20, 3)
        Sensor.OutputType.ForceNorm, # [np.ndarray] # 法向力分量, shape=(35, 20, 3)
        Sensor.OutputType.ForceResultant, # [np.ndarray] # 六维合力, shape=(6,)
        Sensor.OutputType.Mesh3D, # [np.ndarray] # 当前帧3D网格, shape=(35, 20, 3)
        Sensor.OutputType.Mesh3DInit, # [np.ndarray] # 初始3D网格, shape=(35, 20, 3)
        Sensor.OutputType.Mesh3DFlow, # [np.ndarray] # 网格形变向量, shape=(35, 20, 3)
    )
    print("rectify", rectify)
    print("difference", difference)
    print("depth", depth)
    print("force", force)
    print("forcenormal", forcenormal)
    print("forceresultant", forceresultant)
    print("rectify", rectify)
    print("mesh3d", mesh3d)
    print("mesh3dinit", mesh3dinit)
    print("mesh3dflow", mesh3dflow)

    sensor_0.release()
    sys.exit()

if __name__ == '__main__':
    sensor_0 = Sensor.create(0, config_path="config/OG000027")
    main(sensor_0)