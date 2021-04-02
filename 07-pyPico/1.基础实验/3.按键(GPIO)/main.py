'''
实验名称：按键(GPIO)
版本：v1.0
日期：2021-1
作者：01Studio
社区：www.01studio.org
'''

from machine import Pin

#构建LED对象
led=Pin(25, Pin.OUT)

#配置按键
key = Pin(14, Pin.IN, Pin.PULL_UP)

while True:

    if key.value()==0: #KEY被按下接地
        led.high()    #点亮LED
        
    else:
        led.low()     #关闭LED