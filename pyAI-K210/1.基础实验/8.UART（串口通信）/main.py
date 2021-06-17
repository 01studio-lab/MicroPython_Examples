'''
实验名称：串口通信
版本： v1.0
日期： 2019.12
作者： 01Studio
说明：通过编程实现串口通信，跟电脑串口助手实现数据收发。
'''

from machine import UART,Timer
from fpioa_manager import fm

#映射串口引脚
fm.register(6, fm.fpioa.UART1_RX, force=True)
fm.register(7, fm.fpioa.UART1_TX, force=True)

#初始化串口
uart = UART(UART.UART1, 115200, read_buf_len=4096)
uart.write('Hello 01Studio!')


while True:

    text=uart.read() #读取数据

    if text: #如果读取到了数据
        print(text.decode('utf-8')) #REPL打印
        uart.write('I got'+text.decode('utf-8')) #数据回传
