'''
实验名称：继电器
版本：v1.0
日期：2020-4-23
作者：01Studio
社区：www.01studio.org
'''

from pyb import Pin,ExtInt

relay = Pin('Y11',Pin.OUT_PP,value=1) #继电器连接到Y11
state=1 #继电器状态控制

def fun(ext):
    global state
    state=not state
    relay.value(state) #改变继电器状态

ext = ExtInt(Pin('Y1'), ExtInt.IRQ_FALLING, Pin.PULL_UP, fun) #下降沿触发，打开上拉电阻
