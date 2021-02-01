'''
实验名称：电容触摸屏
版本：v1.0
日期：2020.12
作者：01Studio
社区：www.01studio.org
说明：电容触摸屏采集触摸信息
'''

from touch import GT1151
from tftlcd import LCD43M
from pyb import Switch
import time

#定义颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED=(255,0,0)

#LCD初始化
d = LCD43M(portrait=1)
d.fill(WHITE)#填充白色

#电容触摸屏初始化，方向和LCD一致
t = GT1151(portrait=1)

#USR按键初始化
sw = Switch()                       #定义按键对象名字为sw
sw.callback(lambda:d.fill(WHITE))   #当按键被按下时，LCD清屏白色

while True:

    data = t.read() #获取触摸屏坐标
    print(data) #REPL打印

    #当产生触摸时
    if data[0]!=2: #0：按下； 1：移动； 2：松开

        #触摸坐标画圆
        d.drawCircle(data[1], data[2], 10, BLACK, fillcolor=BLACK)
        d.printStr('(X:'+str(data[1])+' Y:'+str(data[2])+')',10,10,RED,size=3)

    time.sleep_ms(10) #触摸响应间隔
