'''
实验名称：流水灯
版本：v1.0
日期：2020.12
作者：01Studio
'''

from pyb import LED,delay   #从pyb导入LED模块

#关闭全部LED
LED(2).off()
LED(3).off()
LED(4).off()

#while True表示一直循环
while True:
    #LED2亮1秒
    LED(2).on()
    pyb.delay(1000)
    LED(2).off()

    #LED3亮1秒
    LED(3).on()
    pyb.delay(1000)
    LED(3).off()

    #LED4亮1秒
    LED(4).on()
    pyb.delay(1000)
    LED(4).off()
