'''
实验名称：视频播放器
版本：v1.0
日期：2019.12
翻译和注释：01Studio
说明：AVI视频播放。
'''

import video,time
from Maix import GPIO
from board import board_info
from fpioa_manager import fm
import lcd

lcd.init()

# 音频使能IO
AUDIO_PA_EN_PIN = 32

#注册音频使能IO
if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)

#注册音频控制IO
fm.register(34,  fm.fpioa.I2S0_OUT_D1, force=True)
fm.register(35,  fm.fpioa.I2S0_SCLK, force=True)
fm.register(33,  fm.fpioa.I2S0_WS, force=True)

#播放avi文件
v = video.open("/sd/badapple.avi")

#打印视频文件信息
print(v)

#音量调节
v.volume(5)

while True:
    if v.play() == 0: #播放完毕
        print("play end")
        break

v.__del__() #销毁对象，释放内存
