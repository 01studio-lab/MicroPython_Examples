'''
实验名称：流水灯
版本：v1.0
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