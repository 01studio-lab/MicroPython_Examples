'''
实验名称：无线数据收发（UART服务）
版本：v1.0
日期：2020.5
作者：01Studio
说明：编程实现手机和蓝牙开发板数据传输。
'''

#导入相关模块
import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

#构建蓝牙对象
ble = BLERadio()

#定义广播名称
ble.name='01Studio'

#构建UART服务
Uart_Service = UARTService()

#广播添加UART服务
advertisement = ProvideServicesAdvertisement(Uart_Service)

while True:

    #发起广播
    ble.start_advertising(advertisement)

    #等待连接
    while not ble.connected:
        pass

    #连接蔡成功
    while ble.connected:

        # 读取128个字节数据，如果没数据，则返回 b''
        one_byte = Uart_Service.read(128)

        #收到信息，REPL打印并回发
        if one_byte:
            print(one_byte)
            Uart_Service.write(one_byte)
