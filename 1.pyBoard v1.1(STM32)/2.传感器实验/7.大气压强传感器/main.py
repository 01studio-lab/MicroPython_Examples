'''
实验名称：大气压强传感器
版本：v1.0
日期：2019.5.1
作者：01Studio 【www.01Studio.org】
说明：测量BMP280温度、气压和计算海拔值，并在OLED上显示。。
'''

import pyb
import bmp280
from machine import Pin,I2C
from ssd1306 import SSD1306_I2C

#初始化OLED
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化BMP280，I2C接口2
BMP = bmp280.BMP280(I2C(2))

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

    pyb.delay(1000)  # 每隔1秒采集一次
