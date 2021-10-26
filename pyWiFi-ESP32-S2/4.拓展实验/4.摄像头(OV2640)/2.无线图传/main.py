'''
实验名称：OV2640无线图传
版本：v1.0
日期：2021.8
作者：01Studio
说明：编程实现录拍摄图片并保存。
'''

from machine import Pin
from tftlcd import LCD32
import network,sensor,time


#摄像头初始化，约3~5秒
cam = sensor.OV2640()
cam.reset()
cam.set_framesize(sensor.QVGA) #320*240分辨率

#定义常用颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

########################
# 构建3.2寸LCD对象并初始化
########################
d = LCD32(portrait=1) #默认方向竖屏

#填充白色
d.fill(WHITE)


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
        
        #LCD显示IP信息
        d.printStr('Network:', 10, 10, RED, size=2)
        d.printStr('IP: ' + wlan.ifconfig()[0], 10, 50, BLACK, size=1)
        d.printStr('Subnet: ' + wlan.ifconfig()[1], 10, 90, BLACK, size=1)
        d.printStr('Gateway: ' + wlan.ifconfig()[2], 10, 130, BLACK, size=1)
        
        return True #连接成功

#执行WIFI连接函数
if WIFI_Connect(): #连接成功

    cam.stream() #进入图传