'''
实验名称：无线彩灯控制
版本：v1.0
日期：2020.5
作者：01Studio
说明：编程实现手机控制彩灯。
'''

#导入相关模块
import board,neopixel
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket

#构建蓝牙对象
ble = BLERadio()

#定义广播名称
ble.name = '01Studio'

#构建UART服务
uart_server = UARTService()

#广播添加UART服务
advertisement = ProvideServicesAdvertisement(uart_server)

#定义neopixel引脚，默认使用板载neopixel
pixels = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.1)

while True:
    # 广播
    ble.start_advertising(advertisement)

    #等待连接
    while not ble.connected:
        pass

    #已连接
    while ble.connected:

        #获取UART服务数据
        packet = Packet.from_stream(uart_server)

        #判断收到的包和颜色包类型是否一致
        if isinstance(packet, ColorPacket):
            print(packet.color)
            pixels.fill(packet.color) #修改灯珠颜色
