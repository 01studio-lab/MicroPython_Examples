'''
实验名称：温度传感器DS18B20
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过编程采集温度数据，并在LCD上显示。。
'''

#导入相关模块
import pyb
from machine import Pin
from tftlcd import LCD43M
from onewire import OneWire
from ds18x20 import DS18X20

#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)

#初始化LCD
d=LCD43M()
d.fill(WHITE)#填充白色

#初始化DS18B20
ow= OneWire(Pin('G6')) #使能单总线
ds = DS18X20(ow)        #传感器是DS18B20
rom = ds.scan()         #扫描单总线上的传感器地址，支持多个传感器同时连接

#显示标题
d.printStr('01Studio DS18B20', 40, 10, BLACK, size=4)

while True:

    ds.convert_temp()#温度采集转换
    temp = ds.read_temp(rom[0])#温度显示,rom[0]为第1个DS18B20

    #实时显示温度值
    d.printStr('Temp: '+str('%.2f'%temp)+' C',10,100,BLACK,size=4)

    pyb.delay(1000)#采集周期1秒

