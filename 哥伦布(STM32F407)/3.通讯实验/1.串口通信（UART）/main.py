'''
实验名称：串口通信
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过编程实现串口通信，跟电脑串口助手实现数据收发。
'''

#导入串口模块
from pyb import UART

uart=UART(3,115200) #设置串口号3和波特率,TX--B10,RX--B11

uart.write('Hello 01Studio!')#发送一条数据

while True:

    #判断有无收到信息
    if uart.any():
        text=uart.read(64) #默认单次最多接收64字节
        print(text) #通过REPL打印串口3接收的数据
