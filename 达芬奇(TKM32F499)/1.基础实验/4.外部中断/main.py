'''
实验名称：外部中断
版本：v1.0
日期：2021-1
作者：01Studio
实验平台：达芬奇
社区：www.01studio.org
'''

from machine import Pin
import time

#构建LED对象
led=Pin('C7', Pin.OUT)

#配置按键
key = Pin('A0', Pin.IN, Pin.PULL_DOWN)

state=0 #LED 引脚状态

#LED 状态翻转函数
def fun(key):

    global state
    time.sleep_ms(10) #消除抖动
    if key.value()==1: #确认按键被按下,开发板按下拉高
        state = not state
        led.value(state)
    
key.irq(fun,Pin.IRQ_RISING) #定义中断，下降沿触发