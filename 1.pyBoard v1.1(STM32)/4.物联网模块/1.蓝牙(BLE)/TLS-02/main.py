'''
实验名称：串口蓝牙模块通信（WeBee TLS-02 BLE模块）
版本：v1.0
日期：2020-4-10
作者：01Studio
说明：通过编程实现串口通信，跟电脑串口助手实现数据收发。
'''

#导入串口模块
from tls02 import TLS02
import time

#构建蓝牙模块对象（串口）
BLE=TLS02(3,9600) #设置串口号3和波特率,TX--Y9,RX--Y10

###############信息透传################
BLE.uart.write('Hello 01Studio!')#发送一条数据

#接收信息
while True:
    if BLE.uart.any(): #查询是否有信息
        text = BLE.uart.read(128) #默认单次最多接收128字节'''
        print(text)

#查看广播名字
#print(BLE.Name_Check())

#查看广播间隔,ms
#print(BLE.BI_Check())

#查看模块波特率
#print(BLE.Baudrate_Check())

#设置名字
#print(BLE.Name_Set("01Studio"))

#设置广播间隔，单位ms
#BLE.BI_Set(200)

#设置波特率，设置完成后需要复位，以及重置开发板UART波特率
#BLE.Baudrate_Set(9600)

#模块复位
#BLE.RST()

#模块重置，重置完会自动复位，复位后延时
#BLE.RESET()
#time.sleep_ms(600)
