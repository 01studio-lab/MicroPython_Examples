# 普通拍照例程
# 提示: 你需要插入SD卡来运行这个例程.
#作者：01Studio

import sensor, lcd, image
from Maix import GPIO
from fpioa_manager import fm

#配置LED蓝、红引脚
fm.register(12, fm.fpioa.GPIO0,force=True)
fm.register(14, fm.fpioa.GPIO1,force=True)

LED_B = GPIO(GPIO.GPIO0, GPIO.OUT,value=1) #构建LED对象
LED_R = GPIO(GPIO.GPIO1, GPIO.OUT,value=1) #构建LED对象

#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(40)
sensor.set_vflip(1)  #设置为后置模式

lcd.init()  #LCD初始化

#红灯亮提示拍照开始
LED_R.value(0)
sensor.skip_frames(time = 2000) # 给2秒时间用户准备.
LED_R.value(1)

#蓝灯亮提示正在拍照
LED_B.value(0)
print("You're on camera!")

# 拍摄并保存相关文件，也可以用"example.bmp"或其它文件方式。
sensor.snapshot().save("/sd/example.jpg")

LED_B.value(1) #l蓝灯灭提示拍照完成

lcd.display(image.Image("/sd/example.jpg")) #LCD显示照片
