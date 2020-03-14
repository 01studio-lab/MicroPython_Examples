'''
实验名称：超声波传感器
版本：v1.0
日期：2019.5.1
作者：01Studio 【www.01Studio.org】
说明：通过超声波传感器测距，并在OLED上显示。
'''

from HCSR04 import HCSR04     #子文件夹下的调用方式
from pyb import Pin,delay
from machine import Pin,I2C
from ssd1306 import SSD1306_I2C

#初始化OLED
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化接口 trig='Y9',echo='Y10'
trig = Pin('Y9',Pin.OUT_PP)
echo = Pin('Y10',Pin.IN)
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

    delay(1000) #每秒采集1次
