'''
实验名称：触摸屏应用
版本： v1.0
日期： 2019.12
翻译和注释： 01Studio
'''

#导入相关模块
from machine import I2C
from fpioa_manager import fm
from Maix import GPIO
import lcd, image
import touchscreen as ts

#按键KEY用于清屏
fm.register(16, fm.fpioa.GPIO1, force=True)
btn_clear = GPIO(GPIO.GPIO1, GPIO.IN)

#触摸使用I2C控制（NS2009）
i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)

#触摸屏初始化
ts.init(i2c)
#ts.calibrate() #触摸校准

#LCD初始化
lcd.init()
lcd.clear()

#新建图像和触摸屏相关参数变量
img = image.Image()
status_last = ts.STATUS_IDLE
x_last = 0
y_last = 0
draw = False

while True:

    #获取触摸屏状态
    (status,x,y) = ts.read()
    print(status, x, y)

    #画图
    if draw:
        img.draw_line((x_last, y_last, x, y))

    #更新最后坐标
    x_last = x
    y_last = y

    #根据触摸屏状态判断是否继续执行画图功能
    if status_last!=status:
        if (status==ts.STATUS_PRESS or status == ts.STATUS_MOVE):
            draw = True
        else: #松开
            draw = False
        status_last = status

    #LCD显示
    lcd.display(img)

    #按键KEY按下清屏
    if btn_clear.value() == 0:
        img.clear()
