'''
实验名称：继电器
版本：v1.0
日期：2021.8
作者：01Studio
说明：通过按键改变继电器通断状态（外部中断方式）
'''

#导入相关模块
from machine import Pin
import time

relay=Pin(10,Pin.OUT,value=1) #构建继电器对象,默认断开
KEY=Pin(0,Pin.IN,Pin.PULL_UP) #构建KEY对象
state=0  #LED引脚状态

#LED状态翻转函数
def fun(KEY):
    global state
    time.sleep_ms(10) #消除抖动
    if KEY.value()==0: #确认按键被按下
        state = not state
        relay.value(state)

KEY.irq(fun,Pin.IRQ_FALLING) #定义中断，下降沿触发
