'''
实验名称：DAC-蜂鸣器
版本：v1.0
日期：2019.4
作者：01Studio
说明：通过USER按键让DAC输出不同频率的方波来驱动蜂鸣器。
'''

#导入相关模块
from pyb import DAC,Switch
from machine import Pin,I2C
from ssd1306 import SSD1306_I2C

#初始化相关模块
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

sw = Switch()     #定义按键对象名字为sw
dac = DAC(1)     #定义DAC对象名字为dac，输出引脚为X5

#定义4组频率值：1Hz、200Hz、1000Hz、5000Hz
freq=[1,200,1000,5000]

# 定义8位精度下方波的值。0、255分别对应输出0V、3.3V。需要定义成字节数组。
buf = bytearray(2)
buf[0]=0
buf[1]=255

key_node = 0  #按键标志位
i = 0         #用于选择频率数组

##############################################
#  按键和其回调函数
##############################################
def key():
    global key_node
    key_node = 1

sw.callback(key)  #当按键被按下时，执行函数key()

##############################################
#  OLED初始显示
##############################################
oled.fill(0)  # 清屏显示黑色背景
oled.text('01Studio', 0, 0)  # 首行显示01Studio
oled.text('DAC-Beep', 0, 15)  # 次行显示实验名称
oled.text('Pls Press USER', 0, 40)  # 显示当前频率
oled.show()

while True:

    if key_node==1: #按键被按下
        i = i+1
        if i == 4:
            i = 0
        key_node = 0 #清空按键标志位

        #DAC输出指定频率
        dac.write_timed(buf, freq[i]*len(buf), mode=DAC.CIRCULAR)

        #显示当前频率
        oled.fill(0)  # 清屏显示黑色背景
        oled.text('01Studio', 0, 0)  # 首行显示01Studio
        oled.text('DAC-Beep', 0, 15)  # 次行显示实验名称
        oled.text(str(freq[i]) + 'Hz', 0, 40)  # 显示当前频率
        oled.show()
