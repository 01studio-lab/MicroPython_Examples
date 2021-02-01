'''
实验名称：蜂鸣器
版本：v1.0
日期：2020.12
作者：01Studio
社区：www.01studio.org
说明：蜂鸣器发出滴滴滴响声
'''

from pyb import Pin
import time

#构建蜂鸣器对象
beep = Pin('F6',Pin.OUT_PP)

while True:

    #蜂鸣器发出滴滴声
    beep.low() #打开蜂鸣器
    time.sleep_ms(500) #延时500毫秒
    beep.high() #关闭蜂鸣器
    time.sleep_ms(500)
