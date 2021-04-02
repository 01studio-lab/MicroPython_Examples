'''
实验名称：流水灯
版本：v1.0
日期：2021.1
作者：01Studio
'''

#导入相关模块
from machine import Pin
import time

#构建LED对象
LED1 = Pin(18, Pin.OUT)
LED2 = Pin(19, Pin.OUT)
LED3 = Pin(20, Pin.OUT)

#关闭所有LED
LED1.low()
LED2.low()
LED3.low()

#while True表示一直循环
while True:

    #LED1亮1秒
    LED1.high()
    time.sleep_ms(1000)
    LED1.low()

    #LED2亮1秒
    LED2.value(1)
    time.sleep_ms(1000)
    LED2.value(0)

    #LED3亮1秒
    LED3.value(1)
    time.sleep_ms(1000)
    LED3.value(0)