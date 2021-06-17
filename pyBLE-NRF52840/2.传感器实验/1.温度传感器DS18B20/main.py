'''
实验名称：温度传感器DS18B20
版本：v1.0
日期：2020.4
作者：01Studio
实验内容：采集温度数据并在oled上显示。
'''

#导入相关模块
import time,board,busio
from digitalio import DigitalInOut
import adafruit_ssd1306

#DS18X20库模块
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20


#构建I2C对象
i2c = busio.I2C(board.SCK, board.MOSI)

#构建oled对象,01Studio配套的OLED地址为0x3C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

#清屏
display.fill(0)
display.show()

# 初始化单总线对象，引脚为D5.
ow = OneWireBus(board.D5)

# 搜索传感器，返回第1个
ds = DS18X20(ow, ow.scan()[0])

while True:

    temp=round(ds.temperature,2) #保留2位小数

    display.fill(0) #清屏
    display.text('01Studio', 0,0, 1,font_name='font5x8.bin')
    display.text('Temp Test', 0,20, 1,font_name='font5x8.bin')
    display.text(str(temp)+' C', 0,40, 1,font_name='font5x8.bin')
    display.show()

    print(str(temp)+' C')

    time.sleep(1)
