'''
实验名称：CAN总线通讯
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过编程实现串口通信，跟电脑串口助手实现数据收发。
'''

#导入串口模块
from pyb import CAN,Switch,delay,LED

send_flag = 0

def send():
    global send_flag

    #消除抖动，sw按下返回1，松开返回0。
    if sw.value()==1:
        delay(10)
        if sw.value()==1:

            send_flag = 1

sw = Switch()     #定义按键对象名字为sw
sw.callback(send) #当按键被按下时，执行函数send()

can=CAN(1, CAN.NORMAL) #设置CAN1为普通模式(RX-->PB8,TX-->PB9)
#设置接收相关配置 id=123, 124, 125 和 126
can.setfilter(0, CAN.LIST16, 0, (123, 124, 125, 126))

can.send('message!', 123)   #发送id=123的信息

num=0
while True:

    #判断有无收到信息
    if can.any(0):
        text=can.recv(0) #读取数据
        print(text) #通过REPL打印串口3接收的数据

    if send_flag == 1:
        can.send(str(num), 123)   #发送id=123的信息
        num=num+1
        send_flag = 0

