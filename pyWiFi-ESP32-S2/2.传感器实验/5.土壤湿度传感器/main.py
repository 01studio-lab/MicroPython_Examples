'''
实验名称：土壤湿度传感器
版本：v1.0
日期：2021.8
作者：01Studio 【www.01Studio.cc】
说明：通过土壤湿度传感器对土壤湿度测量并显示。
'''

#导入相关模块

from machine import Pin,I2C,ADC,Timer
from ssd1306 import SSD1306_I2C

#初始化相关模块
i2c = I2C(sda=Pin(40), scl=Pin(38))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化ADC,Pin是10，开启11DB衰减，量程增至0-3.3V
Soil = ADC(Pin(10))
Soil.atten(ADC.ATTN_11DB)


#中断回调函数
def fun(tim):


	oled.fill(0)  # 清屏显示黑色背景
	oled.text('01Studio', 0, 0)  # 首行显示01Studio
	oled.text('Soil test:', 0, 15)      # 次行显示实验名称

	value=Soil.read() #获取ADC数值

    #显示数值
 	oled.text(str(value)+' (8191)',0,40)
 	#计算电压值，获得的数据0-4095相当于0-3.3V，（'%.2f'%）表示保留2位小数
 	oled.text(str('%.2f'%(value/8191*3.3))+' V',0,55)

	#判断土壤湿度，分3档显示。
	if 0 <= value <=2494:
		oled.text('Dry', 60, 55)

	if 2494 < value <= 4476:
		oled.text('Normal', 60, 55)

	if 4476 < value <= 8191:
		oled.text('Wet  ', 60, 55)

 	oled.show()

#开启RTOS定时器
tim = Timer(-1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) #周期1s
