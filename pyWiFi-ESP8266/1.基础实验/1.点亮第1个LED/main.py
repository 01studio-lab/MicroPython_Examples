'''
实验名称：点亮LED蓝灯
版本：v1.0
日期：2019.7
作者：01Studio
'''

from machine import Pin #导入Pin模块
led=Pin(2,Pin.OUT) #构建led对象，GPIO2,输出
led.value(0) #点亮LED
