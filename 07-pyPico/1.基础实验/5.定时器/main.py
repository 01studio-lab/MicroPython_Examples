'''
实验名称：定时器
版本：v1.0
日期：2021.1
作者：01Studio
说明：通过定时器让LED周期性每秒闪烁1次
'''
from machine import Pin,Timer

led=Pin(25, Pin.OUT)

def fun(tim):

    led.toggle()

#构建定时器
tim = Timer()
tim.init(period=1000, mode=Timer.PERIODIC,callback=fun) #周期为1000ms
