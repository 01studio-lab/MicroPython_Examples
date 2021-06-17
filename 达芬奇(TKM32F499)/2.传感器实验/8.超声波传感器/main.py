'''
实验名称：超声波传感器
版本：v1.0
日期：2021.5
作者：01Studio 【www.01Studio.org】
说明：通过超声波传感器测距，并在OLED上显示。
'''

#导入相关模块
import time
from machine import Pin
from HCSR04 import HCSR04
from tftlcd import LCD43R

#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

#初始化LCD
d=LCD43R()
d.fill(WHITE)#填充白色

#初始化接口 trig='PA2',echo='PA3'
trig = Pin('A2',Pin.OUT_PP)
echo = Pin('A3',Pin.IN)
HC=HCSR04(trig,echo)

#显示标题
d.printStr('01Studio Distance', 40, 10, BLUE, size=4)

while True:

    Distance = HC.getDistance() #测量距离

    #采集超声波距离数据并用LCD显示：
    d.printStr(str(Distance) + ' CM  ', 10, 100, BLACK, size=4)

    print(str(Distance) + ' CM')

    time.sleep(1) #延时1秒
