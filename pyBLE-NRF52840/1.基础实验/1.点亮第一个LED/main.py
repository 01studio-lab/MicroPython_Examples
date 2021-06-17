'''
实验名称：点亮LED蓝灯
版本：v1.0
日期：2020.4
作者：01Studio
'''
#导入相关模块

import board
from digitalio import DigitalInOut, Direction, Pull

#构建LED对象和初始化
led = DigitalInOut(board.BLUE_LED) #定义引脚编号
led.direction = Direction.OUTPUT  #IO为输出

led.value = True #输出高电平，点亮LED

#阻塞IO，让程序保持运行
while True:
    pass
