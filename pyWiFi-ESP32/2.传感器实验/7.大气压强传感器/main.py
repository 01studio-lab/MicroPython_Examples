'''
实验名称：大气压强传感器
版本：v1.0
日期：2019.8
作者：01Studio 【www.01Studio.org】
说明：测量BMP280温度、气压和计算海拔值，并在OLED上显示。。
'''

import bmp280
from machine import Pin,I2C,Timer
from ssd1306 import SSD1306_I2C

#初始化OLED
i2c = I2C(sda=Pin(13), scl=Pin(14))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化BMP280，定义第二个I2C接口i2c2用于连接BMP280
i2c2 = I2C(sda=Pin(16), scl=Pin(17))
BMP = bmp280.BMP280(i2c2)

#中断回调函数
def fun(tim):

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

#开启RTOS定时器
tim = Timer(-1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) #周期1s
