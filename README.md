# Xense SDK 文档

SDK开发文档和软件操作手册更新至： https://xensedoc.readthedocs.io/en/latest/

studio: https://www.xenserobotics.com/about/372

<!-- OUTLINE START -->
## Outline

- [1. download](#download)
- [2. hardware](#hardware)
- [3. urdf](#urdf)
- [4. conda](#conda)
- [5. 根据对应显卡安装显卡驱动](#gpu-driver)
- [6. cuda & cudnn](#cuda-cudnn)
  - [6.1 通过 Conda 直接安装](#cuda-cudnn-conda)
  - [6.2 从本地 Conda 环境包安装](#cuda-cudnn-local)
- [7. install Xense SDK Package](#install-sdk)
- [8. force](#force)
- [9. config](#config)
- [10. API 文档](#api-docs)
  - [10.1 single create_method](#api-docs-single-create)
  - [10.2 single selectSensorInfo_method](#api-docs-single-select)
  - [10.3 single createSolver](#api-docs-single-solver)
  - [10.4 single real-time show image](#api-docs-single-show)
  - [10.5 double sensors test](#api-docs-double)
- [11. Example](#examples)
  - [11.1 example_force.py](#example-force)
  - [11.2 example_marker_detect.py](#example-marker-detect)
  - [11.3 example_finger_depth.py](#example-finger-depth)
  - [11.4 example_depth.py](#example-depth)
- [12. API instruction](#api-instruction)
  - [12.1 create 方法](#api-create)
  - [12.2 selectSensorInfo 方法](#api-selectsensorinfo)
  - [12.3 startSaveSensorInfo 方法](#api-startsavesensorinfo)
  - [12.4 stopSaveSensorInfo 方法](#api-stopsavesensorinfo)
  - [12.5 getCameraID 方法](#api-getcameraid)
  - [12.6 resetReferenceImage 方法](#api-resetreferenceimage)
  - [12.7 release 方法](#api-release)
- [FAQ](#faq)
<!-- OUTLINE END -->

<a id="download"></a>
## 1. download
```
cd ~
git clone -b v1.4.7 https://github.com/ChangerC77/xensesdk.git
```
<a id="hardware"></a>
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

<a id="urdf"></a>
## 3. urdf
you can see `STL` and `stp` file in `models` directory

<a id="conda"></a>
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
<a id="gpu-driver"></a>
## 5. 根据对应显卡安装显卡驱动
---
<a id="cuda-cudnn"></a>
## 6. cuda & cudnn
SDK 支持 `CUDA Toolkit 11.8` 和 `cuDNN 8.9.2.26`。根据您的环境，选择以下安装方式：

<a id="cuda-cudnn-conda"></a>
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

<a id="cuda-cudnn-local"></a>
### 6.2 从本地 Conda 环境包安装
```
conda install --use-local cudatoolkit-11.8.0-hd77b12b_0.conda
conda install --use-local cudnn-8.9.2.26-cuda11_0.conda
```

<a id="install-sdk"></a>
## 7. install Xense SDK Package
```bash
pip install xensesdk-1.4.7-cp39-cp39-manylinux2014_x86_64.manylinux_2_17_x86_64.whl
```

---
<a id="force"></a>
## 8. force 

<img src='img/1.png'>

<a id="config"></a>
## 9. config

使用前请先获得对应传感器配置文件，文件和传感器型号一一对应。

根据具体传感器参数来修改`config/config.yaml`文件

```yaml
xense:
  sensor1_id: 'OG000204' # left / 单传感器脚本默认读取该 ID
  sensor2_id: 'OG000165' # right / 双传感器脚本读取该 ID
  freq: 60

examples:
  data_processing_video_path: ''
  finger_config_path: ''
  record_data_dir: 'Examples/output'
  record_data_duration_seconds: 5
  remote_ip: '192.168.1.120'

```

说明：

- `API/single` 下的 `01_create_method.py`、`02_selectSensorInfo_Method.py`、`03_createSolver.py`、`04_show.py` 默认读取 `xense.sensor1_id`。
- `API/double/05_show.py` 默认读取 `xense.sensor1_id` 作为左侧传感器，读取 `xense.sensor2_id` 作为右侧传感器。
- `Examples` 目录下示例脚本也默认读取 `config/config.yaml`，并支持通过 `--config` 指定其他 YAML 配置文件。
- `xense.freq` 用于控制 `03_createSolver.py` 的保存频率，以及 `04_show.py` 的实时显示频率。
- 所有上述脚本均支持 `--config` 参数，默认配置路径为仓库根目录下的 `config/config.yaml`。
- `config/config_loader.py` 已移除，脚本现在直接读取 YAML 配置文件。

<a id="api-docs"></a>
## 10. API 文档
本目录已按单传感器和双传感器拆分：

- `API/single`：单传感器相关示例
- `API/double`：双传感器相关示例（当前为双传感器图像拼接显示脚本）

默认情况下，这些脚本都会读取 `config/config.yaml`。如果你需要使用其他配置文件，可以在命令后追加 `--config /path/to/config.yaml`。

<a id="api-docs-single-create"></a>
### 10.1 single create_method
```bash
python ~/xensesdk/API/single/01_create_method.py
# or
python ~/xensesdk/API/single/01_create_method.py --config config/config.yaml
```

说明：

- 脚本会读取 `xense.sensor1_id` 并创建一个 `Sensor` 实例。
- 示例运行完成后会自动调用 `release()` 释放资源。

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

<a id="api-docs-single-select"></a>
### 10.2 single selectSensorInfo_method
```bash
python ~/xensesdk/API/single/02_selectSensorInfo_Method.py
# or
python ~/xensesdk/API/single/02_selectSensorInfo_Method.py --config config/config.yaml
```

说明：

- 脚本会读取 `xense.sensor1_id`，并一次性输出多种传感器数据的 shape。

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

<a id="api-docs-single-solver"></a>
### 10.3 single createSolver
```bash
python ~/xensesdk/API/single/03_createSolver.py
# or
python ~/xensesdk/API/single/03_createSolver.py --config config/config.yaml
```

说明：

- 图像和运行时配置会保存到 `API/single/test_dir`，脚本会自动创建该目录。
- 保存使用的传感器 ID 读取自 `xense.sensor1_id`。
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

<a id="api-docs-single-show"></a>
### 10.4 single real-time show image
```bash
python ~/xensesdk/API/single/04_show.py
# or
python ~/xensesdk/API/single/04_show.py --config config/config.yaml
```

说明：

- 实时显示使用的传感器 ID 读取自 `xense.sensor1_id`。
- 运行频率读取 `config/config.yaml` 中的 `xense.freq`。
- 启动后会先将运行时配置导出到 `API/single/test_dir/runtime_<sensor_id>`，再创建 solver 实时计算深度图。

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

<a id="api-docs-double"></a>
### 10.5 double sensors test
```bash
python ~/xensesdk/API/double/05_show.py
# or
python ~/xensesdk/API/double/05_show.py --config config/config.yaml
```

<details>
<summary>output</summary>

```text
Found Xense devices: {'OG000708': 16, 'OG000869': 14}
Read config from OG000869: cam_id_14 success!
In SDK: [Network] Camera 14 connected
Init infer engine
infer session using GPU
Found Xense devices: {'OG000708': 16, 'OG000869': 14}
Read config from OG000708: cam_id_16 success!
In SDK: [Network] Camera 16 connected
Init infer engine
infer session using GPU
```

</details>
<img src='img/14.png'>

说明：

- 左侧传感器读取 `xense.sensor1_id`，右侧传感器读取 `xense.sensor2_id`。
- 脚本会读取两个传感器的 `Rectify` 图像并进行横向拼接显示。
- 默认窗口标题为 `Double Sensors Rectified Images`。
- 在图像窗口按 `q` 退出程序，脚本会自动释放两个传感器连接。

---
<a id="examples"></a>
## 11. Example
<a id="example-force"></a>
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

<a id="example-marker-detect"></a>
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

<a id="example-finger-depth"></a>
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

<a id="example-depth"></a>
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

<a id="api-instruction"></a>
## 12. API instruction
<a id="api-create"></a>
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

<a id="api-selectsensorinfo"></a>
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

<a id="api-startsavesensorinfo"></a>
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

<a id="api-stopsavesensorinfo"></a>
### 12.4 `stopSaveSensorInfo` 方法

##### 描述

停止数据保存。

---

<a id="api-getcameraid"></a>
### 12.5 `getCameraID` 方法

##### 描述

获取当前传感器的相机编号。

---

<a id="api-resetreferenceimage"></a>
### 12.6 `resetReferenceImage` 方法

##### 描述

重置数据处理流程。

---

<a id="api-release"></a>
### 12.7 `release` 方法

##### 描述

释放资源，关闭传感器。

---

<a id="faq"></a>
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
