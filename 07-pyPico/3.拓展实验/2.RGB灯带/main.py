'''
实验名称：Neopixel RGB灯带
版本：v1.0
日期：2021.3
作者：01Studio、benevpi （https://github.com/benevpi/pico_python_ws2812b）
说明：通过编程实现灯带循环显示红色（RED）、绿色（GREEN）和蓝色（BLUE）。
'''

import time
from ws2812b import ws2812b

#灯珠数量30, 控制引脚Pin27
np = ws2812b(num_leds=30, 27)

while True:
    
    #红色
    pixels.fill(255,0,0)
    pixels.show()
    time.sleep(1)

    #绿色
    pixels.fill(0,255,0)
    pixels.show()
    time.sleep(1)

    #蓝色
    pixels.fill(0,0,255)
    pixels.show()
    time.sleep(1)