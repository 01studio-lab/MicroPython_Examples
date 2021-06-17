'''
实验名称：触摸按钮
版本：v1.0
日期：2020.12
作者：01Studio
社区：www.01studio.org
说明：编程实现触摸按钮控制LED。
'''

from tftlcd import LCD43M
from touch import GT1151
from pyb import LED,Timer
import gui,time

#定义常用颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE =(0xFF,0x7F,0x00) #橙色

#LCD初始化
d = LCD43M() #默认方向
d.fill(WHITE) #填充白色

#触摸屏初始化
t = GT1151()#默认方向

#####################
#定义2个按键和回调函数
#####################
def fun1(B1):
    LED(3).toggle() #LED3状态翻转

def fun2(B2):
    LED(4).toggle() #LED4状态翻转

B1 = gui.TouchButton(140,200,200,100,ORANGE,'LED3',WHITE,fun1)
B2 = gui.TouchButton(140,500,200,100,BLUE,'LED4',WHITE,fun2)

#############################
#### 定时器用于触发按钮事件 ##
#############################
tim_flag = 0

def count(tim):
    global tim_flag
    tim_flag = 1

tim = Timer(1,freq=50) #20ms刷新一次
tim.callback(count)

while True:

    #执行按钮触发的任务
    if tim_flag == 1:
        t.tick_inc()
        gui.task_handler()
        tim_flag = 0
