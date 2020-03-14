'''
实验名称：W5500以太网模块连接网络
版本：v1.0
日期：2019.11
作者：01Studio
说明：通过Socket编程实现pyBoard+W5500以太网模块连接网络。
'''

import network,usocket,pyb
from machine import I2C,Pin
from ssd1306 import SSD1306_I2C

#初始化相关模块，OLED引脚换成了Y9、Y10
i2c = I2C(sda=Pin('Y10'), scl=Pin('Y9'))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#以太网模块初始化
nic = network.WIZNET5K(pyb.SPI(2), 'Y5', 'Y4')
nic.active(True)
nic.ifconfig('dhcp')

#判断网络是否连接成功
if nic.isconnected():

    print(nic.ifconfig()) #打印IP信息

    #OLED数据显示
    oled.fill(0)   #清屏背景黑色
    oled.text('IP/Subnet/GW:',0,0)
    oled.text(nic.ifconfig()[0], 0, 20)
    oled.text(nic.ifconfig()[1],0,38)
    oled.text(nic.ifconfig()[2],0,56)
    oled.show()
