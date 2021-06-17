'''
实验名称：RTC实时时钟
版本：v1.0
日期：2020.12
作者：01Studio
说明：在LCD上显示时间
社区：www.01studio.org
'''

#导入相关模块
import pyb
from tftlcd import LCD43M

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

########################
# 构建4.3寸LCD对象并初始化
########################
d = LCD43M(portrait=1) #默认方向
d.fill(WHITE)#填充白色

#初始化RTC
rtc = pyb.RTC()

# 定义星期和时间（时分秒）显示字符列表
week = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
time = ['', '', '']

#显示标题
d.printStr('01Studio RTC', 100, 10, BLACK, size=4)


# 首次上电配置时间，按顺序分别是：年，月，日，星期，时，分，秒，次秒级；这里做#了一个简单的判断，检查到当前年份不对就修改当前时间，开发者可以根据自己实际情况来修改。
if rtc.datetime()[0] != 2019:
    rtc.datetime((2019, 4, 1, 1, 0, 0, 0, 0))

while True:

    datetime = rtc.datetime()  # 获取当前时间

    # 显示日期，字符串可以直接用“+”来连接
    d.printStr(str(datetime[0]) + '-' + str(datetime[1]) + '-' + str(datetime[2]) + ' ' + week[(datetime[3] - 1)], 10, 100, BLACK, size=4)

    # 显示时间需要判断时、分、秒的值否小于10，如果小于10，则在显示前面补“0”以到较佳的显示效果
    for i in range(4, 7):
        if datetime[i] < 10:
            time[i - 4] = "0"
        else:
            time[i - 4] = ""

    # 显示时间
    d.printStr(time[0] + str(datetime[4]) + ':' + time[1] + str(datetime[5]) + ':' + time[2] + str(datetime[6]), 10, 200, BLACK, size=4)
    pyb.delay(300) #延时500ms
