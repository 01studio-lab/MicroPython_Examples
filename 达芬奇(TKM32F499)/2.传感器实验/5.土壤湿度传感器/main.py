'''
实验名称：土壤湿度传感器
版本：v1.0
日期：2021.5
作者：01Studio 【www.01Studio.org】
实验平台：01Studio - 达芬奇
说明：通过土壤湿度传感器对土壤湿度测量并显示。
'''

#导入相关模块
from machine import Pin,ADC
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
Soil = ADC('B1')

#显示标题
d.printStr('01Studio Soil Test', 10, 10, BLUE, size=4)
while True:

    value=Soil.read_u16() #获取ADC数值

    #LCD显示
    d.printStr('Vol:'+str('%.2f'%(value/4095*3.3))+" V", 10, 100, BLACK, size=4)
    d.printStr('Value:'+str(value)+"   ", 10, 200, BLACK, size=4)
    d.printStr("(4095)", 300, 200, BLACK, size=4)

    #判断土壤湿度，分3档位显示
    if 0 <= value <=1247:
        d.printStr('Dry   ', 10, 300, BLACK, size=4)

    if 1247 < value <=2238:
        d.printStr('Normal', 10, 300, BLACK, size=4)

    if 2238 < value <=4095:
        d.printStr('Wet   ', 10, 300, BLACK, size=4)

    time.sleep(1)#延时1秒
