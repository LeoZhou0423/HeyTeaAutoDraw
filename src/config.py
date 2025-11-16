import os
import sys
import platform

class ConfigManager:
    """配置管理器，用于处理应用程序的配置路径和设置"""
    
    def __init__(self):
        self.base_path = self._get_base_path()
        self.config_path = self._get_config_path()
        self.output_path = self._get_output_path()
        
    def _get_base_path(self):
        """获取应用程序的基础路径"""
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        return base_path
    
    def _get_config_path(self):
        """根据操作系统获取配置路径"""
        if platform.system() == 'Windows':
            app_data_path = os.getenv('APPDATA')
            if app_data_path:
                config_path = os.path.join(app_data_path, 'XiChaDrawingTool')
            else:
                # Windows下APPDATA不可用时的回退方案
                config_path = os.path.join(self.base_path, 'config')
        elif platform.system() == 'Darwin':  # macOS
            # macOS应用数据目录
            app_data_path = os.path.expanduser('~/Library/Application Support')
            config_path = os.path.join(app_data_path, 'XiChaDrawingTool')
        elif platform.system() == 'Linux':
            # Linux应用数据目录
            app_data_path = os.path.expanduser('~/.config')
            config_path = os.path.join(app_data_path, 'XiChaDrawingTool')
        else:
            # 其他操作系统回退到当前目录
            config_path = os.path.join(self.base_path, 'config')
        
        # 创建配置目录（如果不存在）
        os.makedirs(config_path, exist_ok=True)
        return config_path
    
    def _get_output_path(self):
        """获取输出路径"""
        output_path = os.path.join(self.config_path, 'output')
        os.makedirs(output_path, exist_ok=True)
        return output_path
    
    def get_config_path(self):
        """获取配置文件路径"""
        return self.config_path
    
    def get_output_path(self):
        """获取输出文件路径"""
        return self.output_path
    
    def get_base_path(self):
        """获取应用程序基础路径"""
        return self.base_path

# 创建全局配置实例
config_manager = ConfigManager()