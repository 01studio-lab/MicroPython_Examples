'''
实验名称：ADC
版本：v1.0
日期：2020.4
说明：0-3.3V电压测量
www.01studio.org
'''

#导入相关库
import time
import board
from analogio import AnalogIn

adc = AnalogIn(board.A5) #输入IO

while True:
    #输出电压，保留2位小数。精度16bit
    print(round(adc.value*3.3/65535,2))
    time.sleep(0.1) #测量周期100ms

