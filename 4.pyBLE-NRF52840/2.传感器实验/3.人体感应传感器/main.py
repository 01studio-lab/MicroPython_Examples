'''
实验名称：人体感应传感器
版本：v1.0
日期：2020.5
作者：01Studio（www.01studio.org）
说明：人体红外感应传感器应用
'''

#导入相关模块
import time,board,busio
from digitalio import DigitalInOut, Direction, Pull
import adafruit_ssd1306


#构建I2C对象
i2c = busio.I2C(board.SCK, board.MOSI)

#构建oled对象,01Studio配套的OLED地址为0x3C
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

#清屏
display.fill(0)
display.show()

# 初始化人体红外传感器对象，引脚为D6.
human = DigitalInOut(board.A2) #定义引脚编号
human.direction = Direction.INPUT #IO为输入
human.pull = Pull.UP #打开上拉电阻

while True:

    if human.value == 1: #有人
        #OLED显示有人Got People
        display.fill(0) #清屏
        display.text('01Studio', 0,0, 1,font_name='font5x8.bin')
        display.text('Human Test', 0,20, 1,font_name='font5x8.bin')
        display.text('Got People!', 0,40, 1,font_name='font5x8.bin')
        display.show()

    else:
        #OLED显示没人No People
        display.fill(0) #清屏
        display.text('01Studio', 0,0, 1,font_name='font5x8.bin')
        display.text('Human Test', 0,20, 1,font_name='font5x8.bin')
        display.text('No People.', 0,40, 1,font_name='font5x8.bin')
        display.show()

    time.sleep(0.5) #检测周期0.5秒
