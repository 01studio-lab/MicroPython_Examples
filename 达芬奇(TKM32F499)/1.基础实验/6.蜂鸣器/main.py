'''
实验名称：蜂鸣器
版本：v1.0
日期：2021-4
作者：01Studio
实验平台：达芬奇
实验说明：编写实现有源蜂鸣器发出滴滴响声。
'''

from machine import Pin
import time

beep = Pin('B13', Pin.OUT) # 蜂鸣器对应引脚是13，

while True:
    
    beep.value(0)       #低电平发出响声
    time.sleep_ms(500)  #延时500毫秒
    beep.value(1)       #关闭蜂鸣器
    time.sleep_ms(500)