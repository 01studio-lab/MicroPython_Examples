# 舵机模块例程.
#
# 本实验请遵循以下要求:
#
#   1. 将舵机连接到任意PWM输出口.
#   2. 需要连接3.7V锂电池 (或5V电源).
#   3. 将 pca9685.py 和 servo.py 文件拷贝到OpenMV的文件系统，然后复位.
#   4. 在IDE里运行本实验代码.
#
#翻译和注释：01Studio

import time
from servo import Servos
from machine import I2C, Pin

#初始化I2C
i2c = I2C(sda=Pin('P5'), scl=Pin('P4'))

#初始化舵机模块
servo = Servos(i2c, address=0x40, freq=50, min_us=500, max_us=2500, degrees=180)

while True:
    for i in range(0, 8):
        servo.position(i, 0) #8路舵机旋转到0°
    time.sleep(500)
    for i in range(0, 8):
        servo.position(i, 180)#8路舵机旋转到180°
    time.sleep(500)
