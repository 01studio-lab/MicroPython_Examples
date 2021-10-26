'''
实验名称：RGB彩灯控制
版本：v1.0
日期：2021.7
作者：01Studio 【www.01Studio.org】
说明：通过编程实现彩灯不同颜色的变化。
'''

#导入相关模块
import time
from machine import Pin,Timer
from neopixel import NeoPixel

#定义红、绿、蓝三种颜色
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

#灯珠数量，板子1个灯珠，01Studio RGB灯带的数量为30
LED_NUM=1

#pyWiFi-ESP32-C3引脚8连接彩灯
pin = Pin(8, Pin.OUT)
np = NeoPixel(pin, LED_NUM)

#设置灯珠颜色
def Color_buf(color):
    for i in range(LED_NUM):
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
