'''
实验名称：点亮LED灯
版本：v1.0
日期：2021.4
作者：01Studio
社区：www.01studio.org
实验平台：01Studio - 达芬奇
'''

#导入Pin模块
from machine import Pin

LED = Pin('C7', Pin.OUT) #构建LED对象
LED.value(1) #点亮LED,高电平点亮