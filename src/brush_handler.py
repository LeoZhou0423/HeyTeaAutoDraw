import os
import pyautogui
import time
import json
from .config import config_manager

class BrushHandler:
    """画笔处理器，用于处理画笔大小检测和切换"""
    
    def __init__(self):
        self.config_path = config_manager.get_config_path()
        self.slider_positions_file = self._get_slider_positions_file()
    
    def _get_slider_positions_file(self):
        """获取画笔滑块位置文件路径"""
        return os.path.join(self.config_path, 'brush_slider_positions.json')
    
    def detect_brush_size_slider(self, canvas_top_left, canvas_size):
        """
        检测画笔大小滑块的位置
        
        Args:
            canvas_top_left: 画布左上角坐标 (x, y)
            canvas_size: 画布大小 (width, height)
            
        Returns:
            画笔滑块位置字典 {size: (x, y)}
        """
        # 假设滑块位于画布的上方，这部分可能需要根据实际应用进行调整
        canvas_x, canvas_y = canvas_top_left
        canvas_width, canvas_height = canvas_size
        
        # 定义画笔大小和对应的位置（示例，需要根据实际情况调整）
        brush_sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        # 计算滑块位置（示例位置，需要根据实际应用调整）
        slider_start_x = canvas_x + canvas_width // 2 - 100
        slider_start_y = canvas_y - 50
        slider_width = 200
        
        positions = {}
        for i, size in enumerate(brush_sizes):
            x = slider_start_x + int((i / (len(brush_sizes) - 1)) * slider_width)
            y = slider_start_y
            positions[size] = (x, y)
        
        return positions
    
    def load_brush_slider_positions(self):
        """
        加载保存的画笔滑块位置
        
        Returns:
            画笔滑块位置字典
        """
        try:
            with open(self.slider_positions_file, 'r') as f:
                positions = json.load(f)
            return positions
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def save_brush_slider_positions(self, positions):
        """
        保存画笔滑块位置
        
        Args:
            positions: 画笔滑块位置字典
        """
        try:
            with open(self.slider_positions_file, 'w') as f:
                json.dump(positions, f, indent=2)
            return True
        except Exception as e:
            return False
    
    def map_width_to_brush_size(self, width):
        """
        将线条宽度映射到对应的画笔大小
        
        Args:
            width: 线条宽度
            
        Returns:
            对应的画笔大小
        """
        # 简单的线性映射，可根据实际情况调整
        if width <= 1:
            return 1
        elif width <= 2:
            return 2
        elif width <= 3:
            return 3
        elif width <= 4:
            return 4
        elif width <= 5:
            return 5
        elif width <= 6:
            return 6
        elif width <= 7:
            return 7
        elif width <= 8:
            return 8
        elif width <= 9:
            return 9
        else:
            return 10
    
    def switch_brush_to_size(self, size_index, slider_positions):
        """
        切换画笔大小
        
        Args:
            size_index: 画笔大小索引
            slider_positions: 画笔滑块位置字典
        """
        if size_index in slider_positions:
            x, y = slider_positions[size_index]
            # 点击滑块位置
            pyautogui.click(x, y)
            time.sleep(0.1)  # 等待切换完成
            return True
        return False