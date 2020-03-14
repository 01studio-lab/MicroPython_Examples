'''
实验名称：流水灯
版本：v1.0
日期：2019.9
作者：01Studio
'''

from pyb import LED  #从pyb导入LED模块
import utime

#关闭全部LED
LED(2).off()
LED(3).off()

#while True表示一直循环
while True:
    #LED2亮1秒
    LED(2).on()
    utime.sleep(1)
    LED(2).off()

    #LED3亮1秒
    LED(3).on()
    utime.sleep(1)
    LED(3).off()
