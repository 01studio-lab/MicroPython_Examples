'''
实验名称：PWM
版本：v1.0
日期：2020.4
作者：01Studio
说明：输出PWM控制蜂鸣器发出不同频率声音
'''

#导入相关模块
import board
from pulseio import PWMOut
import time

#PWM构建，蜂鸣器引脚A4. frequency值必须大于3，否则报错
PWM = PWMOut(board.A4,  duty_cycle=32768,frequency=200,variable_frequency=True)

#循环发出不同频率响声。
while True:

    PWM.frequency = 200
    time.sleep(1)

    PWM.frequency = 400
    time.sleep(1)

    PWM.frequency = 600
    time.sleep(1)

    PWM.frequency = 800
    time.sleep(1)

    PWM.frequency = 1000
    time.sleep(1)
