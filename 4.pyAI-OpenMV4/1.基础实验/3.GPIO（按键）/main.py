'''
实验名称：GPIO
版本：v1.0
日期：2019.9
作者：01Studio
社区：www.01studio.org
'''

from pyb import Pin,LED


#将KEY按键-"P9"配置为输入方式
KEY = Pin('P9', Pin.IN, Pin.PULL_UP)

while True:

    if KEY.value()==0: #按键被按下接地
        LED(3).on()    #点亮LED（3）蓝灯

    else:
        LED(3).off()     #关闭LED（3）蓝灯
