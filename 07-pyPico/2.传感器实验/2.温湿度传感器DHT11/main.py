'''
实验名称：温湿度传感器实验DTH11
版本：v1.0
日期：2021.1
作者：ikornaselur  (https://github.com/ikornaselur/pico-dht11)
翻译和注释：通过编程采集温湿度数据，并在OLED上显示。。
'''

#引入相关模块
from machine import Pin,SoftI2C
from ssd1306 import SSD1306_I2C
from dht import DHT11, InvalidChecksum
import time

#初始化oled
i2c = SoftI2C(scl=Pin(10), sda=Pin(11))   #pyPico I2C初始化：scl--> 10, sda --> 11
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c


# 延时1秒等待DHT11稳定
time.sleep(1)

#创建DTH11对象dt
dt = DHT11(machine.Pin(17))

while True:
    
    te=dt.temperature  #获取温度值
    dh=dt.humidity    #获取湿度值
    
    oled.fill(0) #清屏背景黑色
    oled.text('01Studio', 0, 0)
    oled.text('DHT11 test:',0,15)

    #温度显示
    oled.text(str(te)+' C',0,40)

    #湿度显示
    oled.text(str(dh)+' %',55,40)

    oled.show()
    
    time.sleep_ms(2000)          #每隔2秒采集一次
