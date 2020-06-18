'''
实验名称：蓝牙广播
版本：v1.0
日期：2020.5
作者：01Studio
说明：编程实现无线广播。
'''

import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

#构建BLE对象
ble = BLERadio()

#定义广播名称
ble.name='01Studio'

#服务类型，本例程暂时不提供蓝牙服务
advertisement = ProvideServicesAdvertisement()

#开始广播
ble.start_advertising(advertisement)

#保持程序运行
while True:
    pass
