'''
实验名称：照相机
版本：v1.0
日期：2019.12
作者：01Studio 【www.01Studio.org】
说明：通过按键拍照并在LCD上显示（本实验需要SD卡）。
'''

import sensor, lcd, utime
from Maix import GPIO
from fpioa_manager import fm

#注册KEY的外部IO
fm.register(16, fm.fpioa.GPIOHS0, force=True)

#构建KEY对象
KEY=GPIO(GPIO.GPIOHS0, GPIO.IN, GPIO.PULL_UP)

#摄像头初始化
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # or sensor.QVGA (or others)
sensor.skip_frames(30) # Let new settings take affect.
#sensor.set_vflip(1)    #摄像头后置模式

#LCD初始化
lcd.init()

key_node = 0  #按键标志位
name_num = 0  #照片名字

##############################################
#  按键和其回调函数
##############################################
def fun(KEY):
    global key_node
    utime.sleep_ms(10) #消除抖动
    if KEY.value()==0: #确认按键被按下
        key_node = 1

#开启中断，下降沿触发
KEY.irq(fun, GPIO.IRQ_FALLING)

while True:

    lcd.display(sensor.snapshot()) # LCD实时显示

    if key_node==1: #按键被按下
        key_node = 0 #清空按键标志位

        #拍照并保存，保存文件用时间来命名。
        lcd.display(sensor.snapshot().save("/sd/"+str(name_num)+".jpg"))
        name_num=name_num+1 #名字编码加1

        print("Done! Reset the camera to see the saved image.")

        #延时3秒，观看拍摄图片
        utime.sleep_ms(3000)
