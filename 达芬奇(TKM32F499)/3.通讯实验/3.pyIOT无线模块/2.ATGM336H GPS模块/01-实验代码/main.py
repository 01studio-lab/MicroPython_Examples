'''
实验名称：pyIOT-GPS模块（中科微 ATGM336H GPS模块）
版本：v1.0
日期：2021.3
作者：01Studio
说明：编程实现串口获取GPS数据并显示
实验平台：01Studio 达芬奇
'''

#导入串口模块
from machine import UART
from tftlcd import LCD43R
import time

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE=(255,255,255)

########################
# 构建4.3寸LCD对象并初始化
########################
d = LCD43R(portrait=1) #默认方向

#画接收框
d.fill(WHITE)
d.printStr('GPS Location', 80, 20, BLUE, size=4)

#GPS数据说明
#消息ID：$GNGGA,双模GPS
#[0]定位点UTC时间
#[1]纬度[2]纬度方向[3]经度[4]经度方向
#[5]GPS定位状态
#[6]卫星数量
#[7]水平精度衰减因子
#[8]海平面高度[9]高度单位
GPS_INFO=['','','','','','','','','','','','','',''] #14个数据
k1='$GNGGA,' #关键词,双模GPS数据

#构建蓝牙模块对象（串口2）
GPS=UART(2,9600) #设置串口号3和波特率,TX--A2,RX--A3

#接收信息
while True:

    if GPS.any(): #查询是否有信息
        text0 = GPS.read(1024) #默认单次最多接收128字节'''
        #print(text0) #原始数据

        text=str(text0) #将数据转成字符

        #找到双模定位
        if text.find(k1) != -1 :
            begin_num=text.find(k1)+7 #起始字符
            for i in range(14):
                while text[begin_num]!=',' :
                    GPS_INFO[i] = GPS_INFO[i]+str(text[begin_num])
                    begin_num=begin_num+1
                begin_num=begin_num+1

            print(GPS_INFO) #双模GPS数据

            #时间
            try:
                time_data=GPS_INFO[0].split('.')
                hh=int(int(time_data[0])/10000)+8 #北京时间东八区
                mm=int(int(time_data[0])%10000/100)
                ss=int(int(time_data[0])%100)
                print('Time: '+str(hh)+':'+str(mm)+':'+str(ss))
                d.printStr('Time: '+str(hh)+':'+str(mm)+':'+str(ss), 10, 100, BLACK, size=3)
            
            except ValueError as e: #异常提示
                pass
            
            #经纬度
            print(GPS_INFO[1]+' '+GPS_INFO[2])
            print(GPS_INFO[3]+' '+GPS_INFO[4])
            d.printStr(GPS_INFO[1]+' '+GPS_INFO[2], 10, 150, BLACK, size=3)
            d.printStr(GPS_INFO[3]+' '+GPS_INFO[4], 10, 200, BLACK, size=3)

            #定位状态，1为定位成功
            print('GPS State: '+GPS_INFO[5])
            d.printStr('GPS State: '+GPS_INFO[5], 10, 250, BLACK, size=3)

            #卫星数量
            print('Satellites: '+GPS_INFO[6])
            d.printStr('Satellites: '+GPS_INFO[6], 10, 300, BLACK, size=3)

            #水平精度衰减因子
            print('Horizontal precision attenuation factor: '+GPS_INFO[7])

            #海拔高度
            print('altitude: '+GPS_INFO[8]+GPS_INFO[9])
            d.printStr('altitude: '+GPS_INFO[8]+GPS_INFO[9], 10, 350, BLACK, size=3)


            #清空数据
            for i in range(14):
                GPS_INFO[i]=''

