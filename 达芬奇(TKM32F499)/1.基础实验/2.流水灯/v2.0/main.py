'''
实验名称：流水灯
版本：v2.0
日期：2021.4
作者：CaptainJackey
实验平台：01Studio - 达芬奇
'''

#导入相关模块
from machine import Pin
import time

#构建LED对象
LED1 = Pin('C3', Pin.OUT)
LED2 = Pin('C6', Pin.OUT)
LED3 = Pin('C7', Pin.OUT)

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

