'''
实验名称：NES游戏模拟器
版本：v1.0
日期：2019.12
说明：NES模拟器运行游戏。
翻译和注释：01Studio
'''

import nes, lcd
from Maix import GPIO
from fpioa_manager import fm

# 音频使能IO
AUDIO_PA_EN_PIN = 32

#注册音频使能IO
if AUDIO_PA_EN_PIN:
    fm.register(AUDIO_PA_EN_PIN, fm.fpioa.GPIO1, force=True)

#LCD初始化
lcd.init()

#初始化nes，配置为键盘控制
nes.init(nes.KEYBOARD)

#运行游戏
nes.run("/sd/Bomberman.nes")
