'''
实验名称：水位传感器
版本：v1.0
日期：2021.7
作者：01Studio 【www.01Studio.org】
说明：通过水位传感器对水位测量并显示。
'''

#导入相关模块
from machine import Pin,SoftI2C,ADC,Timer
from ssd1306 import SSD1306_I2C

#初始化OLED模块
i2c = SoftI2C(sda=Pin(1), scl=Pin(0))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

#初始化ADC,Pin是引脚4，使用默认量程0-1V
Water_level = ADC(Pin(4))

#中断回调函数
def fun(tim):

    oled.fill(0)  # 清屏显示黑色背景
    oled.text('01Studio', 0, 0)  # 首行显示01Studio
    oled.text('Water Level test', 0, 15)      # 次行显示实验名称

    value=Water_level.read() #获取ADC数值

    #显示数值
    oled.text(str(value)+' (4095)',0,40)
 	#计算电压值，获得的数据0-4095相当于0-1V，（'%.2f'%）表示保留2位小数
    oled.text(str('%.2f'%(value/4095))+' V',0,55)

	#判断水位，分5档显示，0-4cm
    if 0 <= value <=1300:
        oled.text('0cm', 60, 55)

    if 1300 < value <= 2300:
        oled.text('1cm', 60, 55)

    if 2300 < value <= 3300:
        oled.text('2cm', 60, 55)

    if 3300 < value <= 3800:
        oled.text('3cm', 60, 55)

    if 3800 <= value:
        oled.text('4cm', 60, 55)

    oled.show()

#开启定时器,周期1s
tim = Timer(0)
tim.init(period=1000, mode=Timer.PERIODIC, callback=fun) 
