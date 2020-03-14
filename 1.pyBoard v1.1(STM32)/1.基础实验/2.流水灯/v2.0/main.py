'''
实验名称：流水灯
版本：v2.0
日期：2019.4
作者：01Studio
'''

from pyb import LED,delay   #从pyb导入LED模块

# 相当于for i in [2, 3, 4]，LED(i).off()执行3次，分别是LED 2，3，4
for i in range(2,5):
    LED(i).off()

while True:
    #使用for循环
    for i in range(2,5):
        LED(i).on()
        delay(1000) #延时1000毫秒，即1秒
        LED(i).off()

