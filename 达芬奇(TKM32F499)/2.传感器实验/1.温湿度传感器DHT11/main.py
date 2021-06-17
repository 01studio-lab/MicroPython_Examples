'''
实验名称：温湿度传感器实验DTH11
版本：v1.0
日期：2021.1
作者：01Studio
实验平台：达芬奇
'''

#引入相关模块
from machine import Pin
from dht import DHT11
from tftlcd import LCD43R
import time

#定义常用颜色
WHITE=(255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)

#初始化LCD
d=LCD43R()
d.fill(WHITE) #填充白色

#显示标题
d.printStr('01Studio DHT11', 40, 10, BLUE, size=4)

#创建DTH11对象dt
dt = DHT11(Pin('C4'))

# 延时2秒等待DHT11稳定
time.sleep(2)

while True:
    
    try: #异常处理
        dt.measure()
        te=dt.temperature()  #获取温度值
        dh=dt.humidity()    #获取湿度值
        
        #REPL打印
        print(str(dt.temperature())+' C')
        print(str(dt.humidity())+' %')

        #实时显示温湿度度值
        d.printStr('Temp: '+str(te)+' C',10,100,BLACK,size=4)
        d.printStr('Humi: '+str(dh)+' %',10,200,BLACK,size=4)
        
    except Exception as e: #异常提示
        print('Time Out!')
    
    time.sleep(2) #采集周期2秒