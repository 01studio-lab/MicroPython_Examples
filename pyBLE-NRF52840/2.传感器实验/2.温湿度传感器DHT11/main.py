'''
实验名称：温湿度传感器DHT11
版本：v1.0
日期：2020.4
作者：01Studio
实验内容：采集温湿度数据并在oled上显示。
'''

#导入相关模块
import time,board,busio
from digitalio import DigitalInOut
import adafruit_ssd1306

#DHT库模块
import adafruit_dht


#构建I2C对象
i2c = busio.I2C(board.SCK, board.MOSI)

#构建oled对象,01Studio配套的OLED地址为0x3C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

#清屏
display.fill(0)
display.show()

# 初始化DHT11对象，引脚为D6.
dht = adafruit_dht.DHT11(board.D6)
time.sleep(1)#首次上电停顿1秒让传感器稳定

while True:

    try:
        temperature = dht.temperature #采集温度
        humidity = dht.humidity #采集湿度

        display.fill(0) #清屏
        display.text('01Studio', 0,0, 1,font_name='font5x8.bin')
        display.text('DHT11 Test', 0,20, 1,font_name='font5x8.bin')

        #显示温度数据
        display.text(str(temperature)+' C  '+str(humidity)+' %', 0,40, 1,font_name='font5x8.bin')
        display.show()

        print(str(temperature)+' C')  #REPL串口打印数据
        print(str(humidity)+' %')  #REPL串口打印数据

    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
        print("Reading from DHT failure: ", e.args)

    time.sleep(1) #采集周期2秒
