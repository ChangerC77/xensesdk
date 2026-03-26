import cv2
import numpy as np

from xensesdk import Sensor

def main():
    sensor_left = Sensor.create('OG000869')
    sensor_right = Sensor.create('OG000708')

    while True:
        rectify_left = sensor_left.selectSensorInfo(Sensor.OutputType.Rectify)
        rectify_right = sensor_right.selectSensorInfo(Sensor.OutputType.Rectify)

        combined_image = np.hstack((rectify_left, rectify_right))

        cv2.imshow('Combined Rectified Images', combined_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            sensor_left.release()
            sensor_right.release()
            break

if __name__ == "__main__":
    main()
