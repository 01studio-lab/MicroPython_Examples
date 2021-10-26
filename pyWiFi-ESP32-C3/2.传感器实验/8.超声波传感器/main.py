'''
实验名称：超声波传感器
版本：v1.0
日期：2021.7
作者：01Studio 【www.01Studio.org】
说明：通过超声波传感器测距，并在OLED上显示。
'''

#导入相关模块
from HCSR04 import HCSR04 
from machine import Pin,SoftI2C,Timer
from ssd1306 import SSD1306_I2C

#初始化OLED
i2c = SoftI2C(sda=Pin(1), scl=Pin(0))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化接口 trig=6,echo=7
trig = Pin(6,Pin.OUT)
echo = Pin(7,Pin.IN)
HC=HCSR04(trig,echo)

#中断回调函数
def fun(tim):

    oled.fill(0)  # 清屏,背景黑色
    oled.text('01Studio', 0, 0)
    oled.text('Distance test:', 0, 15)

    Distance = HC.getDistance() #测量距离

    # OLED显示距离
    oled.text(str(Distance) + ' CM', 0, 35)

    oled.show()

    #串口打印
    print(str(Distance)+' CM')

#开启定时器，周期1s
tim = Timer(0)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) 
