'''
实验名称：以太网MQTT通信
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过Socket编程实现以太MQTT通信  发布者（publish）。
'''

import network,usocket,time
from simple import MQTTClient
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

    #MQTT配置
    SERVER = 'mqtt.p2hp.com'
    PORT = 1883
    CLIENT_ID = '01Studio-pyBoard' # 客户端ID
    TOPIC = '/public/01Studio/1' # TOPIC名称

    client = MQTTClient(CLIENT_ID, SERVER, PORT)
    client.connect()

    while (True):

        client.publish(TOPIC, "Hello 01Studio!") #发布消息
        time.sleep_ms(1000) #延时1秒
