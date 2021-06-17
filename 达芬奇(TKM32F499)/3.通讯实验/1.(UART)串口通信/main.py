'''
实验名称：串口通信
版本：v1.0
日期：2021.1
作者：01Studio
实验平台：达芬奇
说明：通过编程实现串口通信，跟电脑串口助手实现数据收发。
'''

#导入串口模块
from machine import UART
import time

uart=UART(2, 115200) #设置串口号1和波特率, MCU_TX--A2, MCU_RX--A3
time.sleep_ms(100) #等待串口初始化稳定
uart.write('Hello 01Studio!')#发送一条数据

while True:

    #判断有无收到信息
    if uart.any():

        text=uart.read(128) #接收128个字符
        print(text) #通过REPL打印串口3接收的数据
