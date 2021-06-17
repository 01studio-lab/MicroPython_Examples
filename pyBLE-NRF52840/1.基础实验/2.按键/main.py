'''
实验名称：按键（GPIO）
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

#构建按键对象和初始化
switch = DigitalInOut(board.SWITCH) #定义引脚编号
switch.direction = Direction.INPUT #IO为输入
switch.pull = Pull.UP #打开上拉电阻

while True:

    if switch.value == 0: #按键被按下
        led.value = True #点亮LED

    else:
        led.value = False #关闭LED
