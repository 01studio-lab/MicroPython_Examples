'''
实验名称：定时器
版本：v1.0
日期：2021.1
作者：01Studio
实验平台：达芬奇
说明：通过定时器让LED周期性每秒闪烁1次
'''
from machine import Pin,Timer

#蓝灯
led=Pin('C7', Pin.OUT)

state=0 #LED引脚状态

#LED 状态翻转函数
def fun(tim):

    global state
    state = not state
    led.value(state)
    
#构建定时器，编号1-10共10个硬件定时器可用
tim = Timer(1) 
tim.init(period=1000, mode=Timer.PERIODIC,callback=fun) #周期为1000ms