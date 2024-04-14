import pygame
from pygame.locals import *
from sys import exit

# 初始化PyGame
pygame.init()

# 设置游戏窗口
screen = pygame.display.set_mode((800,600))

'''# 创建一个时钟对象，用于控制游戏的更新速度
clock = pygame.time.Clock()

# 主循环
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 读取USB控制器的输入
    joystick_count = pygame.joystick.get_count()
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()

        # 获取控制器的轴输入
        num_axes = joystick.get_numaxes()
        for axis_id in range(num_axes):
            axis_value = joystick.get_axis(axis_id)
            print(f"Axis {axis_id}: {axis_value}")

        # 获取控制器的按钮输入
        num_buttons = joystick.get_numbuttons()
        for button_id in range(num_buttons):
            button_value = joystick.get_button(button_id)
            print(f"Button {button_id}: {button_value}")

    # 更新游戏画面
    pygame.display.flip()

    # 控制游戏更新速率为30帧每秒
    clock.tick(30)

# 退出PyGame
pygame.quit()'''

rect2 = Rect(50, 60, 200, 80)
running = True
x=0
y=0

# 初始化手柄
pygame.joystick.init()
if pygame.joystick.get_count() == 0:
    print("未检测到手柄连接！")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        '''
        #键盘输入
        if event.type == KEYDOWN:
            if event.key==K_LEFT:
                x= -1
                y=0
            if event.key == K_RIGHT:
                x=1
                y=0
            if event.key == K_UP:
                x = 0
                y = -1
            if event.key == K_DOWN:
                x = 0
                y = 1
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                x = 0
            if event.key == K_UP or event.key == K_DOWN:
                y = 0
        '''
    
    # 获取手柄输入
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # 设置移动速度
    x = int(x_axis * 2)
    y = int(y_axis * 2)


    rect2.move_ip(x,y)

    # 确保矩形不会超出屏幕边界
    rect2.left = max(rect2.left, 0)
    rect2.top = max(rect2.top, 0)
    rect2.right = min(rect2.right, 800)
    rect2.bottom = min(rect2.bottom, 600)

    screen.fill((127,127,127))
    pygame.draw.rect(screen, (0,0,255), rect2, 5)
    pygame.display.update()

pygame.quit()