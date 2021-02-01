'''
实验名称：舵机(Servo)-360°连续旋转
版本：v1.0
日期：2020.12
作者：01Studio
说明：360°舵机控制。
'''

#导入相关模块
from pyb import Servo,delay

s1 = Servo(1)     #构建舵机对象s1，输出引脚为PA0

#定义5组速度值,0表示停止
speed=[-100,-50,0,50,100]

i = 0  #用于选择速度

#启动时i=0，默认-100
s1.speed(speed[i])

while True:

    #指定角度
    s1.speed(speed[i])

    #5个角度循环
    i=i+1
    if i == 5:
        i=0

    delay(1000) #延时1秒
