'''
实验名称：大气压强传感器
版本：v1.0
日期：2020.12
作者：01Studio 【www.01Studio.org】
说明：测量BMP280温度、气压和计算海拔值，并在OLED上显示。。
'''

#导入相关模块
import pyb,bmp280
from machine import Pin,I2C
from tftlcd import LCD43M

#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)

#初始化LCD
d=LCD43M()
d.fill(WHITE)#填充白色

#初始化BMP280，I2C接口2
BMP = bmp280.BMP280(I2C(2))

#显示标题
d.printStr('01Studio BMP280', 40, 10, BLACK, size=4)

while True:

    #采集温度、压强、高度信息数据并用LCD显示：
    d.printStr('Temp: ' + str(BMP.getTemp()) + ' C', 10, 100, BLACK, size=4)
    d.printStr('Press: ' + str(BMP.getPress()) + ' Pa', 10, 200, BLACK, size=4)
    d.printStr('Altitude: ' + str(BMP.getAltitude()) + ' M', 10, 300, BLACK, size=4)

    pyb.delay(1000) #延时1秒
