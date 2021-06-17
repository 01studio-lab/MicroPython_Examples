'''
实验名称：水位传感器
版本：v1.0
日期：2021.5
作者：01Studio 【www.01Studio.org】
开发平台：01Studio 达芬奇
说明：通过水位传感器对水位测量并显示。
'''

#导入相关模块
from machine import Pin, ADC
from tftlcd import LCD43R
import time

#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)
BLUE=(0,0,255)

#初始化LCD
d=LCD43R()
d.fill(WHITE)#填充白色

#初始化ADC
Water_level = ADC('B1')

#显示标题
d.printStr('01Studio Water Level Test', 10, 10, BLUE, size=4)

while True:

    value=Water_level.read_u16() #获取ADC数值

    #LCD显示
    d.printStr('Vol:'+str('%.2f'%(value/4095*3.3))+" V", 10, 100, BLACK, size=4)
    d.printStr('Value:'+str(value)+"   ", 10, 200, BLACK, size=4)
    d.printStr("(4095)", 300, 200, BLACK, size=4)

    #判断水位，分5档
    if 0 <= value <=600:
        d.printStr('0cm', 10, 300, BLACK, size=4)

    if 600 < value <=900:
        d.printStr('1cm', 10, 300, BLACK, size=4)

    if 900 < value <=1200:
        d.printStr('2cm', 10, 300, BLACK, size=4)

    if 1200 < value <=1300:
        d.printStr('3cm   ', 10, 300, BLACK, size=4)

    if 1300 < value:
        d.printStr('4cm   ', 10, 300, BLACK, size=4)

    time.sleep(1)#延时1秒
