# MQTT 订阅者（subscribe）例程.
#
#需要复制 mqtt.py 文件到OpenMV文件系统.
#
#翻译和注释：01Studio

import time, network
from mqtt import MQTTClient

SSID='01Studio' # Network SSID
KEY='88888888'  # Network key

# Init wlan module and connect to network
print("Trying to connect... (may take a while)...")

wlan = network.WINC()
wlan.connect(SSID, key=KEY, security=wlan.WPA_PSK)

# We should have a valid IP now via DHCP
print(wlan.ifconfig())

#设置MQTT回调函数,有信息时候执行
def MQTT_callback(topic, msg):
    print('topic: {}'.format(topic))
    print('msg: {}'.format(msg))

SERVER = 'mqtt.p2hp.com'
PORT = 1883
CLIENT_ID = '01Studio-OpenMV' # 客户端ID
TOPIC = '/public/01Studio/1' # TOPIC名称


client = MQTTClient(CLIENT_ID, SERVER, PORT)
client.set_callback(MQTT_callback)  #配置回调函数
client.connect()
client.subscribe(TOPIC) #订阅主题

while (True):
    client.check_msg() #检测是否收到信息，收到则执行打印。
    time.sleep(300) #设置接收间隔
