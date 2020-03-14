'''
实验名称：人体感应传感器
版本：v1.0
日期：2019-5-1
作者：01Studio
社区：www.01studio.org
'''

from pyb import ExtInt
from machine import I2C,Pin        #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C    #从ssd1306模块中导入SSD1306_I2C子模块

#pyBoard I2C初始化：sda--> X12, scl --> X11
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
#OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#OLED初始信息显示
oled.fill(0)  # 清屏背景黑色
oled.text("01Studio", 0, 0)  # 写入第1行内容
oled.text("Human body test:", 0, 15)  # 写入第2行内容
oled.show()  # OLED执行显示

def Display(): #Get People闪烁5次效果！

    for i in range(5):
        oled.fill(0)  # 清屏背景黑色
        oled.text("01Studio", 0, 0)  # 写入第1行内容
        oled.text("Human body test:", 0, 15)  # 写入第2行内容
        oled.text("Get People!!!", 0, 40)  # 写入第3行内容
        oled.show()  # OLED执行显示
        pyb.delay(500)

        oled.fill(0)  # 清屏背景黑色
        oled.text("01Studio", 0, 0)  # 写入第1行内容
        oled.text("Human body test:", 0, 15)  # 写入第2行内容
        oled.text("            ", 0, 40)  # 写入第3行内容
        oled.show()  # OLED执行显示
        pyb.delay(500)


callback=lambda e: Display()   #执行Display()函数
ext = ExtInt(Pin('Y11'), ExtInt.IRQ_RISING, Pin.PULL_UP, callback) #上升沿触发，打开上拉电阻
