'''
实验名称：人体感应传感器
版本：v1.0
日期：2021.1
作者：01Studio
社区：www.01studio.org
'''
import time
from machine import SoftI2C,Pin    #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C    #从ssd1306模块中导入SSD1306_I2C子模块

#初始化oled
i2c = SoftI2C(scl=Pin(10), sda=Pin(11))   #SoftI2C初始化：scl--> 10, sda --> 11
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

#配置按键
human = Pin(27, Pin.IN, Pin.PULL_UP)

#OLED初始信息显示
oled.fill(0)  # 清屏背景黑色
oled.text("01Studio", 0, 0)  # 写入第1行内容
oled.text("Human body test:", 0, 15)  # 写入第2行内容
oled.show()  # OLED执行显示

def Display(human): #Get People闪烁5次效果！

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


human.irq(Display,Pin.IRQ_RISING) #定义中断，下降沿触发
