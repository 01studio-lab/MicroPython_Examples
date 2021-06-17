'''
实验名称：7寸电容触摸屏
版本：v1.0
日期：2021.4
作者：01Studio
社区：www.01studio.org
说明：电容触摸屏采集触摸信息
'''

from touch import GT911
from tftlcd import LCD7R
from machine import Pin
import time

#定义颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED=(255,0,0)
BLUE=(0,0,255)

#LCD初始化
d = LCD7R(portrait=1)
d.fill(WHITE)#填充白色

#电容触摸屏初始化，方向和LCD一致
t = GT911(portrait=1)

#配置按键
key = Pin('A0', Pin.IN, Pin.PULL_DOWN)

#清屏函数
def fun(key):

    d.fill(WHITE)
    
key.irq(fun,Pin.IRQ_RISING) #定义中断，下降沿触发

while True:

    data = t.read() #获取触摸屏坐标
    
    #当产生触摸时
    if data[0]!=2: #0：按下； 1：移动； 2：松开
        
        print(data) #REPL打印坐标信息

        #触摸坐标画圆
        d.drawCircle(data[1], data[2], 10, BLACK, fillcolor=BLACK)
        d.printStr('(X:'+str(data[1])+' Y:'+str(data[2])+')   ',10,10,RED,size=3)
    
    time.sleep_ms(20) #间隔20ms