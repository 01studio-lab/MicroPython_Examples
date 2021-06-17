'''
实验名称：点亮板载LED灯
版本：v1.0
日期：2021.1
作者：01Studio
社区：www.01studio.org
'''

#导入Pin模块
from machine import Pin

LED = Pin(25, Pin.OUT) #构建LED对象
LED.value(1) #点亮LED,高电平点亮