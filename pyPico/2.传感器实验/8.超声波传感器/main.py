'''
实验名称：超声波传感器
版本：v1.0
日期：2021.1
作者：01Studio 【www.01Studio.org】
说明：通过超声波传感器测距，并在OLED上显示。
'''

#导入相关模块
from HCSR04 import HCSR04     #子文件夹下的调用方式
from machine import Pin,SoftI2C
from ssd1306 import SSD1306_I2C
import time

#初始化oled
i2c1 = SoftI2C(scl=Pin(10), sda=Pin(11))   #软件I2C初始化：scl--> 10, sda --> 11
oled = SSD1306_I2C(128, 64, i2c1, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

#初始化接口 trig=4,echo=5
trig = Pin(4,Pin.OUT)
echo = Pin(5,Pin.IN)
HC=HCSR04(trig,echo)

while True:

    oled.fill(0)  # 清屏,背景黑色
    oled.text('01Studio', 0, 0)
    oled.text('Distance test:', 0, 15)

    Distance = HC.getDistance() #测量距离

    # OLED显示距离
    oled.text(str(Distance) + ' CM', 0, 35)

    oled.show()

    #串口打印
    print(str(Distance)+' CM')

    time.sleep_ms(500) #每秒采集1次
