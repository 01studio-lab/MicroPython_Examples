# MQTT发布者（publish）例程.
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

SERVER = 'mqtt.p2hp.com'
PORT = 1883
CLIENT_ID = '01Studio-OpenMV' # 客户端ID
TOPIC = '/public/01Studio/1' # TOPIC名称

client = MQTTClient(CLIENT_ID, SERVER, PORT)
client.connect()

while (True):
    client.publish(TOPIC, "Hello 01Studio!") #发布消息
    time.sleep(1000)
