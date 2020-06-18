'''
实验名称：1.8寸LCD显示（ST7735S）
版本：v1.0
日期：2020.4
作者：01Studio
说明：LCD显示实验。
'''

import board,time
import displayio
import terminalio
from adafruit_st7735r import ST7735R
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_text import label

#释放显示总线
displayio.release_displays()

#定义LCD接口，SPI
spi = board.SPI()
tft_cs = board.D11
tft_dc = board.D9
tft_rst = board.D10

#构建spi显示总线
display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)

#构建显示屏对象,默认自动刷新
display = ST7735R(display_bus, width=128, height=160,  rotation=0, bgr=True)

#设置显示元素个数，最大20个
splash = displayio.Group(max_size=20,scale=1)
display.show(splash)

########################################
# 添加元素，添加后默认自动显示
########################################

#画线
splash.append(Line(5, 10, 40, 10, 0xFFFFFF))

#画矩形
rect = Rect(5, 20, 30, 20, outline=0xFFFFFF,fill=0x0)
splash.append(rect)

#画圆
circle = Circle(20, 60, 10, fill=0x0, outline=0xFFFFFF)
splash.append(circle)

# 字符显示,使用Label对象
text_area = label.Label(terminalio.FONT, text="Hello 01Studio!", color=0xFFFFFF,x=10, y=100)
splash.append(text_area)

while True:
    pass
