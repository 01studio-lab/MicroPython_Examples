'''
实验名称：GPIO
版本：v1.0
日期：2019-4-1
作者：01Studio
社区：www.01studio.org
'''

from pyb import Pin

#将LED(4)-"B4"配置成推挽输出模式
p_out=Pin('B4',Pin.OUT_PP)

#将USR按键-"X17"配置为输入方式
p_in = Pin('X17', Pin.IN, Pin.PULL_UP)

while True:

    if p_in.value()==0: #USR被按下接地
        p_out.high()    #点亮LED（4）蓝灯

    else:
        p_out.low()     #关闭LED（4）蓝灯