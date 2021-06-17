'''
实验名称：图片缓存文件制作
版本：v1.0
日期：2021.4
作者：01Studio
社区：www.01studio.org
说明：制作缓存文件用于显示。
实验平台：01Studio-达芬奇
'''

from tftlcd import LCD43R
import time

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (0,0,0)

#############################
# 构建4.3寸RGB LCD对象并初始化
#############################
d = LCD43R(portrait=1) #默认方向,横屏 800*480

#填充白色
d.fill((255,255,255))

#制作缓存文件，使用板载Flash制作较慢，使用SD卡制作速度非常快。
d.CachePicture("/flash/picture/supper.jpg",replace=False)

d.fill((255,255,255)) #清屏用于观察

#####################
## 带计时功能的显示 ##
#####################

start=time.ticks_ms() #起始时间

#缓存文件方式显示图片，可以改成 cached=False 对比速度
d.Picture(0,0,"/flash/picture/supper.jpg", cached=True)

end=time.ticks_ms() #结束时间

print('Display total use: '+str(end-start)+' ms') #打印耗时
