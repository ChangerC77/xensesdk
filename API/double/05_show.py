import cv2
import numpy as np
import argparse
import yaml
from xensesdk import Sensor

def main(config):
    sensor_left = Sensor.create(config['xense']['sensor1_id'])
    sensor_right = Sensor.create(config['xense']['sensor2_id'])
    # print(f"sensor_left: {sensor_left}")
    # print(f"sensor_right: {sensor_right}")

    while True:
        rectify_left = sensor_left.selectSensorInfo(Sensor.OutputType.Rectify)
        rectify_right = sensor_right.selectSensorInfo(Sensor.OutputType.Rectify)

        combined_image = np.hstack((rectify_left, rectify_right))

        cv2.imshow('Double Sensors Rectified Images', combined_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            sensor_left.release()
            sensor_right.release()
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, default='config/config.yaml', help='YAML file path')
    args = parser.parse_args()
    with open(args.config, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
       
    main(config)
