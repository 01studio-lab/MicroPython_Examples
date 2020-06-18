'''
实验名称：UART(串口通讯)
版本：v1.0
日期：2020.4
作者：01Studio
'''

#导入相关模块
import board
import busio

#串口初始化
uart = busio.UART(board.TX, board.RX, baudrate=9600)

#发送数据,要求字节数组
uart.write(b'Hello 01Studio!')

while True:

    data = uart.read(64)  #最多接收64个字节

    if len(data) != 0: #有数据
        print(data)    #REPL打印
        uart.write(data) #数据回发
