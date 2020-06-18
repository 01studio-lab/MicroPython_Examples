'''
实验名称：RGB彩灯控制（NeoPixel）
版本：v1.0
日期：2020.5
作者：01Studio 【www.01Studio.org】
说明：通过编程实现灯带不同颜色的变化。
'''

import time
import board
import neopixel

#pyBLE-NRF52840板载NEOPIXEL(1个灯珠)
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2, auto_write=False)

#外接01Studio RGB灯带(30个灯珠)
#pixels = neopixel.NeoPixel(board.A2, 30, brightness=0.2, auto_write=False)

while True:

    #红色
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)

    #绿色
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(1)

    #蓝色
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(1)
