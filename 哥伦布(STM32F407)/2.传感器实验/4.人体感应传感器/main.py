'''
实验名称：人体感应传感器
版本：v1.0
日期：2020.12
作者：01Studio
社区：www.01studio.org
'''

from pyb import ExtInt
from machine import Pin  #从machine模块导入Pin子模块
from tftlcd import LCD43M

#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)
RED=(255,0,0)

#初始化LCD
d=LCD43M()
d.fill(WHITE)#填充白色


def Display(ext): #Get People闪烁5次效果！

    for i in range(5):
        #显示标题
        d.printStr('Get People!!!', 80, 300, RED, size=4)
        pyb.delay(500)

        d.fill(WHITE)#填充白色
        pyb.delay(300)

ext = ExtInt(Pin('B1'), ExtInt.IRQ_RISING, Pin.PULL_UP, Display) #上升沿触发，打开上拉电阻
