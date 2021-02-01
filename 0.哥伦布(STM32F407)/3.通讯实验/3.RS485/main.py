'''
实验名称：RS485通讯
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过编程实现串口通信，跟电脑串口助手实现数据收发。
'''

#导入串口模块
from pyb import UART,Pin,Switch,delay

send_flag = 0

def send():
    global send_flag

    #消除按键抖动
    if sw.value()==1:
        delay(10)
        if sw.value()==1:
            send_flag = 1

sw = Switch()     #定义按键对象名字为sw
sw.callback(send) #当按键被按下时，执行函数send()

uart=UART(2,115200) #设置串口号2和波特率
RS485_EN = Pin('G8', Pin.OUT_PP) #初始化控制引脚

RS485_EN.high() #拉高进入发送模式
uart.write('Hello 01Studio!')#发送一条数据
RS485_EN.low() #拉低进入接收模式

while True:

    #判断有无收到信息
    if uart.any():
        text=uart.read(64) #默认单次最多接收64字节
        print(text) #通过REPL打印串口3接收的数据

    if send_flag ==1 :
        RS485_EN.high() #拉高进入发送模式
        uart.write('Hello 01Studio!')#发送一条数据
        RS485_EN.low() #拉低进入接收模式
        send_flag = 0
