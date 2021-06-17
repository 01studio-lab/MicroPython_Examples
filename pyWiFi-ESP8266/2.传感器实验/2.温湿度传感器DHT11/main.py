'''
实验名称：温湿度传感器DHT11
版本：v1.0
日期：2019.4
作者：01Studio
说明：通过编程采集温湿度数据，并在OLED上显示。。
'''

#引入相关模块
from machine import Pin,I2C,Timer
from ssd1306 import SSD1306_I2C
import dht,time

#初始化相关模块
i2c = I2C(sda=Pin(13), scl=Pin(14))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#创建DTH11对象
d = dht.DHT11(Pin(5)) #传感器连接到引脚14
time.sleep(1)   #首次启动停顿1秒让传感器稳定

def dht_get(tim):

    d.measure()         #温湿度采集

   #OLED显示温湿度
    oled.fill(0) #清屏背景黑色
    oled.text('01Studio', 0, 0)
    oled.text('DHT11 test:',0,15)
    oled.text(str(d.temperature() )+' C',0,40)   #温度显示
    oled.text(str(d.humidity())+' %',48,40)  #湿度显示
    oled.show()

#开启RTOS定时器，编号为-1
tim = Timer(-1)
tim.init(period=2000, mode=Timer.PERIODIC,callback=dht_get) #周期为2000ms
