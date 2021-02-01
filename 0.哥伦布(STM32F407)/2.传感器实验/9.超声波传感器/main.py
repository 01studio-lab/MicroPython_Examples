'''
实验名称：超声波传感器
版本：v1.0
日期：2020.12
作者：01Studio 【www.01Studio.org】
说明：通过超声波传感器测距，并在OLED上显示。
'''

#导入相关模块
import pyb
from HCSR04 import HCSR04
from machine import Pin,I2C
from tftlcd import LCD43M

#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)

#初始化LCD
d=LCD43M()
d.fill(WHITE)#填充白色

#初始化接口 trig='B10',echo='B11'
trig = Pin('B10',Pin.OUT_PP)
echo = Pin('B11',Pin.IN)
HC=HCSR04(trig,echo)

#显示标题
d.printStr('01Studio Distance', 40, 10, BLACK, size=4)

while True:

    Distance = HC.getDistance() #测量距离

    #采集温度、压强、高度信息数据并用LCD显示：
    d.printStr(str(Distance) + ' CM  ', 10, 100, BLACK, size=4)

    print(str(Distance) + ' CM')

    pyb.delay(1000) #延时1秒
