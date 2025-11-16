from pynput import keyboard
import pyautogui

class KeyboardHandler:
    """键盘事件处理器，用于处理用户的键盘输入"""
    
    def __init__(self):
        self.should_exit = False
        self.is_paused = False
        self.listener = None
    
    def on_press(self, key):
        """按键处理函数"""
        try:
            # 捕获ESC键 - 退出程序
            if key == keyboard.Key.esc:
                self.should_exit = True
                # 立即抬起鼠标按键，确保停止所有绘制操作
                pyautogui.mouseUp()
                return False  # 停止监听器
            # 捕获空格键 - 暂停/继续绘制
            elif key == keyboard.Key.space:
                self.is_paused = not self.is_paused
                if self.is_paused:
                    # 暂停时立即抬起鼠标，防止拖动产生线条
                    pyautogui.mouseUp()
        except Exception as e:
            pass
    
    def start_listener(self):
        """启动键盘监听器"""
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
    
    def stop_listener(self):
        """停止键盘监听器"""
        if self.listener:
            self.listener.stop()
            self.listener = None
    
    def check_exit_condition(self):
        """检查是否应该退出程序"""
        return self.should_exit
    
    def check_pause_condition(self):
        """检查是否应该暂停程序"""
        return self.is_paused