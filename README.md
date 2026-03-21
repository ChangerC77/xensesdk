# Xense SDK 文档

SDK开发文档和软件操作手册更新至： https://xensedoc.readthedocs.io/en/latest/

studio: https://www.xenserobotics.com/about/372
## 1. download
```
cd ~
git clone -b v1.4.7 https://github.com/ChangerC77/xensesdk.git
```
## 2. hardware

<table>
  <tr>
    <td><img src='img/2.png' width="100%"></td>
    <td><img src='img/3.png' width="100%"></td>
  </tr>
  <tr>
    <td><img src='img/4.png' width="100%"></td>
    <td><img src='img/5.png' width="100%"></td>
  </tr>
  <tr>
    <td><img src='img/6.png' width="100%"></td>
    <td><img src='img/7.png' width="100%"></td>
  </tr>
</table>

## 3. urdf
you can see `STL` and `stp` file in `models` directory

## 4. conda

进入 Xense SDK 目录

```bash
# 进入 Xense SDK 目录
cd xensesdk

# 创建并激活虚拟环境
conda create -n xenseenv python=3.9.19
conda activate xenseenv
```
---
## 5. 根据对应显卡安装显卡驱动
---
## 6. cuda & cudnn
SDK 支持 `CUDA Toolkit 11.8` 和 `cuDNN 8.9.2.26`。根据您的环境，选择以下安装方式：

### 6.1. 通过 Conda 直接安装 (recommand)
#### 6.1.1 搜索所需版本：
```
conda search cudnn
conda search cudatoolkit
```
#### 6.1.2 安装所需版本：
```
conda install cudnn==8.9.2.26 cudatoolkit==11.8.0
```
耗时比较长
<details>
<summary>output</summary>

```
Channels:
 - defaults
Platform: linux-64
Collecting package metadata (repodata.json): done
Solving environment: done


==> WARNING: A newer version of conda exists. <==
    current version: 25.3.1
    latest version: 25.5.0

Please update conda by running

    $ conda update -n base -c defaults conda



## Package Plan ##

  environment location: /home/tars/system/miniconda3/envs/xenseenv

  added / updated specs:
    - cudatoolkit==11.8.0
    - cudnn==8.9.2.26


The following packages will be downloaded:

    package                    |            build
    ---------------------------|-----------------
    cudatoolkit-11.8.0         |       h6a678d5_0       630.7 MB
    cudnn-8.9.2.26             |         cuda11_0       469.4 MB
    ------------------------------------------------------------
                                           Total:        1.07 GB

The following NEW packages will be INSTALLED:

  cudatoolkit        pkgs/main/linux-64::cudatoolkit-11.8.0-h6a678d5_0 
  cudnn              pkgs/main/linux-64::cudnn-8.9.2.26-cuda11_0 


Proceed ([y]/n)? y


Downloading and Extracting Packages:
                                                                                                     
Preparing transaction: done                                                                          
Verifying transaction: done
Executing transaction: \ By downloading and using the CUDA Toolkit conda packages, you accept the terms and conditions of the CUDA End User License Agreement (EULA): https://docs.nvidia.com/cuda/eula/index.html

done
```

</details>

### 6.2 从本地 Conda 环境包安装
```
conda install --use-local cudatoolkit-11.8.0-hd77b12b_0.conda
conda install --use-local cudnn-8.9.2.26-cuda11_0.conda
```

## 7. install Xense SDK Package
```bash
pip install xensesdk-1.4.7-cp39-cp39-manylinux2014_x86_64.manylinux_2_17_x86_64.whl
```

---
## 8. force 

<img src='img/1.png'>

## 9. config

使用前请先获得对应传感器配置文件，文件和传感器型号一一对应。

根据具体传感器参数来修改`config/config.yaml`文件

```
xense:
  sensor1_id: 'OG000165'
  sensor2_id: 'OG000204'
  freq: 60

examples:
  data_processing_video_path: ''
  finger_config_path: ''
  record_data_dir: 'Examples/output'
  record_data_duration_seconds: 5
  remote_ip: '192.168.1.120'

```

说明：

- 单传感器脚本兼容读取 `xense.sensor_id`，未配置时会回退到 `xense.sensor1_id`。
- 双传感器脚本默认读取 `xense.sensor1_id` 和 `xense.sensor2_id`，也兼容 `xense.sensor_ids` 列表写法。
- `xense.freq` 用于控制实时读取、实时显示和保存数据时的循环频率。

## 10. API 文档
本目录已按单传感器和双传感器拆分：

- `API/single`：单传感器相关示例
- `API/double`：双传感器相关示例

这些脚本默认从 `config/config.yaml` 读取传感器 ID；实时读取、实时显示和保存数据的频率由 `xense.freq` 控制。双传感器脚本也支持通过命令行直接传入两个传感器 ID。

### 10.1 single create_method
```bash
python ~/xensesdk/API/single/01_create_method.py
```

<details>
<summary>output</summary>

```text
Found Xense devices: {'OG000165': 2}
Read config from OG000165: cam_id_2 success!
In SDK: [Network] Camera 2 connected
Init infer engine
infer session using GPU
In SDK: [Network] Camera 2 disconnected
```

</details>

### 10.2 single selectSensorInfo_method
```bash
python ~/xensesdk/API/single/02_selectSensorInfo_Method.py
```

<details>
<summary>output</summary>

```text
Found Xense devices: {'OG000165': 2}
Read config from OG000165: cam_id_2 success!
In SDK: [Network] Camera 2 connected
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
Sensor timestamp: 1773420554.5228953
In SDK: [Network] Camera 2 disconnected
```

</details>

### 10.3 single createSolver
```bash
python ~/xensesdk/API/single/03_createSolver.py
```

说明：

- 图像会保存到 `API/single/test_dir`。
- 保存频率读取 `config/config.yaml` 中的 `xense.freq`。

<details>
<summary>output</summary>

```text
Found Xense devices: {'OG000165': 2}
Read config from OG000165: cam_id_2 success!
In SDK: [Network] Camera 2 connected
Init infer engine
infer session using GPU
Saved /home/leishen/xensesdk/API/single/test_dir/OG000165_000.png
...
模型已并保存到: /home/leishen/xensesdk/API/single/test_dir/runtime_OG000165
In SDK: [Network] Camera 2 disconnected
Init infer engine
infer session using GPU
Data saved and replayed successfully.
```

</details>

### 10.4 single real-time show image
```bash
python ~/xensesdk/API/single/04_show.py
```

说明：

- 运行频率读取 `config/config.yaml` 中的 `xense.freq`。
- 运行时配置保存在 `API/single/test_dir`。

<details>
<summary>output</summary>

```text
Found Xense devices: {'OG000165': 1}
Read config from OG000165: cam_id_1 success!
In SDK: [Network] Camera 1 connected
Init infer engine
infer session using GPU
模型已并保存到: /home/leishen/cxy/xensesdk/API/single/test_dir/runtime_OG000165
Init infer engine
infer session using GPU
在终端按 Ctrl+C 退出实时显示
```

</details>

| Rectify | Depth |
| --- | --- |
| <img src='img/8.png' width="100%"> | <img src='img/9.png' width="100%"> |

### 10.5 double sensors
```bash
python ~/xensesdk/API/double/05_double_sensors.py
```

也可以直接传入两个传感器 ID：

```bash
python ~/xensesdk/API/double/05_double_sensors.py OG000165 OG000204
```

<details>
<summary>output</summary>

```text
===== Sensor OG000165 =====
[OG000165] Rectified image shape: (700, 400, 3)
[OG000165] Difference image shape: (700, 400, 3)
[OG000165] Depth image shape: (700, 400)
...

===== Sensor OG000204 =====
[OG000204] Rectified image shape: (700, 400, 3)
[OG000204] Difference image shape: (700, 400, 3)
[OG000204] Depth image shape: (700, 400)
...
```

</details>

### 10.6 double sensors real-time
```bash
python ~/xensesdk/API/double/05_double_sensors_real_time.py
```

也可以直接传入两个传感器 ID，并用 `--fps` 临时覆盖 `config/config.yaml` 里的 `xense.freq`：

```bash
python ~/xensesdk/API/double/05_double_sensors_real_time.py OG000165 OG000204 --fps 30
```

<details>
<summary>output</summary>

```text
First frame data shapes:

===== Sensor OG000165 =====
[OG000165] Rectified image shape: (700, 400, 3)
...

===== Sensor OG000204 =====
[OG000204] Rectified image shape: (700, 400, 3)
...

Frame 2 | loop_time=0.0123s | loop_fps=58.41 Hz
[OG000165] timestamp=1770810092.601942, sensor_fps=59.87 Hz, depth_shape=(700, 400), force_resultant=[...]
[OG000204] timestamp=1770810092.602115, sensor_fps=60.02 Hz, depth_shape=(700, 400), force_resultant=[...]
```

</details>

---
## 11. Example
### 11.1 example_force.py
```
python ~/xensesdk/Examples/example_force.py
```
<details>
<summary>output</summary>

```
Found Xense devices: {'OG000165': 0}
new flash read fail, fallback.
new flash read fail, fallback.
new flash read fail, fallback.
new flash read fail, fallback.
Read config from OG000165: cam_id_0 success!
In SDK: [Network] Camera 0 connected
Init infer engine
infer session using GPU
```

</details>
<img src='img/11.png'>

### 11.2 example_marker_detect.py
```
python ~/xensesdk/Examples/example_marker_detect.py
```
<details>
<summary>output</summary>

```
Found Xense devices: {'OG000165': 0}
new flash read fail, fallback.
new flash read fail, fallback.
new flash read fail, fallback.
new flash read fail, fallback.
Read config from OG000165: cam_id_0 success!
In SDK: [Network] Camera 0 connected
Init infer engine
infer session using GPU
```

</details>
<img src='img/12.png'>

### 11.3 example_finger_depth.py
```
python ~/xensesdk/Examples/example_finger_depth.py
```
<details>
<summary>output</summary>

```
Found Xense devices: {'OG000165': 0}
new flash read fail, fallback.
new flash read fail, fallback.
new flash read fail, fallback.
new flash read fail, fallback.
Read config from OG000165: cam_id_0 success!
In SDK: [Network] Camera 0 connected
Init infer engine
infer session using GPU
```

</details>

<img src='img/10.png'>

### 11.4 example_depth.py
```
python ~/xensesdk/Examples/example_depth.py
```
<img src='img/13.png'>

<details>
<summary>output</summary>

```
Found Xense devices: {'OG000165': 0}
new flash read fail, fallback.
new flash read fail, fallback.
new flash read fail, fallback.
new flash read fail, fallback.
Read config from OG000165: cam_id_0 success!
In SDK: [Network] Camera 0 connected
Init infer engine
infer session using GPU
```

</details>

## 12. API instruction
### 12.1 `create` 方法

##### 描述

创建一个传感器实例，在结束时请调用`release`。

##### 输入参数

* **cam\_id** (`int | str`, 可选): 传感器 ID、序列号或视频路径。默认为 0。
* **use\_gpu** (`bool`, 可选): 是否使用 GPU 推理，默认为 True。
* **config\_path** (`str | Path`, 可选): 配置文件路径或目录。如果是目录，需包含与传感器序列号同名的标定文件。
* **api** (`Enum`, 可选): 相机 API 类型（如 OpenCV 后端），用于指定相机访问方式。
* **check\_serial** (`bool`, 可选): 是否检查传感器序列号，默认 True。
* **rectify\_size** (`tuple[int, int]`, 可选): 校正图像尺寸。
* **ip\_address** (`str`, 可选): 远程连接使用的相机 IP。
* **video\_path** (`str`, 可选): 离线模拟的视频路径。

##### 返回

* `Sensor` 对象

##### 示例

```python

# Example 1：  用SN码开启
from xensesdk import Sensor
sensor = Sensor.create('OP000064') 

# Example 2：  用相机编号开启
sensor = Sensor.create(0) 

# Example 3： 打开储存的数据
sensor = Sensor.create(None, video_path=r"data.h5")

# Example 4： 打开算力板上的传感器
sensor =  Sensor.create('OP000064', ip_address="192.168.66.66")
```

---

### 12.2 `selectSensorInfo` 方法

##### 描述

获取指定类型的传感器数据。

##### 输入参数

* **args**: 任意数量的 `Sensor.OutputType` 枚举，用于指定需要获取的数据类型：

    * Rectify: Optional[np.ndarray]          # 校正图像, shape=(700, 400, 3), RGB
    * Difference: Optional[np.ndarray]       # 差分图像, shape=(700, 400, 3), RGB
    * Depth: Optional[np.ndarray]            # 深度图像, shape=(700, 400), 单位mm

    * Marker2D: Optional[np.ndarray]         # 切向位移, shape=(35, 20, 2)
    * Force: Optional[np.ndarray]            # 三维力分布, shape=(35, 20, 3)
    * ForceNorm: Optional[np.ndarray]        # 法向力分量, shape=(35, 20, 3)
    * ForceResultant: Optional[np.ndarray]   # 六维合力, shape=(6,)

    * Mesh3D: Optional[np.ndarray]           # 当前帧3D网格, shape=(35, 20, 3)
    * Mesh3DInit: Optional[np.ndarray]       # 初始3D网格, shape=(35, 20, 3)
    * Mesh3DFlow: Optional[np.ndarray]       # 网格形变向量, shape=(35, 20, 3)

##### 返回

* 所请求的传感器数据（返回数量和顺序与参数一致）

##### 示例

```python
from xensesdk import Sensor
sensor = Sensor.create('OP000064') 
rectify, marker3d, marker3dInit, marker3dFlow, depth = sensor.selectSensorInfo(
    Sensor.OutputType.Rectify, 
    Sensor.OutputType.Marker3D, 
    Sensor.OutputType.Marker3DInit,
    Sensor.OutputType.Marker3DFlow,
    Sensor.OutputType.Depth
)
...
sensor.release()
```

---

### 12.3 `startSaveSensorInfo` 方法

##### 描述

开始保存指定类型的传感器数据，在结束时务必搭配`stopSaveSensorInfo`使用。

##### 输入参数

* **path** (`str`): 数据保存的文件夹路径。
* **data\_to\_save** (`List[Sensor.OutputType]`, 可选): 需要保存的数据类型列表。为 `None` 则保存所有类型。

##### 返回

* 无

##### 示例

```python
from xensesdk import Sensor
sensor = Sensor.create('OP000064') 
data_to_save = [
    Sensor.OutputType.Rectify, 
    Sensor.OutputType.Difference,
    Sensor.OutputType.Depth,
    Sensor.OutputType.Marker2D
]
sensor.startSaveSensorInfo('/path/to/save', data_to_save)
...
sensor.stopSaveSensorInfo()
...
sensor.release()
```

---

### 12.4 `stopSaveSensorInfo` 方法

##### 描述

停止数据保存。

---

### 12.5 `getCameraID` 方法

##### 描述

获取当前传感器的相机编号。

---

### 12.6 `resetReferenceImage` 方法

##### 描述

重置数据处理流程。

---

### 12.7 `release` 方法

##### 描述

释放资源，关闭传感器。

---

## 常见问题解答 (FAQ)

**问：** 无法加载 Qt 平台插件 "xcb" 虽然它已被找到，错误信息为 "..."

**答：** 进入 `.../site-packages/.../Qt/plugins/platform` 目录并删除 `libqxcb.so` 文件。

**问：** from 6.5.0, xcb-cursor0 or libxcb-cursor0 is needed to load the Qt xcb platform plugin.
Could not load the Qt platform plugin "xcb" in "" even though it was found. This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

**答：** 终端内执行：

```shelll
sudo apt-get update
sudo apt-get install libxcb-cursor0
```

