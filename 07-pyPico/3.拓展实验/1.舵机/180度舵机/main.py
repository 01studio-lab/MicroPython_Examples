'''
实验名称：舵机(Servo)-180°
版本：v1.0
日期：2021.1
作者：01Studio
说明：控制舵机旋转不同角度。
'''

from machine import Pin, PWM
import time

S1 = PWM(Pin(0)) # Servo1的引脚是0
S1.freq(50) #舵机控制信号频率

'''
说明：舵机控制函数
功能：180度舵机：angle:-90至90 表示相应的角度
     360连续旋转度舵机：angle:-90至90 旋转方向和速度值。
'''
def Servo(servo,angle):
    a = int(((angle+90)*2/180+0.5)/20*65535)
    print(a)
    S1.duty_u16(a)

while True:
    
    #-90度
    Servo(S1,-90)
    time.sleep(1)

    #-45度
    Servo(S1,-45)
    time.sleep(1)

    #-0度
    Servo(S1,0)
    time.sleep(1)

    #45度
    Servo(S1,45)
    time.sleep(1)

    #90度
    Servo(S1,90)
    time.sleep(1)