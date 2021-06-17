'''
实验名称：TCP客户端（Socket通信） 实验
版本：v1.0
日期：2021.5
作者：01Studio
实验平台：01Studio-达芬奇
说明：通过WiFi模块编程实现达芬奇的Socket通信，数据收发。
'''

import network, usocket, time
from machine import UART, Pin, Timer
from tftlcd import LCD43R

#定义颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

#LCD初始化
d = LCD43R(portrait=1)
d.fill(WHITE)

#wifi信息
SSID='01Studio' # WiFi 账号
KEY='88888888'  # WiFi 密码

###### WiFi模块初始化 ######
uart = UART(1,115200)
wlan = network.ESP8266(uart)

#socket数据接收中断标志位
socket_node = 0

WIFI_LED=Pin('C7', Pin.OUT) #初始化WIFI指示灯,LED4蓝灯

#显示标题
d.printStr('01Studio WiFi Connect:', 40, 10, BLUE, size=4)

#WIFI连接函数
def WIFI_Connect():

    
    print('Connecting to network...')#正在连接提示打印
    d.printStr('Connecting... ', 10, 100, BLACK, size=3)
    wlan.connect(SSID, KEY) #输入WIFI账号密码

    if wlan.isconnected(): #连接成功
            
        #LED点亮
        WIFI_LED.value(1)
        
        info=wlan.ifconfig()
        
        #串口打印信息
        print('IP information:')
        print(wlan.ifconfig())
        
        #;CD显示 IP 信息
        d.printStr('IP: ' + wlan.ifconfig()[0], 10, 100, BLACK, size=3)
        d.printStr('Subnet: ' + wlan.ifconfig()[1], 10, 150, BLACK, size=3)
        d.printStr('Gateway: ' + wlan.ifconfig()[2], 10, 200, BLACK, size=3)
    
    else: #连接失败
        
        print('Connect Fail!')
        d.printStr('Connect Fail!' + nic.ifconfig()[0], 10, 100, BLACK, size=3)

#执行WIFI连接函数
WIFI_Connect()

#创建socket连接，连接成功后发送“Hello 01Studio！”给服务器。
client=usocket.socket()
addr=('192.168.1.116',10000) #服务器IP和端口
client.connect(addr)
client.send('Hello 01Studio!')
client.settimeout(0.1) #必须加上

#定时器回调函数
def fun(tim):
    global socket_node
    socket_node = 1 #改变socket标志位

#构建软件定时器，编号-1
tim = Timer(-1) 
tim.init(period=100, mode=Timer.PERIODIC,callback=fun) #周期为100ms

while True:
    if socket_node:

        try:
            data = client.recv(256)
        except OSError:
            data = None

        if data:
            print("rcv:", len(data),data)

        socket_node = 0
        
    else: pass
