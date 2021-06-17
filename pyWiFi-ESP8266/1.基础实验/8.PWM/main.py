'''
实验名称：PWM
版本：v1.0
日期：2019.7
作者：01Studio
说明：通过不同频率的PWM信号输出，驱动无源蜂鸣器发出不同频率的声音。
'''

from machine import Pin, PWM
import time

Beep = PWM(Pin(15), freq=0, duty=512) # 在同一语句下创建和配置 PWM

#蜂鸣器发出频率200Hz响声
Beep.freq(200)
time.sleep_ms(1000)

#蜂鸣器发出频率400Hz响声
Beep.freq(400)
time.sleep_ms(1000)

#蜂鸣器发出频率600Hz响声
Beep.freq(600)
time.sleep_ms(1000)


#蜂鸣器发出频率800Hz响声
Beep.freq(800)
time.sleep_ms(1000)


#蜂鸣器发出频率1000Hz响声
Beep.freq(1000)
time.sleep_ms(1000)

#停止
Beep.deinit()
