'''
实验名称：按键
版本：v1.0
日期：2021.7
作者：01Studio
说明：通过按键改变LED的亮灭状态
'''
from machine import Pin
import time

LED=Pin(2,Pin.OUT) #构建LED对象,开始熄灭
KEY=Pin(9,Pin.IN,Pin.PULL_UP) #构建KEY对象
state=0 #LED引脚状态

while True:
    if KEY.value()==0:   #按键被按下
        time.sleep_ms(10) #消除抖动
        if KEY.value()==0: #确认按键被按下
            state=not state  #使用not语句而非~语句
            LED.value(state) #LED状态翻转
            print('KEY')
            while not KEY.value(): #检测按键是否松开
                pass