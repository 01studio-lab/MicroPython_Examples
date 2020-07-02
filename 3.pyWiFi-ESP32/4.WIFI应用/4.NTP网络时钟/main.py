'''
实验名称：网络时钟
版本：v1.0
日期：2020.7
作者：01Studio
'''

# 导入相关模块
from machine import Pin, I2C, RTC,Timer
from ssd1306 import SSD1306_I2C
import ntptime,network,time

# 定义星期和时间（时分秒）显示字符列表
week = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
time_list = ['', '', '']

# 初始化所有相关对象
i2c = I2C(sda=Pin(13), scl=Pin(14)) #I2C初始化：sda--> 13, scl --> 14
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
rtc = RTC()

#WIFI连接函数,连接成功后更新时间
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

        #OLED数据显示
        oled.fill(0)   #清屏背景黑色
        oled.text('IP/Subnet/GW:',0,0)
        oled.text(wlan.ifconfig()[0], 0, 20)
        oled.text(wlan.ifconfig()[1],0,38)
        oled.text(wlan.ifconfig()[2],0,56)
        oled.show()

        for i in range(5): #最多尝试获取5次时间
            try:
                ntptime.settime()
                print(rtc.datetime())
                time.sleep_ms(500)
                return None

            except:
                print("Can not get time!")

def RTC_Run(tim):

    datetime = list(rtc.datetime())  # 获取当前时间

    #北京时间，月、日、星期需要适当调整
    datetime[4]=datetime[4]+8 #北京时间，东八区
    if datetime[4] >= 24:
        datetime[4]=datetime[4]%24
        if datetime[1] in [1,3,5,7,8,10,12]: #大月
            datetime[2] = (datetime[2]+1)%32
        else: datetime[2] = (datetime[2]+1)%31
        datetime[3] = (datetime[3]+1)%8

    oled.fill(0)  # 清屏显示黑色背景
    oled.text('01Studio', 0, 0)    # 首行显示01Studio
    oled.text('NTP Clock', 0, 15)  # 次行显示实验名称

    # 显示日期，字符串可以直接用“+”来连接
    oled.text(str(datetime[0]) + '-' + str(datetime[1]) + '-' + str(datetime[2]) + ' ' + week[datetime[3]], 0, 40)

    # 显示时间需要判断时、分、秒的值否小于10，如果小于10，则在显示前面补“0”以达
    # 到较佳的显示效果
    for i in range(4, 7):
        if datetime[i] < 10:
            time_list[i - 4] = "0"
        else:
            time_list[i - 4] = ""

    # 显示时间
    oled.text(time_list[0] + str(datetime[4]) + ':' + time_list[1] + str(datetime[5]) + ':' + time_list[2] + str(datetime[6]), 0, 55)
    oled.show()


#执行WIFI连接函数
WIFI_Connect()


#开启RTOS定时器
tim = Timer(-1)
tim.init(period=300, mode=Timer.PERIODIC, callback=RTC_Run) #周期300ms
