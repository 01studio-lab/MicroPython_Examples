'''
实验名称：土壤湿度传感器
版本：v1.0
日期：2021.1
作者：01Studio 【www.01Studio.org】
说明：通过土壤湿度传感器对土壤湿度测量并显示。
'''

#导入相关模块
import time
from machine import Pin,SoftI2C,ADC
from ssd1306 import SSD1306_I2C

#初始化oled
i2c = SoftI2C(scl=Pin(10), sda=Pin(11))   #SoftI2C初始化：scl--> 10, sda --> 11
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

#初始化ADC1,Pin=27
Soil = ADC(1)

while True:

	oled.fill(0)  # 清屏显示黑色背景
	oled.text('01Studio', 0, 0)  # 首行显示01Studio
	oled.text('Soil test:', 0, 15)      # 次行显示实验名称

	value=Soil.read_u16() #获取ADC数值

    #显示数值
 	oled.text(str(value)+' (65535)',0,40)
 	#计算电压值，获得的数据0-4095相当于0-3V，（'%.2f'%）表示保留2位小数
 	oled.text(str('%.2f'%(value/65535*3.3))+' V',0,55)

	#判断土壤湿度，分3档显示。
	if 0 <= value <=19957:
		oled.text('Dry', 60, 55)

	if 19957 < value <= 35816:
		oled.text('Normal', 60, 55)

	if 35816 < value <= 65535:
		oled.text('Wet  ', 60, 55)

 	oled.show()
 	time.sleep_ms(1000)
