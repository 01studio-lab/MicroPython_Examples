# LCD 示例程序
#
# 提示: 这个实验需要外接一个LCD模块.
#
# 本示例实现了LCD实时显示摄像头帧缓冲画面.
#
#翻译和注释：01Studio

import sensor, image, lcd

#摄像头初始化
sensor.reset() # 初始化摄像头.
sensor.set_pixformat(sensor.RGB565) # 或者 sensor.GRAYSCALE
sensor.set_framesize(sensor.QQVGA2) # LCD的分辨率为 128x160 .

#LCD初始化
lcd.init()

while(True):
    lcd.display(sensor.snapshot()) # 拍照和显示图像.

