'''
实验名称：LCD液晶显示屏
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过编程实现LCD的各种显示功能，包括画点、线、矩形、圆形、显示英文、显示图片等。
refer: https://github.com/AnthonyKNorman/MicroPython_ST7735
'''

import machine,time,lcd_gfx,st7735,time
from bmp import BMP

#初始化LCD
spi = machine.SPI(1, baudrate=8000000, polarity=0, phase=0)
d = st7735.ST7735(spi, rst=13, ce=9, dc=12)
d.reset()
d.begin()

#白色背景
d._bground = 0xffff
d.fill_screen(d._bground)

#画点,(0,0,0)表示黑色
d.pixel(5, 5, d.rgb_to_565(0,0,0))

#画线,(0,0,0)表示黑色
lcd_gfx.drawLine(5,10,80,10,d,d.rgb_to_565(0,0,0))

#画矩形,(0,0,0)表示黑色
lcd_gfx.drawRect(5,20,80,40,d,d.rgb_to_565(0,0,0))

#画圆,(0,0,0)表示黑色
lcd_gfx.drawCircle(40,90,20,d,d.rgb_to_565(0,0,0))

#写字符
d.p_string(10,130,'Hello 01Studio!',d.rgb_to_565(255,0,0))

time.sleep_ms(2000) #延时2秒

#显示图片
BMP('flower128x160.bmp',d,0,0,1)