'''
实验名称：串口通信
版本：v1.0
日期：2021.6
作者：01Studio
说明：通过编程实现串口通信，跟电脑串口助手实现数据收发。
平台：pyWiFi-ESP32
参考：http://docs.01studio.org/esp32/quickref.html#uart-serial-bus
'''

#导入串口模块
from machine import UART

uart=UART(2,115200) #设置串口号2和波特率,TX--Y9--17,RX--Y10--16

uart.write('Hello 01Studio!')#发送一条数据

while True:

    #判断有无收到信息
    if uart.any():

        text=uart.read(128) #接收128个字符
        print(text) #通过REPL打印串口3接收的数据
