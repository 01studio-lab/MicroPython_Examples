'''
实验名称：光敏传感器
版本：v1.0
日期：2019.5
作者：01Studio 【www.01Studio.org】
说明：通过光敏传感器对外界环境光照强度测量并显示。
'''

#导入相关模块
import pyb
from machine import Pin,I2C
from ssd1306 import SSD1306_I2C

#初始化相关模块
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化ADC,Pin='Y11'
Light = pyb.ADC('Y11')

while True:

	oled.fill(0)  # 清屏显示黑色背景
	oled.text('01Studio', 0, 0)  # 首行显示01Studio
	oled.text('Light test:', 0, 15)      # 次行显示实验名称

	value=Light.read() #获取ADC数值

    #显示数值
 	oled.text(str(value)+' (4095)',0,40)
 	#计算电压值，获得的数据0-4095相当于0-3V，（'%.2f'%）表示保留2位小数
 	oled.text(str('%.2f'%(value/4095*3.3))+' V',0,55)

	#判断光照强度，分3档显示。
	if 0 < value <=1365:
		oled.text('Bright', 60, 55)

	if 1365 < value <= 2730:
		oled.text('Normal', 60, 55)

	if 2730 < value <= 4095:
		oled.text('Weak  ', 60, 55)

 	oled.show()
 	pyb.delay(1000)
