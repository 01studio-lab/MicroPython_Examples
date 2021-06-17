'''
实验名称：RGB灯圈
版本：v1.0
日期：2020.12
作者：01Studio
说明：Neopixel WS2812 RGB灯带控制。
'''

import neopixel,time
from machine import Pin

#定义红、绿、蓝三种颜色
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

#灯带初始化，PB1引脚，灯珠数量30。
np = neopixel.NeoPixel(Pin('B1', machine.Pin.OUT), n=16)

while True:

    np.fill(RED)   #红色
    np.write()     # 写入数据
    time.sleep(1)

    np.fill(GREEN) #绿色
    np.write()     # 写入数据
    time.sleep(1)

    np.fill(BLUE)  #蓝色
    np.write()     # 写入数据
    time.sleep(1)

    for i in range (16):

        np[i]=RED
        np.write()
        time.sleep_ms(100)
