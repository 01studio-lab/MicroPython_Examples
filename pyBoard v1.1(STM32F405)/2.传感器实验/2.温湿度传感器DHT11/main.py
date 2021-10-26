'''
实验名称：温湿度传感器实验DTH11
版本：v1.0
日期：2021.8
作者：01Studio
说明：通过编程采集温湿度数据，并在OLED上显示。。
'''

#引入相关模块
from pyb import delay
from machine import Pin,I2C
from ssd1306 import SSD1306_I2C
from dht import DHT11

#初始化相关模块
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#创建DTH11对象dt
dt=DHT11(Pin('X12'))
delay(2000)          #首次启动停顿2秒然传感器稳定

while True:

    try: #异常处理
        dt.measure()         #温湿度采集
        te=dt.temperature()  #获取温度值
        dh=dt.humidity()     #获取湿度值

        oled.fill(0) #清屏背景黑色
        oled.text('01Studio', 0, 0)
        oled.text('DHT11 test:',0,15)

        #温度显示
        oled.text(str(te)+' C',0,40)

        #湿度显示
        oled.text(str(dh)+' %',48,40)

        print('Temp is: '+str(te)+'C  '+'Humi is:'+str(dh)+'%')

        oled.show()

    except Exception as e: #异常提示

        print('Time Out!')

	delay(2000)          #每隔1秒采集一次
