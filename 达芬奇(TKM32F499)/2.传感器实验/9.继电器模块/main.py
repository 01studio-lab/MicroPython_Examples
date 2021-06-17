'''
实验名称：继电器模块
版本：v1.0
日期：2021-4
作者：01Studio
实验平台：达芬奇
社区：www.01studio.org
'''

from machine import Pin
import time

#构建继电器对象
relay=Pin('B1', Pin.OUT,value=1)

#配置按键
key = Pin('A0', Pin.IN, Pin.PULL_DOWN)

state=0 #LED 引脚状态

#继电器通断
def fun(key):

    global state
    time.sleep_ms(10) #消除抖动
    if key.value()==1: #确认按键被按下,开发板按下拉高
        state = not state
        relay.value(state)
    
key.irq(fun,Pin.IRQ_RISING) #定义中断，下降沿触发