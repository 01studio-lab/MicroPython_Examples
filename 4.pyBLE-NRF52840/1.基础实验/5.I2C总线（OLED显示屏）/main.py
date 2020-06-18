'''
实验名称：I2C总线（OLED显示屏）
版本：v1.0
日期：2020.4
作者：01Studio
实验内容：学习使用MicroPython的I2C总线通讯编程和OLED显示屏的使用。
'''

#导入相关模块
import time,board,busio
from digitalio import DigitalInOut
import adafruit_ssd1306


#构建I2C对象
i2c = busio.I2C(board.SCK, board.MOSI)

#构建oled对象,01Studio配套的OLED地址为0x3C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

#清屏
display.fill(0)
display.show()

#画点(x,y,color)
display.pixel(5, 5, 1)

#画线(x, y, width, color)
display.hline(5,10,20,1)

#画矩形(x, y, width, height, color, *, fill=False)
display.rect(5, 15, 20, 10, 1)

#画圆
display.circle(50, 15, 10, 1)

#字符
display.text("Hello 01Studio!", 5, 40, 1,font_name='font5x8.bin')

#显示
display.show()
