'''
左摇杆光标移动; 右摇杆滚轮; A键鼠标左键; B键鼠标右键; X键Backspace删除; Y键退出程序
LT键 <-; RT键 ->
十字按键：下 将焦点转移至任务栏；左、右 左右移动; A 确定; B 取消
在浏览器中时; LB键 切换到左一个浏览器页面; RB键 切换到右一个浏览器页面  
'''

import pygame
from sys import exit
import pyautogui
import time
import pygetwindow as gw
import win32gui  
import win32con  
import ctypes  

import vibration



def is_browser_active():
    # 获取当前活动窗口
    active_window = gw.getActiveWindow()

    # 如果没有活动窗口，返回 False
    if active_window is None:
        return False

    # 获取当前活动窗口的标题
    window_title = active_window.title

    # 浏览器的关键字列表
    browser_keywords = ["Chrome", "Firefox", "Edge", "Safari"]

    # 判断当前活动窗口的标题是否包含浏览器的关键字
    for keyword in browser_keywords:
        if keyword in window_title:
            return True

    return False



# 初始化 Pygame
pygame.init()

# 初始化手柄
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("未检测到手柄连接！")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

# 获取屏幕大小
screen_width, screen_height = pyautogui.size()

running = True

mouse_move_yes = 0
scroll_axis_yes = 0

# 定义隐藏和显示鼠标的函数  
def hide_cursor():  
    ctypes.windll.user32.ShowCursor(False)  

def show_cursor():  
    ctypes.windll.user32.ShowCursor(True)  


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取手柄输入
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)
    scroll_axis = joystick.get_axis(3)
    left = joystick.get_axis(4)
    right = joystick.get_axis(5)


     # 检测十字按键（D-Pad）  
    if event.type == pygame.JOYHATMOTION:  # D-Pad 事件  
        hat_value = joystick.get_hat(0)  # 获取第一个 hat 的状态  
        x, y = hat_value  # 分别获取 x 和 y 的值  

        if x == -1:   #print("D-Pad 向左")  
            pyautogui.press('left')  
        elif x == 1:  #print("D-Pad 向右")  
            pyautogui.press('right')  
        if y == -1:  #print("D-Pad 向下")  
            pyautogui.hotkey('win', 't')  # 切换到任务栏  
            time.sleep(0.5)  # 等待任务栏切换完成  

            # 进入等待输入的循环  
            waiting = True  
            # 隐藏鼠标  
            hide_cursor()  
            while waiting:  
                # 获取新的事件  
                for sub_event in pygame.event.get():  
                    if sub_event.type == pygame.QUIT:  
                        running = False  
                        waiting = False  
                        break  

                    # 检测新的 D-Pad 输入  
                    if sub_event.type == pygame.JOYHATMOTION:  
                        hat_value = joystick.get_hat(0)  
                        x, y = hat_value  
                        if x == -1:   #print("D-Pad 向左")  
                            pyautogui.press('left')  
                        elif x == 1:  #print("D-Pad 向右")  
                            pyautogui.press('right')  

                    # 检测 A 键或 B 键  
                    if joystick.get_button(0):  # A键  
                        pyautogui.press('enter')  # 模拟按下 Enter 键  
                        waiting = False  # 退出等待循环  
                    elif joystick.get_button(1):  # B键  
                        pyautogui.press('esc')  # 模拟按下 Esc 键，取消任务栏焦点  
                        waiting = False  # 退出等待循环  

            # 恢复鼠标  
            show_cursor()  

             



    #if scroll_axis < 0.1 and scroll_axis > -0.1:
    if abs(scroll_axis) < 0.1:
        '''没有推动右摇杆'''
        scroll_axis_yes = 0
        #print("没有推动右摇杆")
    if scroll_axis_yes == 0:
        if abs(scroll_axis) > 0.1:
            scroll_axis_yes = 1
            start_push_scroll = time.time()
            #print("计时开始")

    
    if abs(x_axis) < 0.1 and abs(y_axis) < 0.1:
        '''没有推动左摇杆'''
        mouse_move_yes = 0
        #print("没有推动左摇杆")
    if mouse_move_yes == 0:
        if abs(x_axis) > 0.1 or abs(y_axis) > 0.1 or (x_axis**2+y_axis**2)>0.01:
            mouse_move_yes = 1
            start_mouse_moving = time.time()
            #print("计时开始")


    # 设置鼠标移动
    mouse_speed = 200
    if mouse_move_yes == 1 and time.time() - start_mouse_moving > 0.5:
        mouse_speed = 800 # 定义鼠标速度
        #print("鼠标加速")
    else:
        mouse_speed = 200 # 定义鼠标速度
    # 计算新的鼠标位置
    new_x = pyautogui.position()[0] + x_axis * mouse_speed
    new_y = pyautogui.position()[1] + y_axis * mouse_speed
    # 防止鼠标移出屏幕边界
    new_x = max(3, min(new_x, screen_width-3))
    new_y = max(3, min(new_y, screen_height-3))
    pyautogui.moveTo(new_x, new_y)


    scroll_speed = 100
    # 模拟鼠标滚轮
    if scroll_axis_yes == 1 and time.time() - start_push_scroll > 2:
        scroll_speed = 500 # 定义滚轮速度
        #print("滚动加速")
    else:
        scroll_speed = 100 # 定义滚轮速度
    scroll_amount = int(scroll_axis * scroll_speed)  # 将滚轮值转换为整数
    pyautogui.scroll(scroll_amount)


    # 模拟鼠标左键点击
    if joystick.get_button(0):  # A键
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        

    # 模拟鼠标右键点击
    if joystick.get_button(1):  # B键
        pyautogui.mouseDown(button='right')
        pyautogui.mouseUp(button='right')

    # 模拟键盘Backspace键
    if joystick.get_button(2):  # X键
        pyautogui.press('backspace')

    
    if is_browser_active():
        if joystick.get_button(4):  # LB键 切换到左一个浏览器页面  
            pyautogui.hotkey('ctrl', 'shift', 'tab')  

        if joystick.get_button(5):  # RB键 切换到右一个浏览器页面  
            pyautogui.hotkey('ctrl', 'tab')  


    if left > 0:  # LT键
        pyautogui.press('left')

    if right > 0:  # RT键
        pyautogui.press('right')

    # 退出程序
    if joystick.get_button(3):  # Y键

        #手柄震动
        start_vibration = time.time()
        while 1:
            vibration.set_vibration(0, 1.0, 0.5)
            if time.time() - start_vibration > 0.5:
                break

        running = False
  

pygame.quit()
