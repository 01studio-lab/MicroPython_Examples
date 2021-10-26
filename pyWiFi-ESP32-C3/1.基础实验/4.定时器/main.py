'''
实验名称：定时器
版本：v1.0
日期：2021.7
作者：01Studio
说明：通过定时器让LED周期性每秒闪烁1次
'''
from machine import Pin,Timer

led=Pin(2,Pin.OUT)
Counter = 0
Fun_Num = 0

def fun(tim):

    global Counter
    Counter = Counter + 1
    print(Counter)
    led.value(Counter%2)

#使用定时器0，周期为1秒
tim = Timer(0)
tim.init(period=1000, mode=Timer.PERIODIC,callback=fun) #周期为1000ms
