'''
实验名称：温度传感器DS18B20
版本：v1.0
日期：2019.8
作者：01Studio
说明：通过编程采集温度数据，并在OLED上显示。。
'''

#引用相关模块
from machine import Pin,I2C,Timer
from ssd1306 import SSD1306_I2C
import onewire,ds18x20

#初始化相关模块
i2c = I2C(sda=Pin(13), scl=Pin(14))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化DS18B20
ow= onewire.OneWire(Pin(4)) #使能单总线
ds = ds18x20.DS18X20(ow)        #传感器是DS18B20
rom = ds.scan()         #扫描单总线上的传感器地址，支持多个传感器同时连接

def temp_get(tim):
    ds.convert_temp()
    temp = ds.read_temp(rom[0]) #温度显示,rom[0]为第1个DS18B20

    #OLED数据显示
    oled.fill(0)   #清屏背景黑色
    oled.text('MicroPython', 0, 0)
    oled.text('Temp test:',0,20)
    oled.text(str('%.2f'%temp)+' C',0,40) #显示temp,保留2位小数
    oled.show()

#开启RTOS定时器，编号为-1
tim = Timer(-1)
tim.init(period=1000, mode=Timer.PERIODIC,callback=temp_get) #周期为1000ms
