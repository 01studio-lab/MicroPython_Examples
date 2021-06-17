#实验名称：DS18B20传感器例程
#实验平台：01Studio pyAI-K210开发板

#导入相关模块，onewire库请更新至较新版固件
from fpioa_manager import *
from micropython import const
from board import board_info
from ds18x20 import DS18X20
import time,lcd,image

lcd.init() #初始化 LCD
lcd.clear(lcd.WHITE) #清屏白色

#初始化DS18B20 GPIO
fm.register(10, fm.fpioa.GPIOHS2, force=True)
ds18b20_2 = DS18X20(fm.fpioa.GPIOHS2)
rom = ds18b20_2.scan()

while True:

    #采集温度，保留2位小数
    temp = str('%.2f'%ds18b20_2.read_temp(rom))

    #显示字符
    lcd.draw_string(90, 100, "DS18B20 Temp:",lcd.BLACK, lcd.WHITE)
    lcd.draw_string(110, 120, temp+ " C",lcd.BLACK, lcd.WHITE)

    #串口打印
    print(temp+" C")

    time.sleep_ms(1000)#每秒采集1次




