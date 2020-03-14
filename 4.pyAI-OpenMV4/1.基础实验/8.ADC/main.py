'''
实验名称：ADC-电压测量
版本：v1.0
日期：2019.9
作者：01Studio
说明：通过对ADC数据采集，转化成电压在显示屏上显示。ADC精度12位，电压0-3.3V。
'''

#导入相关模块
import pyb,utime
from machine import Pin,I2C
from ssd1306x import SSD1306_I2C

#初始化相关模块
i2c = I2C(sda=Pin("P0"), scl=Pin("P2"),freq=80000)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
adc = pyb.ADC('P6') #Pin='P6'

while True:

    oled.fill(0)  # 清屏显示黑色背景
    oled.text('01Studio', 0, 0)  # 首行显示01Studio
    oled.text('ADC', 0, 15)      # 次行显示实验名称

    #获取ADC数值
    oled.text(str(adc.read()),0,40)
    oled.text('(4095)',40,40)

    #计算电压值，获得的数据0-4095相当于0-3.3V，（'%.2f'%）表示保留2位小数
    oled.text(str('%.2f'%(adc.read()/4095*3.3)),0,55)
    oled.text('V',40,55)

    oled.show()
    utime.sleep(1) #延时1秒
