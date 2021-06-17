
'''
实验名称：RGB灯带
版本：v1.0
日期：2019.7
作者：01Studio
说明：RGB灯带控制。
'''

from ws2812 import WS2812
from colors import *
from machine import Pin
import pyb

#定义灯带连接引脚，Y11接口
LED = Pin('Y11',Pin.OUT,value=0)

#构建RGB灯带对象,定义控制引脚和灯珠数量
strip = WS2812(spi_bus=LED, led_count=30)

#灯带填色函数,灯珠数量为led_count
def fill_color(color):
    data=[]
    for i in range (strip.led_count):
        data.append(color)
    return data

#清空RGB灯带颜色
strip.show(fill_color(EMPTY))

while True:
    strip.show(fill_color(RED))
    pyb.delay(1000)

    strip.show(fill_color(GREEN))
    pyb.delay(1000)

    strip.show(fill_color(BLUE))
    pyb.delay(1000)

