'''
实验名称：2.4寸LCD液晶显示屏
版本：v1.0
日期：2021.9
作者：01Studio
实验平台：pyWiFi-ESP32-S2P
说明：通过编程实现LCD的各种显示功能，包括填充、画点、线、矩形、圆形、显示英文、显示图片等。
'''

#导入相关模块
from tftlcd import LCD24
import time

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

########################
# 构建2.4寸LCD对象并初始化
########################
d = LCD24(portrait=1) #默认方向竖屏

#填充白色
d.fill(WHITE)

#画点
d.drawPixel(5, 5, RED)
 
#画线段
d.drawLine(5, 10, 200, 10, RED)
 
#画矩形
d.drawRect(5, 30, 200, 40, RED, border=5)

#画圆
d.drawCircle(100, 120, 30, RED, border=5)
 
#写字符,4种尺寸
d.printStr('Hello 01Studio', 10, 200, RED, size=1)
d.printStr('Hello 01Studio', 10, 230, GREEN, size=2)
d.printStr('Hello 01Studio', 10, 270, BLUE, size=3)

time.sleep(5) #等待5秒

#显示图片
d.Picture(0,0,"/picture/1.jpg")
time.sleep(3)
d.Picture(0,0,"/picture/2.jpg")
time.sleep(3)
d.Picture(0,0,"/picture/01studio.jpg")
