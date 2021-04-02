'''
实验名称：大气压强传感器
版本：v1.0
日期：2021.1
作者：01Studio 【www.01Studio.org】
说明：测量BMP280温度、气压和计算海拔值，并在OLED上显示。。
'''

import time,bmp280
from machine import Pin,SoftI2C
from ssd1306 import SSD1306_I2C

#初始化oled
i2c1 = SoftI2C(scl=Pin(10), sda=Pin(11))   #软件I2C初始化：scl--> 10, sda --> 11
oled = SSD1306_I2C(128, 64, i2c1, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

#初始化BMP280，软件模拟I2C
i2c2 = SoftI2C(scl=Pin(4), sda=Pin(5))   #软件I2C初始化：scl--> 4, sda --> 5
BMP = bmp280.BMP280(i2c2)

while True:

    oled.fill(0)  # 清屏,背景黑色
    oled.text('01Studio', 0, 0)
    oled.text('Air Pressure:', 0, 15)

    # 温度显示
    oled.text(str(BMP.getTemp()) + ' C', 0, 35)
    # 湿度显示
    oled.text(str(BMP.getPress()) + ' Pa', 0, 45)
    # 海拔显示
    oled.text(str(BMP.getAltitude()) + ' m', 0, 55)

    oled.show()

    time.sleep_ms(1000)  # 每隔1秒采集一次
