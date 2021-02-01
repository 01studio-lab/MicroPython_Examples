'''
实验名称：视频播放
版本：v1.0
日期：2020.12
作者：01Studio
说明：AVI视频文件播放。
'''

#导入相关模块

import video,time
from pyb import Switch
from machine import Pin

#构建视频文件对象
v=video.VIDEO()

vol = 80 #音量初始默认80，范围：0-100

######################
# 播放 USR按键
######################
play_flag = 0 #播放标志位

def video_play():
    global play_flag
    play_flag = 1

sw =Switch()
sw.callback(video_play)

######################
# 音量加 A0按键
######################
VOL_U = Pin('A0',Pin.IN,Pin.PULL_UP) #构建按键A0

def vol_up(VOL_U):

    global vol

    #消除按键抖动
    if VOL_U.value() == 0:
        time.sleep_ms(10)
        if VOL_U.value() == 0:
            vol=vol+10
            if vol > 100:
                vol = 100
            v.volume(vol)

#定义中断，下降沿触发,视频播放必须使用硬件中断
VOL_U.irq(vol_up,Pin.IRQ_FALLING,hard=1)

######################
# 音量减 E3按键
######################

VOL_D = Pin('E3',Pin.IN,Pin.PULL_UP) #构建按键A0

def vol_down(VOL_D):

    global vol

    #消除按键抖动
    if VOL_D.value() == 0:
        time.sleep_ms(10)
        if VOL_D.value() == 0:
            vol=vol-10
            if vol < 10:
                vol = 10
            v.volume(vol)

#定义中断，下降沿触发,视频播放必须使用硬件中断
VOL_D.irq(vol_down,Pin.IRQ_FALLING,hard=1)

#加载视频
v.load('/sd/video/badapple.avi')

while True:

    #播放视频
    if play_flag == 1:

        v.play()
        play_flag = 0
