'''
实验名称：触摸按钮
版本：v1.0
日期：2021.8
作者：01Studio
社区：www.01studio.cc
说明：编程实现触摸按钮控制LED。
'''

from tftlcd import LCD32
from touch import XPT2046
from machine import Timer,Pin
import gui,time

#定义常用颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
ORANGE =(0xFF,0x7F,0x00) #橙色

#LCD初始化
d = LCD32() #默认方向
d.fill(WHITE) #填充白色

#触摸屏初始化
t = XPT2046()#默认方向

LED=Pin(2,Pin.OUT) #构建LED对象,开始熄灭
state=0 #LED引脚状态

#####################
#定义2个按键和回调函数
#####################
def fun1(B1):
    
    #LED灯状态翻转
    global state
    state=not state  #使用not语句而非~语句
    LED.value(state) #LED状态翻转

def fun2(B2):
    
    print('Button is pressed!')


B1 = gui.TouchButton(80,50,80,50,BLUE,'Led',WHITE,fun1)
B2 = gui.TouchButton(80,120,80,50,RED,'Button',WHITE,fun2)

# #############################
# #### 定时器用于扫描按钮触发事件 ##
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
