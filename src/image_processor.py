import cv2
import numpy as np
import os
from .config import config_manager

class ImageProcessor:
    """图像处理器，用于处理图像和提取轮廓"""
    
    def __init__(self):
        self.config_manager = config_manager
        self.output_path = self.config_manager.get_output_path()
    
    def preprocess_image(self, image_path):
        """
        预处理图像，转换为二值图像
        
        Args:
            image_path: 输入图像路径
            
        Returns:
            二值化处理后的图像
        """
        # 读取图像
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"无法读取图像: {image_path}")
        
        # 转换为灰度图像
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 应用高斯模糊减少噪声
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 使用自适应阈值将图像二值化
        binary = cv2.adaptiveThreshold(
            blurred, 255, 
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY_INV, 
            11, 2
        )
        
        return binary
    
    def extract_contours(self, binary_img):
        """
        从二值图像中提取轮廓
        
        Args:
            binary_img: 二值化图像
            
        Returns:
            提取的轮廓列表
        """
        # 查找轮廓
        contours, _ = cv2.findContours(
            binary_img, 
            cv2.RETR_EXTERNAL, 
            cv2.CHAIN_APPROX_SIMPLE
        )
        
        # 按轮廓面积排序，保留较大的轮廓
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        return contours
    
    def extract_strict_strokes(self, image_path):
        """
        严格提取图像中的笔触，用于高质量绘制
        
        Args:
            image_path: 输入图像路径
            
        Returns:
            traced_paths: 追踪的路径列表
            stroke_widths: 对应的笔触宽度列表
        """
        # 读取图像
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"无法读取图像: {image_path}")
        
        # 转换为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 应用中值滤波去除噪声
        median = cv2.medianBlur(gray, 5)
        
        # 检测边缘
        edges = cv2.Canny(median, 50, 150, apertureSize=3)
        
        # 形态学操作：膨胀和腐蚀，以连接邻近的边缘
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        edges = cv2.dilate(edges, kernel, iterations=1)
        edges = cv2.erode(edges, kernel, iterations=1)
        
        # 查找轮廓
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        traced_paths = []
        stroke_widths = []
        
        # 遍历每个轮廓
        for contour in contours:
            # 跳过太小的轮廓
            if cv2.contourArea(contour) < 10:
                continue
            
            # 计算轮廓的周长
            perimeter = cv2.arcLength(contour, True)
            
            # 简化轮廓，减少点的数量
            epsilon = 0.001 * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # 将轮廓转换为路径点列表
            path = []
            for point in approx:
                x, y = point[0]
                path.append((x, y))
            
            traced_paths.append(path)
            
            # 估算笔触宽度
            x, y, w, h = cv2.boundingRect(contour)
            avg_width = max(1, (w + h) / 4)
            stroke_widths.append(avg_width)
        
        return traced_paths, stroke_widths