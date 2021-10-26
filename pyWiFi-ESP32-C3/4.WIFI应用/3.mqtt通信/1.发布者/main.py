'''
实验名称：MQTT通信
版本：v1.0
日期：2021.7
作者：01Studio
说明：编程实现MQTT通信，实现发布（发送）数据。
MQTT助手：http://www.tongxinmao.com/txm/webmqtt.php#collapseOne
'''

#导入相关模块
import network,time
from simple import MQTTClient #导入MQTT板块
from machine import SoftI2C,Pin,Timer
from ssd1306 import SSD1306_I2C

#初始化OLED
i2c = SoftI2C(sda=Pin(1), scl=Pin(0))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#WIFI连接函数
def WIFI_Connect():

    WIFI_LED=Pin(2, Pin.OUT) #初始化WIFI指示灯

    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('01Studio', '88888888') #输入WIFI账号密码

        while not wlan.isconnected():

            #LED闪烁提示
            WIFI_LED.value(1)
            time.sleep_ms(300)
            WIFI_LED.value(0)
            time.sleep_ms(300)

            #超时判断,15秒没连接成功判定为超时
            if time.time()-start_time > 15 :
                print('WIFI Connected Timeout!')
                break

    if wlan.isconnected():
        #LED点亮
        WIFI_LED.value(1)

        #串口打印信息
        print('network information:', wlan.ifconfig())

        #OLED数据显示（如果没接OLED，请将下面代码屏蔽）
        oled.fill(0)   #清屏背景黑色
        oled.text('IP/Subnet/GW:',0,0)
        oled.text(wlan.ifconfig()[0], 0, 20)
        oled.text(wlan.ifconfig()[1],0,38)
        oled.text(wlan.ifconfig()[2],0,56)
        oled.show()
        return True

    else:
        return False

#发布数据任务
def MQTT_Send(tim):
    
    client.publish(TOPIC, 'Hello 01Studio!')

#执行WIFI连接函数并判断是否已经连接成功
if WIFI_Connect():

    SERVER = 'mq.tongxinmao.com'
    PORT = 18830
    CLIENT_ID = 'pyWiFi-ESP32-C3' # 客户端ID
    TOPIC = '/public/01Studio/1' # TOPIC名称
    client = MQTTClient(CLIENT_ID, SERVER, PORT)
    client.connect()

    #开启定时器，周期1000ms，执行MQTT发布
    tim = Timer(0)
    tim.init(period=1000, mode=Timer.PERIODIC,callback=MQTT_Send)
