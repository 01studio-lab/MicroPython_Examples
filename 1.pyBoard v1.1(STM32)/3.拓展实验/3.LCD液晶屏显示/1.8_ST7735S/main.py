'''
实验名称：LCD液晶显示屏
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过编程实现LCD的各种显示功能，包括画点、线、矩形、圆形、显示英文、显示图片等。
refer: https://github.com/AnthonyKNorman/MicroPython_ST7735
'''

import time
import lcd_gfx
from bmp import bmp
import machine
import ST7735

spi = machine.SPI(2, baudrate=8000000, polarity=0, phase=0)
d = ST7735.ST7735(spi, rst='Y4', ce='Y5', dc='Y3')
d.reset()
d.begin()
d._bground = 0xffff
d.fill_screen(d._bground)

d.set_rotation(0)
bmp('flower64x48.bmp',d,10,10,1)

d.set_rotation(1)
bmp('flower64x48.bmp',d,10,10,1)

d.set_rotation(2)
bmp('flower64x48.bmp',d,10,10,1)

d.set_rotation(3)
bmp('flower64x48.bmp',d,10,10,1)

d._color = 0
d.set_rotation(0)
d.p_string(10,10,'Hello World')

d._color = 0xf800 #红色
d.set_rotation(1)
d.p_string(10,10,'Hello World')

d._color = 0x07e0
d.set_rotation(2)
d.p_string(10,10,'Hello World')

d._color = 0x001f
d.set_rotation(3)
d.p_string(10,10,'Hello World')

time.sleep(2)
d.set_rotation(3)
bmp('flower160x128.bmp',d,0,0,1)

time.sleep(2)
lcd_gfx.drawLine(5,5,20,20,d,d.rgb_to_565(0,0,255))

x = int(d._width/2)
y = int(d._height/2)
r = int(min(x,y)/2)

d.fill_screen(d.rgb_to_565(255,255,255))
color = d.rgb_to_565(0,36,125)
lcd_gfx.drawfillCircle(x,y,r,d,color)
r = int(r*2/3)
color = d.rgb_to_565(255,255,255)
lcd_gfx.drawfillCircle(x,y,r,d,color)
r = int(r/2)
color = d.rgb_to_565(206,17,38)
lcd_gfx.drawfillCircle(x,y,r,d,color)
