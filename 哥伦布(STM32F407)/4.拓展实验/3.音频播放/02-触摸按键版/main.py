'''
实验名称：音频播放
版本：v1.0
日期：2020.12
作者：01Studio
说明：mp3/wav音频文件播放，使用触摸按键控制。
'''

from tftlcd import LCD43M
from touch import GT1151
from pyb import Timer
import audio,gui,time

#音频 初始化
wm=audio.WM8978()

#定义常用颜色
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
#灰色
GRAY1 =(0x80,0x80,0x80)
GRAY2 =(0xa0,0xa0,0xa0)

#LCD初始化
d = LCD43M() #默认方向
d.fill(WHITE) #填充白色

#显示音乐播放器背景
d.Picture(0,0,"/flash/picture/music_player.jpg")

#触摸屏初始化
t = GT1151()#默认方向



########################
#定义音频相关按键和回调函数
########################
audio_flag = 0
pause_flag = 0 #暂停标志位

#首次播放和继续播放共用
def fun1(B1):

    global audio_flag,pause_flag

    #如果是暂停后按play按钮，则继续播放
    if pause_flag == 1:
        wm.continue_play()
        pause_flag =0

    audio_flag = 1

#暂停播放
def fun2(B2):
    global pause_flag
    wm.pause()#暂停播放
    pause_flag = 1

#停止播放
def fun3(B3):
    wm.stop()#停止播放

#音量加
def fun4(B4):
    global vol
    vol = vol+10
    if vol > 100:
        vol = 100
    print(vol)
    wm.volume(vol)

#音量减
def fun5(B5):
    global vol
    vol = vol-10
    if vol < 0:
        vol = 0
    print(vol)
    wm.volume(vol)


B1 = gui.TouchButton(20,580,130,80,GRAY1,'PLAY',WHITE,fun1)
B2 = gui.TouchButton(170,580,130,80,GRAY1,'PAUSE',WHITE,fun2)
B3 = gui.TouchButton(320,580,130,80,GRAY1,'STOP',WHITE,fun3)
B4 = gui.TouchButton(60,700,150,80,GRAY2,'VOL+',WHITE,fun4)
B5 = gui.TouchButton(270,700,150,80,GRAY2,'VOL-',WHITE,fun5)

#############################
#### 定时器用于触发按钮事件 ##
#############################
tim_flag = 0

def count(tim):
    global tim_flag
    tim_flag = 1

tim = Timer(1,freq=50) #20ms刷新一次
tim.callback(count)

#加载音乐
wm.load('/flash/music/Seasons In The Sun.mp3')

vol = 80 #音量初始默认80，范围：0-100

while True:

    #执行按钮触发的任务
    if tim_flag == 1:
        t.tick_inc()
        gui.task_handler()
        tim_flag = 0


    #播放音乐
    if audio_flag == 1:
        wm.stop() #从头播放前先停止之前的播放
        wm.play()
        audio_flag = 0
