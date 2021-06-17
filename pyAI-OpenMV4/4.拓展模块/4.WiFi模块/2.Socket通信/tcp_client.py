# TCP客户端（Socket通信） 实验
#
# 通过WiFi模块编程实现OpenMV的Socket通信，数据收发.
#
#作者：01Studio

import network, usocket,pyb

# WiFi信息
SSID='01Studio' # Network SSID
KEY='88888888'  # Network key

#socket数据接收中断标志位
socket_node = 0

# Init wlan module and connect to network
print("Trying to connect... (may take a while)...")

wlan = network.WINC()
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)

# We should have a valid IP now via DHCP
print(wlan.ifconfig())

#创建socket连接，连接成功后发送“Hello 01Studio！”给服务器。
client=usocket.socket()
addr=('192.168.1.116',10000) #服务器IP和端口
client.connect(addr)
client.send('Hello 01Studio!')

#开启定时器，周期100ms,重复执行socket通信接收任务
def fun(tim):
    global socket_node
    socket_node = 1
    pyb.LED(3).toggle()

tim = pyb.Timer(4,freq=10)
tim.callback(fun)


while True:
    if socket_node:
        text=client.recv(128) #单次最多接收128字节
        if text == '':
            pass

        else: #打印接收到的信息为字节，可以通过decode('utf-8')转成字符串
            print(text)
            client.send('I got:'+text.decode('utf-8'))

        socket_node=0

