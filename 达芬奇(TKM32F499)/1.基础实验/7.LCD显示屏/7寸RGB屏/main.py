'''
实验名称：7寸RGB液晶显示屏
版本：v1.0
日期：2021.4
作者：01Studio
社区：www.01studio.org
说明：通过编程实现LCD的各种显示功能，包括填充、画点、线、矩形、圆形、显示英文、显示图片等。
'''

from tftlcd import LCD7R
import time

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (0,0,0)

#############################
# 构建7寸RGB LCD对象并初始化
#############################
d = LCD7R(portrait=1) #默认方向,横屏 800*480

#填充白色

d.fill((255,255,255))

#画点
d.drawPixel(5, 20, RED)

#画线段
d.drawLine(5, 50, 300, 50, RED)

#画矩形
d.drawRect(5, 100, 300, 100, RED, border=5)

#画圆
d.drawCircle(150, 300, 50, RED, border=10)

#写字符,4种尺寸
d.printStr('Hello 01Studio', 400, 20, RED, size=1)
d.printStr('Hello 01Studio', 400, 100, GREEN, size=2)
d.printStr('Hello 01Studio', 400, 200, BLUE, size=3)
d.printStr('Hello 01Studio', 400, 300, BLACK, size=4)

time.sleep(3) #等待3秒

#显示图片
d.Picture(0,0,"/flash/picture/supper.jpg")
