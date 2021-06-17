'''
实验名称：按键(GPIO)
版本：v1.0
日期：2021-1
作者：01Studio
实验平台：01Studio - 达芬奇
社区：www.01studio.org
'''

from machine import Pin
import time

#构建LED对象
led=Pin('C7', Pin.OUT)

#配置按键
key = Pin('A0', Pin.IN, Pin.PULL_DOWN)

while True:

    if key.value()==1: #KEY被按下拉高
        
        led.high()    #点亮LED
        
    else:
        led.low()     #关闭LED