'''
实验名称：LCD液晶显示屏
版本：v1.0
日期：2019.7
作者：01Studio
说明：通过编程实现LCD的各种显示功能，包括画点、线、矩形、圆形、显示英文、显示图片等。
'''

from lcd import *
from fonts.arial_14 import Arial_14

starttime = pyb.micros()//1000 #测试刷屏起始时间

########################
    #构建对象并初始化#
########################

#构建LCD对象
d = LCD() # or d = LCD(portrait=False) for landscape

#构建字符对象
c = d.initCh(color=BLACK, bgcolor=WHITE, font=Arial_14)

########################
    #函数使用方法#
########################

#填充
d.fillMonocolor(WHITE)

#画点
d.drawPixel(5, 5, RED, pixels=4)

#画垂直线
d.drawVline(5, 10, 10, RED, width=1)

#画水平线
d.drawHline(5, 25, 30, RED, width=1)

#画线段
d.drawLine(5, 30, 25, 50, RED)

#画矩形
d.drawRect(5, 60, 30, 20, RED, border=1)

#画圆
d.drawCircle(30, 120, 20, RED, border=1, degrees=360, startangle=0)

#写字符
c.printChar('@', 20, 160)

#写字符串行
c.printLn('Hello 01Studio', 20, 200)

pyb.delay(3000) #延时3秒方便观察

#显示图片
d.renderBmp("01Studio.bmp", (0, 0))

# 测试刷屏速度(减去3000ms延时)
print('executed in:', (pyb.micros()//1000-starttime-3000)/1000, 'seconds')
