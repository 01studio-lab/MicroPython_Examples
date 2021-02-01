'''
实验名称：以太网Socket通信
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过Socket编程实现以太网与电脑网络服务器助手建立TCP连接，相互收发数据。
'''

import network,usocket
from tftlcd import LCD43M

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

#4.3寸LCD初始化
d = LCD43M(portrait=1)
d.fill((255,255,255)) #填充白色

#socket数据接收中断标志位
socket_node = 0

#以太网初始化
nic = network.Ethernet()
nic.active(True)
nic.ifconfig('dhcp')

#判断网络是否连接成功
if nic.isconnected():

    print(nic.ifconfig()) #打印IP信息

    #显示标题
    d.printStr('01Studio Network', 40, 10, BLACK, size=4)

    #显示IP信息
    d.printStr('IP: ' + nic.ifconfig()[0], 10, 100, BLACK, size=3)
    d.printStr('Subnet: ' + nic.ifconfig()[1], 10, 150, BLACK, size=3)
    d.printStr('Gateway: ' + nic.ifconfig()[2], 10, 200, BLACK, size=3)

    #创建socket连接，TCP类型，连接成功后发送“Hello 01Studio！”给服务器。
    s=usocket.socket()
    addr=('192.168.3.14',10000) #服务器IP和端口，根据实际情况修改
    s.connect(addr)
    s.send('Hello 01Studio!')

#开启定时器，周期100ms，执行socket通信接收任务
def fun(tim):
    global socket_node
    socket_node = 1
    pyb.LED(3).toggle()

tim = pyb.Timer(1,freq=10) #周期100ms
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
