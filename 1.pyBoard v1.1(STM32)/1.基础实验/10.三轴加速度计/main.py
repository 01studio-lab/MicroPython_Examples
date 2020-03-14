'''
实验名称：三轴加速度计
版本：v1.0
日期：2019.4
作者：01Studio
说明：通过编程获取其各个方向的数值（X轴、Y轴、Z轴）并在OLED上显示。
'''

import pyb
from machine import Pin,I2C
from ssd1306 import SSD1306_I2C

#初始化相关模块
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

accel = pyb.Accel()

while True:

	oled.fill(0) #清屏
	oled.text('01Studio', 0, 0)
	oled.text('Accel test:',0,15)

	#获取x,y,z的值并显示
	oled.text('X:'+str(accel.x()),0,40)
	oled.text('Y:'+str(accel.y()),44,40)
	oled.text('Z:'+str(accel.z()),88,40)
	oled.show()

	pyb.delay(1000) #延时1s
