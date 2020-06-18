'''
实验名称：土壤传感器
版本：v1.0
日期：2020.5
作者：01Studio（www.01studio.org）
'''

#导入相关模块
import time,board,busio
from analogio import AnalogIn
import adafruit_ssd1306

#构建I2C对象
i2c = busio.I2C(board.SCK, board.MOSI)

#构建oled对象,01Studio配套的OLED地址为0x3C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

#清屏
display.fill(0)
display.show()

# 初始化土壤湿度传感器对象，引脚为A3.
light = AnalogIn(board.A3)

while True:

    #获取光照强度AD值
    value=light.value

    #基础信息显示
    display.fill(0) #清屏
    display.text('01Studio', 0,0, 1,font_name='font5x8.bin')
    display.text('Soil Test', 0,15, 1,font_name='font5x8.bin')

    #电压信息显示
    display.text(str(value)+' (65535)', 0,40, 1,font_name='font5x8.bin')
    display.text(str(round(value*3.3/65535,2))+' V',0,55,1,font_name='font5x8.bin')

    #判断水位高度，分5档显示。
    if 0 <= value <=9600:
        display.text('0cm', 60, 55, 1,font_name='font5x8.bin')

    if 9600 < value <= 14400:
        display.text('1cm', 60, 55, 1,font_name='font5x8.bin')

    if 14400 < value <= 19200:
        display.text('2cm', 60, 55, 1,font_name='font5x8.bin')

    if 19200 < value <= 20800:
        display.text('3cm', 60, 55, 1,font_name='font5x8.bin')

    if 20800 < value:
        display.text('4cm', 60, 55, 1,font_name='font5x8.bin')

    display.show()

    time.sleep(0.5) #检测周期0.5秒
