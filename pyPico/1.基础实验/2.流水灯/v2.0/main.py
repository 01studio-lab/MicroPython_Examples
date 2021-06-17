'''
实验名称：流水灯
版本：v2.0
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

LEDS = [LED1,LED2,LED3]

# 相当于for i in [0, 1, 2]，LED[i].low()执行3次，分别是LED 1，2，3
for i in range(3):
    LEDS[i].low()
    
while True:
    #使用for循环
    for i in range(3):
        LEDS[i].high()
        time.sleep_ms(1000) #延时1000毫秒，即1秒
        LEDS[i].low()

