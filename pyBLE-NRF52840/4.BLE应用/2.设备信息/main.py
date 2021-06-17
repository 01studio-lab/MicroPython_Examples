'''
实验名称：设备信息
版本：v1.0
日期：2020.5
作者：01Studio
说明：编程实现无线广播。
'''

import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.device_info import DeviceInfoService

#构建BLE对象
ble = BLERadio()

#定义广播名称
ble.name = '01Studio'

#定义设备信息
dev_info = DeviceInfoService(manufacturer='01Studio',
                            software_revision='v1.0',
                            model_number='pyBLE-NRF52840',
                            serial_number=None,
                            firmware_revision=None,
                            hardware_revision='v1.0',
                            service=None)

#广播添加设备信息服务
advertisement = ProvideServicesAdvertisement(dev_info)

#发起广播
ble.start_advertising(advertisement)

while True:
    pass
