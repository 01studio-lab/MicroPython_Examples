'''
实验名称：外部中断
版本：v1.0
日期：2019.9
作者：01Studio
社区：www.01studio.org
'''

from pyb import Pin,ExtInt,LED

callback = lambda e: LED(3).toggle()
#下降沿触发，打开上拉电阻
ext = ExtInt(Pin('P9'), ExtInt.IRQ_FALLING, Pin.PULL_UP, callback)
