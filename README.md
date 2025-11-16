# HeyTeaAutoDraw

一个用于在绘画应用程序中自动绘制图像的工具，支持一键式图像转手绘功能。

## 功能特性

- **图像预处理**：自动将图片转换为黑白轮廓
- **窗口检测**：智能识别目标绘画窗口
- **一键绘制**：自动在绘画应用中绘制图像
- **画笔控制**：根据线条宽度自动调整画笔大小
- **键盘控制**：支持暂停/继续（空格键）和退出（ESC键）
- **坐标捕获**：自动记录画布坐标位置

## 技术栈

- Python 3.x
- PyQt5（GUI界面）
- OpenCV（图像处理）
- pyautogui（自动操作）
- keyboard（键盘监听）
- numpy（数值计算）

## 项目结构

```
├── main.py              # 主程序入口，GUI界面
├── draw_image.py        # 绘制核心逻辑
├── window_detection.py  # 窗口检测和坐标处理
├── src/                 # 核心模块目录
│   ├── config.py        # 配置管理
│   ├── keyboard_handler.py  # 键盘事件处理
│   ├── path_processor.py    # 路径处理
│   ├── brush_handler.py     # 画笔大小控制
│   ├── image_processor.py   # 图像处理
│   └── coordinate_loader.py # 坐标加载
├── output/              # 输出目录
│   └── coordinates/     # 坐标文件存储
└── README.md            # 项目文档
```

## 安装说明

1. 确保已安装 Python 3.6 或更高版本
2. 安装依赖包：

```bash
pip install pyqt5 opencv-python pyautogui keyboard numpy
```

## 使用方法

1. 启动程序：

```bash
python main.py
```

2. 使用步骤：
   - 点击"选择图片"按钮，选择要绘制的图像
   - 确保目标绘画应用程序已打开
   - 点击"开始绘制"按钮
   - 程序将自动检测窗口并开始绘制
   - 使用空格键暂停/继续绘制，ESC键退出

## 配置说明

程序会在首次运行时自动创建配置目录和文件：

- `output/coordinates/`：存储捕获的坐标文件
- `output/config/`：存储配置信息

## 注意事项

1. 确保目标绘画应用程序窗口可见且未被遮挡
2. 绘制过程中不要移动或调整绘画窗口大小
3. 程序需要一定的系统权限才能进行自动操作
4. 建议使用分辨率适中的图像（建议不超过1000x1000像素）

## 开发说明

### 核心模块说明

1. **ConfigManager**：管理配置路径和文件
2. **KeyboardHandler**：处理键盘事件监听
3. **PathProcessor**：处理图像路径和轮廓
4. **BrushHandler**：控制画笔大小切换
5. **ImageProcessor**：图像预处理和轮廓提取
6. **CoordinateLoader**：加载和保存坐标信息
7. **Drawer**：执行实际的绘制操作

### 代码规范

- 使用面向对象编程，避免全局变量
- 为所有函数添加清晰的文档字符串
- 遵循Python PEP8代码风格规范
