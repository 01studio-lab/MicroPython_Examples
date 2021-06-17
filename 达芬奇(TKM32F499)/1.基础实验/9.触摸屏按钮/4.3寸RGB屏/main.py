'''
实验名称：触摸按钮
版本：v1.0
日期：2021.4
作者：01Studio
社区：www.01studio.org
说明：编程实现触摸按钮控制LED。
实验平台：01Studio 达芬奇
'''

#导入相关模块
from tftlcd import LCD43R
from touch import FT5436
from machine import LED,Timer
import gui,time

#定义常用颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE =(0xFF,0x7F,0x00) #橙色

#LCD初始化
d = LCD43R() #默认方向
d.fill(WHITE) #填充白色

#触摸屏初始化
t = FT5436() #默认方向

#####################
#定义4个按键和回调函数
#####################
def fun1(B1):
    LED(1).toggle() #LED3状态翻转

def fun2(B2):
    LED(2).toggle() #LED4状态翻转
    
def fun3(B3):
    LED(3).toggle() #LED3状态翻转

def fun4(B4):
    LED(4).toggle() #LED4状态翻转

B4 = gui.TouchButton(40,50,150,80,BLUE,'LED4',WHITE,fun4)
B3 = gui.TouchButton(230,50,150,80,ORANGE,'LED3',WHITE,fun3)
B2 = gui.TouchButton(420,50,150,80,GREEN,'LED2',WHITE,fun2)
B1 = gui.TouchButton(610,50,150,80,RED,'LED1',WHITE,fun1)

#############################
#### 定时器用于扫描按钮触发事件 ##
#############################
tim_flag = 0

def count(tim):
    global tim_flag
    tim_flag = 1

#构建软件定时器，编号1
tim = Timer(1) 
tim.init(period=20, mode=Timer.PERIODIC,callback=count) #周期为20ms

while True:

    #执行按钮触发的任务
    if tim_flag == 1:
        
        t.tick_inc()
        gui.task_handler()
        tim_flag = 0
