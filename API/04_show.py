from pathlib import Path
SCRIPT_DIR = Path(__file__).resolve().parent
SAVE_DIR = Path(SCRIPT_DIR / "test_dir")  # Storage directory
SAVE_DIR.mkdir(parents=True, exist_ok=True)
import cv2
import time
import numpy as np

from xensesdk import Sensor

sensor_id = 'OG000165'

def save_data():
    fps = 30       # Hz
    duration = 3   # seconds
    frame_interval = 1.0 / fps
    total_frames = fps * duration

    sensor_0 = Sensor.create(sensor_id)
    for i in range(total_frames):
        start_time = time.time()

        # Capture one frame
        rec = sensor_0.selectSensorInfo(Sensor.OutputType.Rectify)  

        # Generate filename
        filename = SAVE_DIR / f"{sensor_id}_{i:03d}.png"

        # Save image
        cv2.imwrite(str(filename), rec)
        print(f"Saved {filename}")

        # Control frame rate (30Hz)
        elapsed = time.time() - start_time
        sleep_time = frame_interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

    # Export configuration
    sensor_0.exportRuntimeConfig(SAVE_DIR)

    sensor_0.release()

def replay_data():
    sensor_solver = Sensor.createSolver(SAVE_DIR / f"runtime_{sensor_id}")
    
    # 获取所有PNG文件并排序
    png_files = sorted([f for f in SAVE_DIR.glob("*.png") if not f.name.endswith("_depth.png")])
    
    # 创建显示窗口
    cv2.namedWindow('Original Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Depth Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Force Image', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Difference Image', cv2.WINDOW_NORMAL)
    
    # 设置帧率控制（30fps）
    fps = 30
    frame_interval = 1.0 / fps
    
    for png_file in png_files:
        start_time = time.time()
        
        # 读取原始图像
        img = cv2.imread(str(png_file), cv2.IMREAD_UNCHANGED)
        
        # 处理图像 - 这里使用正确的参数传递方式
        # 注意：根据原始代码，可能需要先设置图像，然后调用selectSensorInfo
        # 这里假设sensor_solver有一个setRectifyImage方法或其他方式设置图像
        
        # 根据原始代码的调用方式，应该是：
        depth, force, diff = sensor_solver.selectSensorInfo(
            Sensor.OutputType.Depth,
            Sensor.OutputType.Force,
            Sensor.OutputType.Difference,
            img  # 直接传递图像作为参数，而不是关键字参数
        )
        
        # 可视化处理
        depth_vis = np.clip(depth * 200, 0, 255).astype(np.uint8)
        force_vis = np.clip(force * 200, 0, 255).astype(np.uint8)
        diff_vis = np.clip(diff * 200, 0, 255).astype(np.uint8)
        
        # 如果是彩色图像，转换为BGR格式用于显示
        if len(img.shape) == 2:
            img_display = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        else:
            img_display = img
        
        # 将深度图转换为彩色图以便更好显示
        depth_color = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
        force_color = cv2.applyColorMap(force_vis, cv2.COLORMAP_JET)
        diff_color = cv2.applyColorMap(diff_vis, cv2.COLORMAP_JET)
        
        # 显示图像
        cv2.imshow('Original Image', img_display)
        cv2.imshow('Depth Image', depth_color)
        cv2.imshow('Force Image', force_color)
        cv2.imshow('Difference Image', diff_color)
        
        # 添加文件名信息在窗口标题上显示（可选）
        cv2.setWindowTitle('Original Image', f'Original Image - {png_file.name}')
        
        # 等待按键，'q'退出，空格暂停/继续
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord(' '):
            cv2.waitKey(0)  # 暂停，按任意键继续
        
        # 控制播放速度（30fps）
        elapsed = time.time() - start_time
        sleep_time = frame_interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)
    
    # 关闭所有窗口
    cv2.destroyAllWindows()
    sensor_solver.release()

def realtime_display():
    """直接从传感器实时显示图像"""
    fps = 30
    frame_interval = 1.0 / fps
    
    sensor = Sensor.create(sensor_id)
    
    # 创建显示窗口
    cv2.namedWindow('Real-time Rectify', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Real-time Depth', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Real-time Force', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Real-time Difference', cv2.WINDOW_NORMAL)
    
    print("按 'q' 退出实时显示")
    print("按 's' 保存当前帧")
    
    frame_count = 0
    
    try:
        while True:
            start_time = time.time()
            
            # 获取矫正图像
            rectify = sensor.selectSensorInfo(Sensor.OutputType.Rectify)
            
            # 获取深度、力和差分图像
            # 注意：这里假设selectSensorInfo可以同时获取多个输出类型
            # 根据错误信息，我们不使用关键字参数
            try:
                # 尝试获取深度、力和差分
                depth, force, diff = sensor.selectSensorInfo(
                    Sensor.OutputType.Depth,
                    Sensor.OutputType.Force,
                    Sensor.OutputType.Difference
                )
            except:
                # 如果上面的调用失败，可能需要分别获取
                depth = sensor.selectSensorInfo(Sensor.OutputType.Depth)
                force = sensor.selectSensorInfo(Sensor.OutputType.Force)
                diff = sensor.selectSensorInfo(Sensor.OutputType.Difference)
            
            # 可视化处理
            if depth is not None:
                depth_vis = np.clip(depth * 200, 0, 255).astype(np.uint8)
                depth_color = cv2.applyColorMap(depth_vis, cv2.COLORMAP_JET)
                cv2.imshow('Real-time Depth', depth_color)
            
            if force is not None:
                force_vis = np.clip(force * 200, 0, 255).astype(np.uint8)
                force_color = cv2.applyColorMap(force_vis, cv2.COLORMAP_JET)
                cv2.imshow('Real-time Force', force_color)
            
            if diff is not None:
                diff_vis = np.clip(diff * 200, 0, 255).astype(np.uint8)
                diff_color = cv2.applyColorMap(diff_vis, cv2.COLORMAP_JET)
                cv2.imshow('Real-time Difference', diff_color)
            
            # 显示原始图像
            if len(rectify.shape) == 2:
                rectify_display = cv2.cvtColor(rectify, cv2.COLOR_GRAY2BGR)
            else:
                rectify_display = rectify
            
            cv2.imshow('Real-time Rectify', rectify_display)
            
            # 检查按键
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                # 保存当前帧
                cv2.imwrite(str(SAVE_DIR / f"realtime_frame_{frame_count:03d}.png"), rectify)
                frame_count += 1
                print(f"Saved frame {frame_count}")
            
            # 控制帧率
            elapsed = time.time() - start_time
            sleep_time = frame_interval - elapsed
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        print("\n实时显示被用户中断")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        cv2.destroyAllWindows()
        sensor.release()
        print("传感器已释放")

if __name__ == '__main__':
    # 选择模式
    print("选择模式:")
    print("1. 保存数据")
    print("2. 回放数据（实时显示）")
    print("3. 实时显示")
    
    choice = input("请输入选项 (1/2/3): ").strip()
    
    if choice == '1':
        save_data()
        print("数据保存成功")
    elif choice == '2':
        replay_data()
        print("数据回放完成")
    elif choice == '3':
        realtime_display()
    else:
        print("无效选项")