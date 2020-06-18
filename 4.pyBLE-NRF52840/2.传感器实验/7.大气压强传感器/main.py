'''
实验名称：大气压强传感器BMP280
版本：v1.0
日期：2020.5
作者：01Studio（www.01studio.org）
'''

#导入相关模块
import time,board,busio
from analogio import AnalogIn
import adafruit_ssd1306,adafruit_bmp280

#构建I2C对象
i2c = busio.I2C(board.SCK, board.MOSI)
i2c2 = busio.I2C(board.TX, board.RX)

#构建oled对象,01Studio配套的OLED地址为0x3C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

#清屏
display.fill(0)
display.show()

#构建BMP280,注意01studio模块地址为0x76.
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c2,address=0x76)

# 当地海平面标准大气压
bmp280.sea_level_pressure = 1013.25


while True:

    #获取光照强度AD值
    temperature=bmp280.temperature
    pressure=bmp280.pressure
    altitude=bmp280.altitude

    #基础信息显示
    display.fill(0) #清屏
    display.text('01Studio', 0,0, 1,font_name='font5x8.bin')
    display.text('BMP280 Test', 0,15, 1,font_name='font5x8.bin')

    #电压信息显示
    display.text(str(temperature)+' C', 0,30, 1,font_name='font5x8.bin')
    display.text(str(pressure)+' hPa', 0,40, 1,font_name='font5x8.bin')
    display.text(str(altitude)+' M', 0,50, 1,font_name='font5x8.bin')
    display.show()

    time.sleep(2) #检测周期2秒
