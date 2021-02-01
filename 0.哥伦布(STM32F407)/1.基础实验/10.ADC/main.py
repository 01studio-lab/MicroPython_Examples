'''
实验名称：ADC-电压测量
版本：v1.0
日期：2020.12
作者：01Studio
说明：通过对ADC数据采集，转化成电压在显示屏上显示。ADC精度12位，电压0-3.3V。
'''

#导入相关模块
import pyb,time
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

#构建ADC对象，引脚PA5
adc = pyb.ADC('A5')

#显示标题
d.printStr('01Studio ADC', 100, 10, BLACK, size=4)

while True:

    #电压采集
    value = str(adc.read()) #原始值
    vol = str('%.2f'%(adc.read()/4095*3.3)) #电压值，0-3.3V

    #显示测量值和电压值
    d.printStr('Vol:'+vol+" V", 10, 100, BLACK, size=4)
    d.printStr('Value:'+value+"   ", 10, 200, BLACK, size=4)
    d.printStr("(4095)", 300, 200, BLACK, size=4)
    print(value)

    time.sleep_ms(500) #延时500ms
