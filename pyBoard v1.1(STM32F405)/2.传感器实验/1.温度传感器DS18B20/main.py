'''
实验名称：温度传感器DS18B20
版本：v1.0
日期：2019.4
作者：01Studio
说明：通过编程采集温度数据，并在OLED上显示。。
'''

#引用相关模块
from pyb import delay
from machine import Pin,I2C
from ssd1306 import SSD1306_I2C
from onewire import OneWire
from ds18x20 import DS18X20

#初始化相关模块
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6")) # 软件模拟I2C
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化DS18B20
ow= OneWire(Pin('X11')) #使能单总线
ds = DS18X20(ow)        #传感器是DS18B20
rom = ds.scan()         #扫描单总线上的传感器地址，支持多个传感器同时连接

while True:
	
	ds.convert_temp()   #温度采集转换
	temp = ds.read_temp(rom[0]) #温度显示,rom[0]为第1个DS18B20

	#数据显示
	oled.fill(0)   #清屏背景黑色
 	oled.text('01Studio', 0, 0)
  	oled.text('Temp test:',0,20)
  	oled.text(str('%.2f'%temp)+' C',0,40) #显示temp,保留2位小数
  	oled.show()

  	delay(1000)
