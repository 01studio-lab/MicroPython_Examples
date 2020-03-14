'''
实验名称：外部中断
版本：v1.0
日期：2019-4-1
作者：01Studio
社区：www.01studio.org
'''

from pyb import Pin,ExtInt,LED

callback = lambda e: LED(4).toggle()
ext = ExtInt(Pin('Y1'), ExtInt.IRQ_FALLING, Pin.PULL_UP, callback) #下降沿触发，打开上拉电阻
