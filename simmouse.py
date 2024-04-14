'''
左摇杆光标移动，右摇杆滚轮，A键鼠标左键，B键鼠标右键，X键Backspace删除，Y键退出程序
'''

import pygame
from sys import exit
import pyautogui

# 初始化 Pygame
pygame.init()

# 初始化手柄
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("未检测到手柄连接！")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 获取手柄输入
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)
    scroll_axis = joystick.get_axis(3)

    # 设置鼠标移动
    mouse_speed = 200
    pyautogui.moveRel(x_axis * mouse_speed, y_axis * mouse_speed)

    # 模拟鼠标滚轮
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

    # 退出程序
    if joystick.get_button(3):  # Y键
        running = False
  

pygame.quit()
