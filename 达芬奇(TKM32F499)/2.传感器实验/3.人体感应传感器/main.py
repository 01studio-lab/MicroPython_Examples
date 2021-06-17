'''
实验名称：人体感应传感器
版本：v1.0
日期：2021.5
作者：01Studio
实验平台：01Studio-达芬奇
社区：www.01studio.org
'''
import time
from machine import SoftI2C,Pin    #从machine模块导入I2C、Pin子模块
from tftlcd import LCD43R

#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)
RED=(255,0,0)

#初始化LCD
d=LCD43R()
d.fill(WHITE)#填充白色

#配置按键
human = Pin('B1', Pin.IN, Pin.PULL_UP)

def Display(human): #Get People闪烁5次效果！

    for i in range(5):
        #显示标题
        d.printStr('Get People!!!', 80, 300, RED, size=4)
        time.sleep_ms(500)

        d.fill(WHITE)#填充白色
        time.sleep_ms(500)


human.irq(Display,Pin.IRQ_RISING) #定义中断，下降沿触发
