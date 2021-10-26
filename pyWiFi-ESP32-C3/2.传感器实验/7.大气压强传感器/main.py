'''
实验名称：大气压强传感器
版本：v1.0
日期：2021.7
作者：01Studio 【www.01Studio.org】
说明：测量BMP280温度、气压和计算海拔值，并在OLED上显示。
'''

#导入相关模块
import bmp280
from machine import Pin,SoftI2C,Timer
from ssd1306 import SSD1306_I2C

#初始化OLED模块
i2c = SoftI2C(sda=Pin(1), scl=Pin(0))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化BMP280，I2C连接
i2c2 = SoftI2C(sda=Pin(7), scl=Pin(6))
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

#开启定时器,周期1s
tim = Timer(0)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) 
