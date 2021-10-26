'''
实验名称：舵机控制
版本：v1.0
日期：2021.8
作者：01Studio 【www.01Studio.cc】
说明：通过编程控制舵机旋转到不同角度
'''

from machine import Pin, PWM
import time

S1 = PWM(Pin(0), freq=50, duty=0) # Servo1的引脚是0

'''
说明：舵机控制函数
功能：180度舵机：angle:-90至90 表示相应的角度
     360连续旋转度舵机：angle:-90至90 旋转方向和速度值。
'''
def Servo(servo,angle):
    S1.duty(int(((angle+90)*2/180+0.5)/20*1023))

#-90度
Servo(S1,-90)
time.sleep(1)

#-90度
Servo(S1,-45)
time.sleep(1)

#-90度
Servo(S1,0)
time.sleep(1)

#-90度
Servo(S1,45)
time.sleep(1)

#-90度
Servo(S1,90)
time.sleep(1)