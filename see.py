import pygame
import time
from sys import exit

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

    # 输出手柄的附加轴值
    for i in range(joystick.get_numaxes()):
        axis_value = joystick.get_axis(i)
        print(f"附加轴 {i}: {axis_value}")

    # 输出手柄的按钮值
    for i in range(joystick.get_numbuttons()):
        button_value = joystick.get_button(i)
        print(f"按钮 {i}: {button_value}")

    # 添加延迟
    time.sleep(2)

pygame.quit()
