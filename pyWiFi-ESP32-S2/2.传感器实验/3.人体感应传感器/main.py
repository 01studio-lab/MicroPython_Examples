'''
实验名称：人体感应传感器
版本：v1.0
日期：2021.8
作者：01Studio（www.01studio.cc）
说明：人体红外感应传感器应用
'''

import time
from machine import SoftI2C,Pin   #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C   #从ssd1306模块中导入SSD1306_I2C子模块

#pyBoard I2C初始化
i2c = SoftI2C(sda=Pin(40), scl=Pin(38))
#OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

Human=Pin(10,Pin.IN,Pin.PULL_UP) #构建人体红外对象

#OLED初始信息显示
oled.fill(0)  # 清屏背景黑色
oled.text("01Studio", 0, 0)  # 写入第1行内容
oled.text("Human body test:", 0, 15)  # 写入第2行内容
oled.show()  # OLED执行显示

def fun(Human): #Get People闪烁5次效果！

    for i in range(5):
        oled.fill(0)  # 清屏背景黑色
        oled.text("01Studio", 0, 0)  # 写入第1行内容
        oled.text("Human body test:", 0, 15)  # 写入第2行内容
        oled.text("Get People!!!", 0, 40)  # 写入第3行内容
        oled.show()  # OLED执行显示
        time.sleep_ms(500)

        oled.fill(0)  # 清屏背景黑色
        oled.text("01Studio", 0, 0)  # 写入第1行内容
        oled.text("Human body test:", 0, 15)  # 写入第2行内容
        oled.text("            ", 0, 40)  # 写入第3行内容
        oled.show()  # OLED执行显示
        time.sleep_ms(500)

Human.irq(fun,Pin.IRQ_RISING) #定义中断，上升沿触发
