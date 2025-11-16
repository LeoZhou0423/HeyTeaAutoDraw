import os
import json
from .config import config_manager

class CoordinateLoader:
    """坐标加载器，用于加载各种坐标数据"""
    
    def __init__(self):
        self.config_path = config_manager.get_config_path()
        self.canvas_coordinates_file = os.path.join(self.config_path, 'canvas_coordinates.txt')
        self.captured_coordinates_file = os.path.join(self.config_path, 'captured_coordinates.txt')
    
    def load_captured_coordinates(self):
        """
        加载捕获的坐标点
        
        Returns:
            坐标点列表
        """
        captured_points = []
        if os.path.exists(self.captured_coordinates_file):
            try:
                with open(self.captured_coordinates_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line:
                        # 解析坐标点，格式例如 "坐标点 1: (1234, 567)"
                        try:
                            # 找到括号中的内容
                            start = line.find('(')
                            end = line.find(')')
                            if start != -1 and end != -1:
                                coords = line[start+1:end]
                                x_str, y_str = coords.split(',')
                                x = int(x_str.strip())
                                y = int(y_str.strip())
                                captured_points.append((x, y))
                        except Exception as e:
                            pass
            except Exception as e:
                pass
        
        return captured_points
    
    def load_canvas_coordinates(self):
        """
        加载画布坐标
        
        Returns:
            tuple: (canvas_top_left, canvas_size) 或 None
        """
        try:
            with open(self.canvas_coordinates_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if len(lines) < 2:
                return None
            
            # 解析左上角坐标
            line1 = lines[0].strip()
            start = line1.find('(')
            end = line1.find(')')
            if start != -1 and end != -1:
                coords = line1[start+1:end]
                x_str, y_str = coords.split(',')
                top_left_x = int(x_str.strip())
                top_left_y = int(y_str.strip())
            else:
                return None
            
            # 解析画布尺寸
            line2 = lines[1].strip()
            start = line2.find(':')
            if start != -1:
                size_part = line2[start+1:].strip()
                width_str, height_str = size_part.split('x')
                width = int(width_str.strip())
                height = int(height_str.strip())
            else:
                return None
            
            return (top_left_x, top_left_y), (width, height)
            
        except FileNotFoundError:
            return None
        except Exception as e:
            return None