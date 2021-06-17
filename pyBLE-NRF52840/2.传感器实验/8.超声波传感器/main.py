'''
实验名称：大气压强传感器BMP280
版本：v1.0
日期：2020.5
作者：01Studio（www.01studio.org）
'''

#导入相关模块
import time,board,busio
from analogio import AnalogIn
import adafruit_ssd1306,adafruit_hcsr04

#构建I2C对象
i2c = busio.I2C(board.SCK, board.MOSI)

#构建oled对象,01Studio配套的OLED地址为0x3C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

#清屏
display.fill(0)
display.show()

#构建超声波传感器对象
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.TX, echo_pin=board.RX)

while True:

    #获取距离值
    distance=sonar.distance

    #基础信息显示
    display.fill(0) #清屏
    display.text('01Studio', 0,0, 1,font_name='font5x8.bin')
    display.text('Distance Test', 0,15, 1,font_name='font5x8.bin')

    #距离信息显示
    display.text(str(round(distance,1))+' CM', 0,40, 1,font_name='font5x8.bin')
    display.show()

    print(str(round(distance,1))+' CM')

    time.sleep(0.2) #检测周期0.2秒
