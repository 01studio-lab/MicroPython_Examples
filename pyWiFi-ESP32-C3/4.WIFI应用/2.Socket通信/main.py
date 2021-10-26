'''
实验名称：Socket通信
版本：v1.0
日期：2021.7
作者：01Studio
说明：通过Socket编程实现pyWiFi-ESP32与电脑服务器助手建立TCP连接，相互收发数据。
'''

#导入相关模块
import network,usocket,time
from machine import SoftI2C,Pin,Timer
from ssd1306 import SSD1306_I2C

#初始化OLED模块
i2c = SoftI2C(sda=Pin(1), scl=Pin(0))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#WIFI连接函数
def WIFI_Connect():

    WIFI_LED=Pin(2, Pin.OUT) #初始化WIFI指示灯

    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('Connecting to network...')
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

        #OLED数据显示
        oled.fill(0)   #清屏背景黑色
        oled.text('IP/Subnet/GW:',0,0)
        oled.text(wlan.ifconfig()[0], 0, 20)
        oled.text(wlan.ifconfig()[1],0,38)
        oled.text(wlan.ifconfig()[2],0,56)
        oled.show()
        return True

    else:
        return False


#判断WIFI是否连接成功
if WIFI_Connect():

    #创建socket连接TCP类似，连接成功后发送“Hello 01Studio！”给服务器。
    s=usocket.socket()
    addr=('192.168.1.116',10000) #服务器IP和端口
    s.connect(addr)
    s.send('Hello 01Studio!')


while True:
    
    text=s.recv(128) #单次最多接收128字节
    if text == '':
        pass

    else: #打印接收到的信息为字节，可以通过decode('utf-8')转成字符串
        print(text)
        s.send('I got:'+text.decode('utf-8'))
    
    time.sleep_ms(300)