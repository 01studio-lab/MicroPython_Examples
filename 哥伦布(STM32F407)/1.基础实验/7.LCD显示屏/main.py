'''
实验名称：4.3寸LCD液晶显示屏
版本：v1.0
日期：2020.12
作者：01Studio
社区：www.01studio.org
说明：通过编程实现LCD的各种显示功能，包括填充、画点、线、矩形、圆形、显示英文、显示图片等。
'''


from tftlcd import LCD43M
import time

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)

########################
# 构建4.3寸LCD对象并初始化
########################
d = LCD43M(portrait=1) #默认方向

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
d.printStr('Hello 01Studio', 10, 400, RED, size=1)
d.printStr('Hello 01Studio', 10, 500, GREEN, size=2)
d.printStr('Hello 01Studio', 10, 600, BLUE, size=3)
d.printStr('Hello 01Studio', 10, 700, BLACK, size=4)

time.sleep(5) #等待5秒

#显示图片
d.Picture(0,0,"/flash/picture/01studio.jpg")
time.sleep(3)
d.Picture(0,0,"/flash/picture/COLUMBUS.jpg")


