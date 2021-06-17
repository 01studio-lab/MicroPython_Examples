'''
实验名称：定时器（蓝灯周期性闪烁）
版本：v1.0
日期：2019.9
作者：01Studio
'''

import pyb

tim = pyb.Timer(4,freq=1)      # 使用定时器4创建定时器对象,频率1Hz
tim.callback(lambda t:pyb.LED(3).toggle()) #定时器中断，执行LED（3）蓝灯状态反转
