'''
实验名称： PWM
版本： v1.0
日期： 2019.12
作者： 01Studio
说明：通过不同频率的 PWM 信号输出，驱动无源蜂鸣器发出不同频率的声音。
'''
from machine import Timer,PWM
import time

#PWM通过定时器配置，接到IO15引脚
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
beep = PWM(tim, freq=1, duty=50, pin=15)

#循环发出不同频率响声。
while True:
    beep.freq(200)
    time.sleep(1)

    beep.freq(400)
    time.sleep(1)

    beep.freq(600)
    time.sleep(1)

    beep.freq(800)
    time.sleep(1)

    beep.freq(1000)
    time.sleep(1)
