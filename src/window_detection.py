import pygetwindow as gw
import pyautogui
import time
import os
import sys
import cv2
import numpy as np

# 获取系统AppData路径用于存储配置文件
def get_config_paths():
    """获取配置文件和输出文件的路径"""
    app_data_path = os.getenv('APPDATA')
    if app_data_path:
        config_path = os.path.join(app_data_path, 'XiChaDrawingTool')
        output_path = os.path.join(app_data_path, 'XiChaDrawingTool', 'output')
    else:
        # 如果AppData不可用，回退到相对路径
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config_path = os.path.join(base_path, 'config')
        output_path = os.path.join(base_path, 'output')
    
    # 创建配置目录和输出目录（如果不存在）
    os.makedirs(config_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)
    
    return config_path, output_path

# 获取配置路径
config_path, output_path = get_config_paths()


        
def get_target_window():
    """
    获取目标窗口对象
    尝试匹配"定制喜贴"或"喜茶GO"窗口
    
    Returns:
        pygetwindow.Window: 找到的目标窗口对象，如果未找到则返回None
    """
    for title in ['定制喜贴', '喜茶GO']:
        windows = gw.getWindowsWithTitle(title)
        if windows:
            return windows[0]
    return None


def resize_and_position_window(win):
    """
    调整窗口大小和位置
    
    Args:
        win (pygetwindow.Window): 要调整的窗口对象
    """
    # 激活窗口到前台
    win.activate()
    time.sleep(1)  # 等待窗口完全激活
    
    # 调整窗口大小为固定的450 x 1089
    target_width = 450
    target_height = 1089
    win.resizeTo(target_width, target_height)
    time.sleep(1)  # 等待窗口大小调整完成
    
    # 自动将窗口移动到指定位置(1371, 0)
    target_left = 1371
    target_top = 0
    win.moveTo(target_left, target_top)
    time.sleep(0.5)  # 等待窗口位置调整完成
    
    return win


def detect_gray_area_by_color(win):
    """
    通过颜色识别检测灰色区域
    
    Args:
        win (pygetwindow.Window): 窗口对象
        
    Returns:
        tuple: (left, top, width, height) 或 None
    """
    try:
        # 先截取整个窗口
        window_screenshot = pyautogui.screenshot(region=(int(win.left), int(win.top), int(win.width), int(win.height)))
        
        # 将PIL图像转换为OpenCV格式
        img = cv2.cvtColor(np.array(window_screenshot), cv2.COLOR_RGB2BGR)
        
        # 直接搜索固定颜色 #EEEEEE 的灰色区域，扩大颜色范围
        lower_color = np.array([220, 220, 220])  # 降低下限
        upper_color = np.array([240, 240, 240])  # 提高上限
        mask = cv2.inRange(img, lower_color, upper_color)
        
        # 查找轮廓
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 寻找最大的轮廓，假设这是我们要找的灰色区域
        if contours:
            # 按面积排序轮廓
            contours = sorted(contours, key=cv2.contourArea, reverse=True)
            
            # 取面积最大的轮廓
            largest_contour = contours[0]
            
            # 获取边界框
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # 计算在屏幕上的实际坐标
            left = int(win.left + x)
            top = int(win.top + y)
            canvas_width = int(w)
            canvas_height = int(h)
            
            return left, top, canvas_width, canvas_height
        
        return None
        
    except Exception as e:
        return None


def estimate_gray_area(win):
    """
    估算灰色区域的位置和大小
    
    Args:
        win (pygetwindow.Window): 窗口对象
        
    Returns:
        tuple: (left, top, width, height)
    """
    margin_left = win.width * 0.1  # 左侧边距约为窗口宽度的10%
    margin_top = win.height * 0.2   # 顶部边距约为窗口高度的20%
    canvas_width = win.width * 0.8   # 画布宽度约为窗口宽度的80%
    canvas_height = win.height * 0.6 # 画布高度约为窗口高度的60%
    
    # 计算截图的左上角坐标并转换为整数
    left = int(win.left + margin_left)
    top = int(win.top + margin_top)
    canvas_width = int(canvas_width)
    canvas_height = int(canvas_height)
    
    return left, top, canvas_width, canvas_height


def save_canvas_coordinates(left, top, width, height):
    """
    保存画布坐标到文件
    
    Args:
        left (int): 左上角X坐标
        top (int): 左上角Y坐标
        width (int): 宽度
        height (int): 高度
    """
    # 截取灰色区域
    try:
        screenshot = pyautogui.screenshot(region=(left, top, width, height))
        output_file = os.path.join(output_path, 'canvas_screenshot.png')
        screenshot.save(output_file)
        
        # 记录灰色区域坐标到文件（指定utf-8编码避免乱码）
        config_file = os.path.join(config_path, 'canvas_coordinates.txt')
        with open(config_file, 'w', encoding='utf-8') as f:
            f.write(f"灰色区域左上角坐标: ({left}, {top})\n")
            f.write(f"灰色区域尺寸: {width} x {height}\n")
            f.write(f"灰色区域右下角坐标: ({left + width}, {top + height})\n")
        
        return True
    except Exception as e:
        return False


def load_brush_widths():
    """
    加载存储的画笔宽度数据
    """
    config_file = os.path.join(config_path, 'brush_widths.txt')
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            brush_widths = list(map(int, f.read().split(',')))
        return brush_widths
    return None


def main():
    """主函数，执行窗口检测并保存画布坐标"""
    # 获取目标窗口
    target_window = get_target_window()
    
    if not target_window:
        raise Exception("找不到目标窗口（'定制喜贴'或'喜茶GO'）")
    
    # 调整窗口大小和位置
    win = resize_and_position_window(target_window)
    
    # 检测灰色区域
    gray_area = detect_gray_area_by_color(win)
    
    if gray_area:
        left, top, width, height = gray_area
    else:
        left, top, width, height = estimate_gray_area(win)
    
    # 保存画布坐标
    if not save_canvas_coordinates(left, top, width, height):
        raise Exception("保存画布坐标失败")
    
    return True

# 如果直接运行此脚本
if __name__ == "__main__":
    main()