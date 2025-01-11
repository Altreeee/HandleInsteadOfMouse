'''
想搞一个检测到设备连接就显示一个图形界面，提示是否要运行这个程序，但这个还有问题。
'''

import win32gui  
import win32con  
import win32api  
import win32gui_struct  
import ctypes  
from ctypes import wintypes  

# 定义设备通知的常量  
DBT_DEVICEARRIVAL = 0x8000  # 设备连接  
DBT_DEVICEREMOVECOMPLETE = 0x8004  # 设备断开  
DBT_DEVTYP_DEVICEINTERFACE = 0x0005  

# 定义 GUID，用于检测 HID 设备（包括手柄）  
GUID_DEVINTERFACE_HID = ctypes.c_byte * 16  
HID_GUID = GUID_DEVINTERFACE_HID(  
    0x4D, 0x1E, 0x55, 0xB2, 0xF2, 0xBA, 0xD0, 0x11,  
    0x9E, 0xE3, 0x00, 0xC0, 0x4F, 0xB1, 0x94, 0x92  
)  

class DeviceNotification:  
    def __init__(self):  
        self.hwnd = None  

    def start(self):  
        # 定义窗口类  
        wc = win32gui.WNDCLASS()  
        wc.lpszClassName = 'DeviceChangeListener'  
        wc.lpfnWndProc = self._wnd_proc  
        wc.hInstance = win32api.GetModuleHandle(None)  
        class_atom = win32gui.RegisterClass(wc)  

        # 创建隐藏窗口  
        self.hwnd = win32gui.CreateWindow(  
            class_atom,  
            'Device Listener',  
            0,  
            0, 0, 0, 0,  
            0, 0, wc.hInstance, None  
        )  

        # 注册设备通知  
        filter = win32gui_struct.PackDEV_BROADCAST_DEVICEINTERFACE(  
            win32con.DBT_DEVTYP_DEVICEINTERFACE,  
            HID_GUID  
        )  
        self.dev_notify = ctypes.windll.user32.RegisterDeviceNotificationW(  
            self.hwnd,  
            filter,  
            win32con.DEVICE_NOTIFY_WINDOW_HANDLE  
        )  

        # 开始消息循环  
        print("Listening for device changes...")  
        win32gui.PumpMessages()  

    def _wnd_proc(self, hwnd, msg, wparam, lparam):  
        if msg == win32con.WM_DEVICECHANGE:  
            if wparam == DBT_DEVICEARRIVAL:  
                print("Device connected!")  
                self._check_device(lparam)  
            elif wparam == DBT_DEVICEREMOVECOMPLETE:  
                print("Device disconnected!")  
        return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)  

    def _check_device(self, lparam):  
        # 检查设备是否是手柄  
        device = win32gui_struct.UnpackDEV_BROADCAST(lparam)  
        if device.dbch_devicetype == DBT_DEVTYP_DEVICEINTERFACE:  
            print(f"Device path: {device.dbcc_name}")  
            print("This might be a game controller!")  

if __name__ == "__main__":  
    listener = DeviceNotification()  
    listener.start()