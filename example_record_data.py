from xensesdk.xenseInterface.XenseSensor import Sensor
import time 

if __name__ == '__main__':
    sensor  = Sensor.create(0, config_path="config/OG000046")

    sensor.startSaveSensorInfo(r"data", [Sensor.OutputType.Difference, Sensor.OutputType.Rectify])
    time.sleep(5)
    sensor.stopSaveSensorInfo()
    print("save ok")
    
    sensor.release()
