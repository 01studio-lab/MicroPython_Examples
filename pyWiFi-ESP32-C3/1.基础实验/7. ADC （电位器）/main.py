'''
实验名称：ADC-电压测量
版本：v1.0
日期：2021.7
作者：01Studio
说明：通过对ADC数据采集，转化成电压在显示屏上显示。ADC精度12位，电压0-1V。
'''

#导入相关模块
from machine import Pin,SoftI2C,ADC,Timer
from ssd1306 import SSD1306_I2C

#初始化相关模块
i2c = SoftI2C(sda=Pin(1), scl=Pin(0))  #I2C初始化：sda--> 1, scl --> 0
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
adc = ADC(Pin(3)) #引脚3跟pyBase的电位器相连接

def ADC_Test(tim):

	oled.fill(0)  # 清屏显示黑色背景
	oled.text('01Studio', 0, 0)  # 首行显示01Studio
	oled.text('ADC', 0, 15)      # 次行显示实验名称

	#获取ADC数值
 	oled.text(str(adc.read()),0,40)
 	oled.text('(4095)',40,40)

 	#计算电压值，获得的数据0-4095相当于0-1V，（'%.2f'%）表示保留2位小数
 	oled.text(str('%.2f'%(adc.read()/4095*1)),0,55)
  	oled.text('V',40,55)

 	oled.show()

#开启定时器0，周期300ms
tim = Timer(0)
tim.init(period=300, mode=Timer.PERIODIC, callback=ADC_Test) #周期300ms

