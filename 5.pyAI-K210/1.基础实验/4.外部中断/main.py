'''
实验名称：外部中断
版本： v1.0
日期： 2019.12
作者： 01Studio
说明：通过按键改变 LED 的亮灭状态（外部中断方式）
'''

from Maix import GPIO
from fpioa_manager import fm
import utime

#注册IO，注意高速GPIO口才有中断
fm.register(12, fm.fpioa.GPIO0)
fm.register(16, fm.fpioa.GPIOHS0)

#构建lED和KEY对象
LED_B=GPIO(GPIO.GPIO0,GPIO.OUT,value=1)
KEY=GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)

#LED状态表示
state = 1

#中断回调函数
def fun(KEY):
    global state
    utime.sleep_ms(10) #消除抖动
    if KEY.value()==0: #确认按键被按下
        state = not state
        LED_B.value(state)

#开启中断，下降沿触发
KEY.irq(fun, GPIO.IRQ_FALLING)
