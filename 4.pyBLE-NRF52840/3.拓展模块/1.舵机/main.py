'''
实验名称：舵机控制
版本：v1.0
日期：2020.5
作者：01Studio 【www.01Studio.org】
说明：通过编程控制180°舵机旋转到不同角度（360°连续旋转舵机表现为不同旋转方向和速度）
'''

import time,board,pulseio
from adafruit_motor import servo

#构建PWM对象，A0引脚。
pwm = pulseio.PWMOut(board.A0, duty_cycle=2 ** 15, frequency=50)

#构建Servo对象Servo1。参数适用于SG90舵机
Servo1 = servo.Servo(pwm,min_pulse=500, max_pulse=2500)

#180°舵机表现为旋转到不同角度；360°连续旋转舵机表现为不同旋转方向和速度
while True:

    Servo1.angle = 0
    time.sleep(1)

    Servo1.angle = 45
    time.sleep(1)

    Servo1.angle = 90
    time.sleep(1)

    Servo1.angle = 135
    time.sleep(1)

    Servo1.angle =180
    time.sleep(1)
