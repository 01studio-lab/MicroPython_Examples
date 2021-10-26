'''
实验名称：电阻触摸屏
版本：v1.0
日期：2021.8
作者：01Studio
实验平台：pyWiFi-ESP32-S2P
说明：电阻触摸屏采集触摸信息
'''

from touch import XPT2046
from tftlcd import LCD32
from machine import Pin
import time

#定义颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED=(255,0,0)

#LCD初始化
d = LCD32(portrait=1) #默认竖屏
d.fill(WHITE) #填充白色

#电阻触摸屏初始化，方向和LCD一致
t = XPT2046(portrait=1)

def fun(KEY):
    
    d.fill(WHITE) #清屏
    
#USR按键初始化
KEY=Pin(0,Pin.IN,Pin.PULL_UP) #构建KEY对象
KEY.irq(fun,Pin.IRQ_FALLING) #定义中断，下降沿触发

while True:

    data = t.read() #获取触摸屏坐标
    print(data) #REPL打印

    #当产生触摸时
    if data[0]!=2: #0：按下； 1：移动； 2：松开

        #触摸坐标画圆
        d.drawCircle(data[1], data[2], 5, BLACK, fillcolor=BLACK)
        d.printStr('(X:'+str('%03d'%data[1])+' Y:'+str('%03d'%data[2])+')',10,10,RED,size=1)

    time.sleep_ms(20) #触摸响应间隔
