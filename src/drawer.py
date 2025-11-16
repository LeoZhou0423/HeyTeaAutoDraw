import pyautogui
import time
from .keyboard_handler import KeyboardHandler

class Drawer:
    """绘制器，用于实际执行绘制操作"""
    
    def __init__(self):
        self.keyboard_handler = KeyboardHandler()
        # 配置pyautogui
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.001  # 极小延迟，提升绘制速度
    
    def draw_on_canvas(self, traced_paths, canvas_top_left, canvas_size, stroke_widths=None, scale_factor=1.0):
        """
        在画布上绘制路径
        
        Args:
            traced_paths: 要绘制的路径列表
            canvas_top_left: 画布左上角坐标 (x, y)
            canvas_size: 画布大小 (width, height)
            stroke_widths: 对应的笔触宽度列表
            scale_factor: 缩放因子
        """
        # 启动键盘监听器
        self.keyboard_handler.start_listener()
        
        try:
            # 计算画布的中心位置
            canvas_center_x = canvas_top_left[0] + canvas_size[0] // 2
            canvas_center_y = canvas_top_left[1] + canvas_size[1] // 2
            
            # 先将鼠标移动到画布中心
            pyautogui.moveTo(canvas_center_x, canvas_center_y)
            time.sleep(0.5)
            
            # 如果没有提供笔触宽度，使用默认值
            if stroke_widths is None:
                stroke_widths = [1.0] * len(traced_paths)
            
            # 遍历所有路径
            for i, path in enumerate(traced_paths):
                if self.keyboard_handler.check_exit_condition():
                    break
                
                # 等待直到绘制继续（如果暂停）
                while self.keyboard_handler.check_pause_condition():
                    if self.keyboard_handler.check_exit_condition():
                        break
                    time.sleep(0.1)
                
                # 计算路径的缩放后的坐标
                scaled_path = []
                for x, y in path:
                    # 缩放坐标
                    scaled_x = canvas_top_left[0] + int(x * scale_factor)
                    scaled_y = canvas_top_left[1] + int(y * scale_factor)
                    scaled_path.append((scaled_x, scaled_y))
                
                # 绘制路径
                if scaled_path:
                    # 移动到路径的起点
                    pyautogui.moveTo(scaled_path[0][0], scaled_path[0][1])
                    time.sleep(0.01)
                    
                    # 按下鼠标左键
                    pyautogui.mouseDown()
                    time.sleep(0.01)
                    
                    # 绘制路径的每个点
                    for j, (x, y) in enumerate(scaled_path[1:]):
                        if self.keyboard_handler.check_exit_condition():
                            pyautogui.mouseUp()
                            break
                        
                        # 等待直到绘制继续（如果暂停）
                        while self.keyboard_handler.check_pause_condition():
                            if self.keyboard_handler.check_exit_condition():
                                pyautogui.mouseUp()
                                break
                            time.sleep(0.1)
                        
                        # 移动到下一个点
                        pyautogui.moveTo(x, y)
                        time.sleep(0.001)
                    
                    # 释放鼠标左键
                    pyautogui.mouseUp()
                    time.sleep(0.01)
            
        finally:
            # 停止键盘监听器
            self.keyboard_handler.stop_listener()
            # 确保鼠标按键已释放
            pyautogui.mouseUp()