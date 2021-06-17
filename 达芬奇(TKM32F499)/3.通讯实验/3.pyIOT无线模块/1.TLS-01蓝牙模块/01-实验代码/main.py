'''
实验名称：串口蓝牙模块通信（pyIOT-BLE TLS01蓝牙串口模块 by WeBee）
版本：v1.0
日期：2021.5
作者：01Studio
说明：通过编程实现蓝牙模块数据收发，并执行关键词指令，点亮LED
实验平台：01Studio-达芬奇
'''

#导入相关模块
from tls01 import TLS01
from machine import Pin
from tftlcd import LCD43R
import time

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

########################
# 构建4.3寸LCD对象并初始化
########################
d = LCD43R(portrait=1) #默认方向

#画接收框
d.fill((255,255,255))
d.printStr('BLE Message Receive', 80, 20, BLACK, size=3)
d.printStr('Receive:', 10, 100, RED, size=3)
d.drawRect(10, 150, 450, 100, BLUE, border=5) #画矩形

#构建LED4对象,蓝灯
LED = Pin('C7', Pin.OUT) 

#构建蓝牙模块对象（串口2）
BLE=TLS01(2,9600) #设置串口号3和波特率,TX--A2,RX--YA3

###############信息透传################
BLE.uart.write('Hello 01Studio!')#给手机发送一条数据

num = 0 #接收计数

#接收信息
while True:

    if BLE.uart.any(): #查询是否有信息

        text = BLE.uart.read(128) #默认单次最多接收128字节'''
        print(text)

        #接收数据LCD显示
        num =num +1
        d.printStr('Num:'+str(num), 150, 100, BLACK, size=3)
        d.printStr(str(text), 20, 180, BLACK, size=3)


        #判断关键词指令，打开或关闭LED4蓝灯
        if text == b'LEDON':
            LED.value(1)

        if text == b'LEDOFF':
            LED.value(0)
