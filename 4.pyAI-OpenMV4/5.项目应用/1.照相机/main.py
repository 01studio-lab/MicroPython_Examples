'''
实验名称：照相机
版本：v1.0
日期：2019.10
作者：01Studio 【www.01Studio.org】
说明：通过按键拍照并在LCD上显示（本实验需要SD卡）。
'''


import sensor, image, pyb, lcd
from pyb import ExtInt,Pin,RTC

RED_LED_PIN = 1
BLUE_LED_PIN = 3

#摄像头初始化
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.LCD) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

#LCD初始化
lcd.init()

#时间初始化，用于给图片命名
rtc=RTC()

key_node = 0  #按键标志位

##############################################
#  按键和其回调函数
##############################################
def key(ext):
    global key_node
    key_node = 1

ext = ExtInt(Pin('P9'), ExtInt.IRQ_FALLING, Pin.PULL_UP, key) #下降沿触发，打开上拉电阻

while True:

    lcd.display(sensor.snapshot()) # LCD实时显示

    if key_node==1: #按键被按下
        key_node = 0 #清空按键标志位

        #红灯亮提示用户看镜头
        pyb.LED(RED_LED_PIN).on()
        sensor.skip_frames(time = 2000)

        #红灯灭，蓝灯亮提示开始拍照
        pyb.LED(RED_LED_PIN).off()
        pyb.LED(BLUE_LED_PIN).on()

        print("You're on camera!")

        #拍照并保存，保存文件用时间来命名。
        lcd.display(sensor.snapshot().save(str(rtc.datetime())+".jpg"))

        pyb.LED(BLUE_LED_PIN).off()
        print("Done! Reset the camera to see the saved image.")

        #延时3秒，观看拍摄图片
        pyb.delay(3000)
