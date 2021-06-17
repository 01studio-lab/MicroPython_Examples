'''
实验名称：ADC-电压测量
版本：v1.0
日期：2021.1
作者：01Studio
说明：通过对ADC数据采集，转化成电压在显示屏上显示。ADC精度12位(注意返回的是0-65535)，电压0-3.3V。
'''

#导入相关模块
from machine import Pin,SoftI2C,ADC
from ssd1306 import SSD1306_I2C
import time

#初始化oled
i2c = SoftI2C(scl=Pin(10), sda=Pin(11))   #SoftI2C初始化：scl--> 10, sda --> 11
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

#初始化adc
adc = ADC(0) #Pin = 26

while True:
    
    value = adc.read_u16()
    
    oled.fill(0)  # 清屏显示黑色背景
    oled.text('01Studio', 0, 0)  # 首行显示01Studio
    oled.text('ADC', 0, 15)      # 次行显示实验名称

    #获取ADC数值
    oled.text(str(value),0,40)
    oled.text('(65535)',40,40)

    #计算电压值，获得的数据0-4095相当于0-3V，（'%.2f'%）表示保留2位小数
    oled.text(str('%.2f'%(value/65535*3.3)),0,55)
    oled.text('V',40,55)

    oled.show()
    time.sleep_ms(300)
