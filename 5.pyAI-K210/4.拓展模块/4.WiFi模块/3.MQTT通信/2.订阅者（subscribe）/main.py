'''
实验名称：MQTT通信
版本：v1.0
日期：2019.8
作者：01Studio
说明：编程实现MQTT通信，实现订阅数据。
'''

import network,time
from machine import UART,Timer
from Maix import GPIO
from fpioa_manager import fm
from simple import MQTTClient

SSID='01Studio' # WiFi 账号
KEY='88888888'  # WiFi 密码


###### WiFi模块初始化 ######
#使能引脚初始化
fm.register(8, fm.fpioa.GPIOHS0, force=True)
wifi_en=GPIO(GPIO.GPIOHS0, GPIO.OUT)

#串口初始化
fm.register(7, fm.fpioa.UART2_TX, force=True)
fm.register(6, fm.fpioa.UART2_RX, force=True)
uart = UART(UART.UART2,115200,timeout=1000,read_buf_len=4096)

#WiFi使能函数
def wifi_enable(en):
    global wifi_en
    wifi_en.value(en)

def wifi_init():
    global uart
    wifi_enable(0)
    time.sleep_ms(200)
    wifi_enable(1)
    time.sleep(2)
    uart = UART(UART.UART2,115200,timeout=1000, read_buf_len=4096)
    tmp = uart.read()
    uart.write("AT+UART_CUR=921600,8,1,0,0\r\n")
    print(uart.read())
    uart = UART(UART.UART2,921600,timeout=1000, read_buf_len=10240) # important! baudrate too low or read_buf_len too small will loose data
    uart.write("AT\r\n")
    tmp = uart.read()
    print(tmp)
    if not tmp.endswith("OK\r\n"):
        print("reset fail")
        return None
    try:
        nic = network.ESP8285(uart)
    except Exception:
        return None
    return nic

############################
#########  主程序  ##########
############################

#构建WiFi对象并使能
wlan = wifi_init()

#正在连接印提示
print("Trying to connect... (may take a while)...")

#连接网络
wlan.connect(SSID,KEY)

#打印IP相关信息
print(wlan.ifconfig())

#设置MQTT回调函数,有信息时候执行
def MQTT_callback(topic, msg):
    print('topic: {}'.format(topic))
    print('msg: {}'.format(msg))

#接收数据任务
def MQTT_Rev(tim):
    try:
        client.check_msg()
    except OSError:
        pass


SERVER = 'mqtt.p2hp.com'
PORT = 1883
CLIENT_ID = '01Studio-ESP32' # 客户端ID
TOPIC = '/public/01Studio/1' # TOPIC名称

client = MQTTClient(CLIENT_ID, SERVER, PORT) #建立客户端对象
client.set_callback(MQTT_callback)  #配置回调函数
client.connect()
client.subscribe(TOPIC) #订阅主题

#定时器0初始化，周期300ms，执行MQTT通信接收任务
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC,
            period=300, callback=MQTT_Rev)

while True:
    pass
