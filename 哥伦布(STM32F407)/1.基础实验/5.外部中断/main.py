'''
实验名称：外部中断
版本：v1.0
日期：2020.12
作者：01Studio
社区：www.01studio.org
'''

from pyb import Pin,ExtInt,LED

#定义回调函数，需要将ext中断号传递进来
def fun1(ext):
    LED(4).toggle()

ext = ExtInt(Pin('A0'), ExtInt.IRQ_FALLING, Pin.PULL_UP, fun1) #下降沿触发，打开上拉电阻
