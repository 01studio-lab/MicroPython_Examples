'''
实验名称：MQTT通信
版本：v1.0
日期：2021.5
作者：01Studio
说明：编程实现MQTT通信，实现发布数据。
实验平台：01Studio-达芬奇
'''

import network, time
from machine import UART, Pin, Timer
from tftlcd import LCD43R
from simple import MQTTClient

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

SERVER = 'mqtt.p2hp.com'
PORT = 1883
CLIENT_ID = '01Studio-Davinci' # 客户端ID
TOPIC = '/public/01Studio/1' # TOPIC名称
client = MQTTClient(CLIENT_ID, SERVER, PORT)
client.connect()
time.sleep(2)
client.publish(TOPIC, 'Hello 01Studio! 123567')

while True:
    
    client.publish(TOPIC, 'Hello 01Studio!')
    time.sleep(1)