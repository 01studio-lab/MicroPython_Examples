'''
实验名称：W5500以太网模块Socket通信
版本：v1.0
日期：2019.11
作者：01Studio
说明：通过Socket编程实现pyBoard+W5500以太网模块与电脑服务器助手建立TCP连接，相互收发数据。
'''

import network,usocket,pyb
from machine import I2C,Pin
from ssd1306 import SSD1306_I2C

#初始化相关模块
i2c = I2C(sda=Pin('Y10'), scl=Pin('Y9'))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#socket数据接收中断标志位
socket_node = 0

#初始化以太网模块
nic = network.WIZNET5K(pyb.SPI(2), pyb.Pin.board.Y5, pyb.Pin.board.Y4)
nic.active(True)
nic.ifconfig('dhcp')

#判断网络是否连接成功
if nic.isconnected():

    print(nic.ifconfig()) #打印IP信息
    #OLED数据显示
    oled.fill(0)   #清屏背景黑色
    oled.text('IP/Subnet/GW:',0,0)
    oled.text(nic.ifconfig()[0], 0, 20)
    oled.text(nic.ifconfig()[1],0,38)
    oled.text(nic.ifconfig()[2],0,56)
    oled.show()

    #创建socket连接TCP类似，连接成功后发送“Hello 01Studio！”给服务器。
    s=usocket.socket()
    addr=('192.168.1.116',10000) #服务器IP和端口
    s.connect(addr)
    s.send('Hello 01Studio!')

#开启RTOS定时器，编号为-1,周期100ms，执行socket通信接收任务
def fun(tim):
    global socket_node
    socket_node = 1
    pyb.LED(3).toggle()

tim = pyb.Timer(1,freq=10)
tim.callback(fun)

while True:
    if socket_node:
        text=s.recv(128) #单次最多接收128字节
        if text == '':
            pass

        else: #打印接收到的信息为字节，可以通过decode('utf-8')转成字符串
            print(text)
            s.send('I got:'+text.decode('utf-8'))

        socket_node=0
