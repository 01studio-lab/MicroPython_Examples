'''
实验名称：RTC实时时钟
版本：v1.0
日期：2019.9
作者：01Studio
'''

# 导入相关模块
from pyb import RTC
from machine import Pin, I2C
from ssd1306x import SSD1306_I2C
import utime

# 定义星期和时间（时分秒）显示字符列表
week = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
time = ['', '', '']

# 初始化所有相关对象
i2c = I2C(sda=Pin("P0"), scl=Pin("P2"), freq=80000) #频率8MHz
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
rtc = RTC()

# 首次上电配置时间，按顺序分别是：年，月，日，星期，时，分，秒，次秒级；这里做了
# 一个简单的判断，检查到当前年份不对就修改当前时间，开发者可以根据自己实际情况来
# 修改。
if rtc.datetime()[0] != 2019:
    rtc.datetime((2019, 4, 1, 1, 0, 0, 0, 0))

while True:

    datetime = rtc.datetime()  # 获取当前时间

    oled.fill(0)  # 清屏显示黑色背景
    oled.text('01Studio', 0, 0)    # 首行显示01Studio
    oled.text('RTC Clock', 0, 15)  # 次行显示实验名称

    # 显示日期，字符串可以直接用“+”来连接
    oled.text(str(datetime[0]) + '-' + str(datetime[1]) + '-' + str(datetime[2]) + ' ' + week[(datetime[3] - 1)], 0, 40)

    # 显示时间需要判断时、分、秒的值否小于10，如果小于10，则在显示前面补“0”以达
    # 到较佳的显示效果
    for i in range(4, 7):
        if datetime[i] < 10:
            time[i - 4] = "0"
        else:
            time[i - 4] = ""

    # 显示时间
    oled.text(time[0] + str(datetime[4]) + ':' + time[1] + str(datetime[5]) + ':' + time[2] + str(datetime[6]), 0, 55)

    oled.show()
    utime.sleep_ms(300)  #延时300ms
