'''
实验名称：温湿度传感器实验DTH11
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过编程采集温湿度数据，并在LCD上显示。。
'''

#导入相关模块
from pyb import delay
from machine import Pin
from tftlcd import LCD43M
from dht import DHT11

#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)

#初始化LCD
d=LCD43M()
d.fill(WHITE)#填充白色

#创建DTH11对象dt
dt=DHT11(Pin('G7'))

#显示标题
d.printStr('01Studio DHT11', 40, 10, BLACK, size=4)

delay(1000) #首次启动停顿1秒然传感器稳定

while True:

    #获取温湿度值
    dt.measure()
    te=dt.temperature()
    dh=dt.humidity()

    #实时显示温湿度度值
    d.printStr('Temp: '+str(te)+' C',10,100,BLACK,size=4)
    d.printStr('Humi: '+str(dh)+' %',10,200,BLACK,size=4)

    delay(2000) #采集周期2秒

