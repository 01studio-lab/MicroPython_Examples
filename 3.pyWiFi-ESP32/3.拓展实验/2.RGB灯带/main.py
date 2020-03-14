'''
实验名称：RGB彩灯控制
版本：v1.0
日期：2019.8
作者：01Studio 【www.01Studio.org】
说明：通过编程实现灯带不同颜色的变化。
'''
import time
from machine import Pin,Timer
from neopixel import NeoPixel

#定义红、绿、蓝三种颜色
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

#22引脚连接灯带，灯珠数量30
pin = Pin(22, Pin.OUT)
np = NeoPixel(pin, 30)

#设置灯珠颜色，本实验供30个灯珠
def Color_buf(color):
    for i in range(30):
        np[i]=color

while True:

    Color_buf(RED) #红色
    np.write()     # 写入数据
    time.sleep(1)

    Color_buf(GREEN) #红色
    np.write()     # 写入数据
    time.sleep(1)

    Color_buf(BLUE) #红色
    np.write()     # 写入数据
    time.sleep(1)
