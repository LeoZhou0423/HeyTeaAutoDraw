import cv2
import numpy as np
from skimage.morphology import skeletonize
import math

class PathProcessor:
    """路径处理器，用于处理和优化绘制路径"""
    
    def __init__(self):
        pass
    
    def extend_short_path(self, path, threshold=7, target_length=6):
        """
        扩展过短的路径使其满足绘制条件
        
        Args:
            path: 路径坐标列表
            threshold: 判断是否需要延长的阈值（max(x)-min(x)或max(y)-min(y)的最小值）
            target_length: 延长后的目标长度（max(x)-min(x)或max(y)-min(y)需要达到的值）
            
        Returns:
            延长后的路径坐标列表
        """
        if not path or len(path) < 2:
            return path  # 无效路径直接返回
        
        # 计算原始路径的边界
        xs = [p[0] for p in path]
        ys = [p[1] for p in path]
        width = max(xs) - min(xs)
        height = max(ys) - min(ys)
        
        # 如果路径已经足够长，直接返回
        if max(width, height) >= threshold:
            return path
        
        # 计算需要延长的方向（从起点到终点）
        start_point = path[0]
        end_point = path[-1]
        
        # 计算方向向量
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        
        # 计算路径长度
        path_length = math.hypot(dx, dy)
        
        if path_length == 0:
            # 如果是一个点，向任意方向扩展
            dx, dy = 1, 1
            path_length = math.hypot(dx, dy)
        
        # 计算需要延长的比例
        extension_ratio = target_length / path_length
        
        # 计算新的起点和终点
        new_start_x = start_point[0] - dx * extension_ratio / 2
        new_start_y = start_point[1] - dy * extension_ratio / 2
        new_end_x = end_point[0] + dx * extension_ratio / 2
        new_end_y = end_point[1] + dy * extension_ratio / 2
        
        # 创建新的路径（保持中间点不变，只延长起点和终点）
        new_path = [(new_start_x, new_start_y)]
        new_path.extend(path[1:-1])
        new_path.append((new_end_x, new_end_y))
        
        return new_path
    
    def get_line_width(self, contour):
        """
        估算轮廓的平均宽度
        
        Args:
            contour: 轮廓点列表
            
        Returns:
            估算的平均宽度
        """
        if len(contour) < 5:
            return 1.0
        
        # 计算轮廓的边界框
        x, y, w, h = cv2.boundingRect(contour)
        
        # 计算轮廓的面积和周长
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return 1.0
        
        # 使用形状因子估算宽度
        circularity = 4 * np.pi * area / (perimeter ** 2) if perimeter > 0 else 0
        
        # 根据形状选择合适的宽度估算方法
        if circularity > 0.7:  # 接近圆形
            width = np.sqrt(area / np.pi) * 2
        elif w > h:  # 更宽
            width = area / h
        else:  # 更高
            width = area / w
        
        return max(1.0, width)  # 确保宽度至少为1
    
    def filter_short_paths(self, paths, min_points=3):
        """
        过滤掉点数量过少的路径
        
        Args:
            paths: 路径列表
            min_points: 路径的最小点数量
            
        Returns:
            过滤后的路径列表
        """
        return [path for path in paths if len(path) >= min_points]
    
    def extract_skeleton_paths(self, binary_img):
        """
        从二值图像中提取骨架路径
        
        Args:
            binary_img: 二值图像
            
        Returns:
            提取的路径列表
        """
        # 确保图像是二值的（0或1）
        binary_img = (binary_img > 0).astype(np.uint8)
        
        # 应用骨架化算法
        skeleton = skeletonize(binary_img).astype(np.uint8) * 255
        
        # 查找骨架的轮廓
        contours, _ = cv2.findContours(skeleton, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 将轮廓转换为路径点列表
        paths = []
        for contour in contours:
            if len(contour) < 2:
                continue
            
            path = []
            for point in contour:
                x, y = point[0]
                path.append((x, y))
            
            paths.append(path)
        
        return paths