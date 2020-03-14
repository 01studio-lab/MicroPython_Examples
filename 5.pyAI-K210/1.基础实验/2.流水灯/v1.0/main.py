'''
实验名称：流水灯
版本：v1.0
日期：2019.12
作者：01Studio
实验目的：让RGB灯循环闪烁。
'''
from Maix import GPIO
from fpioa_manager import fm
import utime

#将将LED外部IO注册到内部GPIO，K210引脚支持任意配置
fm.register(12, fm.fpioa.GPIO0)
fm.register(13, fm.fpioa.GPIO1)
fm.register(14, fm.fpioa.GPIO2)

#构建LED对象，并初始化输出高电平，关闭LED
LED_B = GPIO(GPIO.GPIO0, GPIO.OUT,value=1)
LED_G = GPIO(GPIO.GPIO1, GPIO.OUT,value=1)
LED_R = GPIO(GPIO.GPIO2, GPIO.OUT,value=1)

while True:

    #蓝灯亮1秒
    LED_B.value(0) #点亮LED
    utime.sleep(1)
    LED_B.value(1) #关闭LED

    #绿灯亮1秒
    LED_G.value(0) #点亮LED
    utime.sleep(1)
    LED_G.value(1) #关闭LED

    #红灯亮1秒
    LED_R.value(0) #点亮LED
    utime.sleep(1)
    LED_R.value(1) #关闭LED
