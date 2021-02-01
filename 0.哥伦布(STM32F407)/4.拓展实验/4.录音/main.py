'''
实验名称：录音
版本：v1.0
日期：2020.12
作者：01Studio
说明：编程实现录音和播放。
'''

#导入相关模块
import audio,time
from pyb import Switch,LED
from machine import Pin

#构建语音模块对象
wm=audio.WM8978()

record_flag = 0 #录音标志位

######################
# 开始录音 USR按键
######################
def rec_begin():
    global record_flag
    record_flag = 1

sw =Switch()
sw.callback(rec_begin)

######################
# 停止录音 A0按键
######################
KEY_A = Pin('A0',Pin.IN,Pin.PULL_UP) #构建按键A0

def rec_stop(KEY_A):
    global record_flag
    #消除按键抖动
    if KEY_A.value() == 0:
        time.sleep_ms(5)
        if KEY_A.value() == 0:

            record_flag = 2

KEY_A.irq(rec_stop,Pin.IRQ_FALLING) #定义中断，下降沿触发

######################
# 音量减 E3按键
######################

KEY_E = Pin('E3',Pin.IN,Pin.PULL_UP) #构建按键A0

def rec_play(KEY_E):

    global record_flag

    #消除按键抖动
    if KEY_E.value() == 0:
        time.sleep_ms(10)
        if KEY_E.value() == 0:

            record_flag = 3

KEY_E.irq(rec_play,Pin.IRQ_FALLING) #定义中断，下降沿触发


while True:

    #开始录音
    if record_flag == 1:
        wm.record("/flash/test.wav",db=80)
        LED(3).on() #开始录音
        record_flag = 0

    #停止录音
    if record_flag == 2:
        wm.record_stop()
        LED(4).on() #结束录音
        record_flag = 0

    #播放录音，录音完成后按RST复位开发板才有效
    if record_flag == 3:
        #加载录音
        wm.load('/flash/test.wav')
        wm.play()
        record_flag = 0
