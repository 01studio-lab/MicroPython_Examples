'''
实验名称：音频播放
版本：v1.0
日期：2020.12
作者：01Studio
说明：MP3/WAV音频文件播放。使用物理按键控制
'''

#导入相关模块
import audio,time
from pyb import Switch
from machine import Pin

#构建音频对象
wm=audio.WM8978()

vol = 80 #音量初始化，80

######################
# 播放 USR按键
######################
play_flag = 0

def music_play():
    global play_flag
    play_flag = 1

sw =Switch()
sw.callback(music_play)

######################
# 音量加 A0按键
######################
VOL_U = Pin('A0',Pin.IN,Pin.PULL_UP) #构建按键A0

vol_up_flag = 0

def vol_up(VOL_U):

    global vol

    #消除按键抖动
    if VOL_U.value() == 0:
        time.sleep_ms(10)
        if VOL_U.value() == 0:
            vol=vol+10
            if vol > 100:
                vol = 100
            wm.volume(vol)

VOL_U.irq(vol_up,Pin.IRQ_FALLING, hard=1) #定义中断，下降沿触发

######################
# 音量减 E3按键
######################

VOL_D = Pin('E3',Pin.IN,Pin.PULL_UP) #构建按键A0

vol_down_flag = 0

def vol_down(VOL_D):

    global vol

    #消除按键抖动
    if VOL_D.value() == 0:
        time.sleep_ms(10)
        if VOL_D.value() == 0:
            vol=vol-10
            if vol < 10:
                vol = 10
            wm.volume(vol)

VOL_D.irq(vol_down,Pin.IRQ_FALLING, hard=1) #定义中断，下降沿触发

#加载音乐
wm.load('/flash/music/Seasons In The Sun.mp3')

while True:

    #播放音乐
    if play_flag == 1:

        wm.play()
        play_flag = 0


