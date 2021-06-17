'''
实验名称：RGB彩灯控制
版本：v1.0
日期：2019.12
作者：01Studio 【www.01Studio.org】
说明：通过编程实现灯带红、绿、蓝不同颜色的变化。
'''

from modules import ws2812
import utime

#定义红、绿、蓝三种颜色
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

#定义RGB灯带对象,引脚32连接，灯珠数量：30。
np = ws2812(32,30)

while True:

    #显示红色
    for i in range(30):
        np.set_led(i,RED)
    np.display()
    utime.sleep(1)

    #显示绿色
    for i in range(30):
        np.set_led(i,GREEN)
    np.display()
    utime.sleep(1)

    #显示蓝色
    for i in range(30):
        np.set_led(i,BLUE)
    np.display()
    utime.sleep(1)
