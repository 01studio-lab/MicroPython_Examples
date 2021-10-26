'''
实验名称：I2C总线(OLED显示屏)
版本：v1.0
日期：2021.7
作者：01Studio
'''


from machine import SoftI2C,Pin #从machine模块导入I2C、Pin子模块
from ssd1306 import SSD1306_I2C #从ssd1306模块中导入SSD1306_I2C子模块

i2c = SoftI2C(sda=Pin(1), scl=Pin(0))   #I2C初始化：sda--> 1, scl --> 0
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c) #OLED显示屏初始化：128*64分辨率,OLED的I2C地址是0x3c

oled.text("Hello World!", 0,  0)      #写入第1行内容
oled.text("MicroPython",  0, 20)      #写入第2行内容
oled.text("By 01Studio",  0, 50)      #写入第3行内容

oled.show()   #OLED执行显示