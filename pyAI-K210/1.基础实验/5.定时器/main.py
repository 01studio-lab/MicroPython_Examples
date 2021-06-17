'''
实验名称：定时器
版本： v1.0
日期： 2019.12
作者： 01Studio
说明：通过定时器让 LED 周期性每秒闪烁 1 次
'''
from Maix import GPIO
from fpioa_manager import fm
from machine import Timer

#注册IO和构建LED对象
fm.register(12, fm.fpioa.GPIO0)
LED_B = GPIO(GPIO.GPIO0, GPIO.OUT)

#计数变量
Counter=0

#定时器回调函数
def fun(tim):
    global Counter
    Counter = Counter + 1
    print(Counter)
    LED_B.value(Counter%2)#LED循环亮灭。

#定时器0初始化，周期1秒
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=1000, callback=fun)
