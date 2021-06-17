'''
实验名称：流水灯
版本：v2.0
日期：2019.9
作者：01Studio
'''

from pyb import LED  #从pyb导入LED模块
import utime

# 相当于for i in [2, 3]，LED(i).off()执行2次，分别是LED 2，3
for i in range(2,4):
    LED(i).off()

while True:
    #使用for循环
    for i in range(2,4):
        LED(i).on()
        utime.sleep(1) #延时1秒
        LED(i).off()

