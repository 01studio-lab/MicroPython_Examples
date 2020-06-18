'''
实验名称：通过littlevGL按钮实现LED蓝灯状态翻转
版本：v1.0
日期：2020.1
作者：01Studio
实验说明：此例程仅供参考，更多MicroPython+littlevGL相关内容请查阅以下链接：
        https://blog.littlevgl.com/2019-02-20/micropython-bindings
'''

import lvgl as lv
import lvgl_helper as lv_h
import touchscreen as ts
import lcd,time
from machine import Timer
from machine import I2C
from Maix import GPIO
from fpioa_manager import fm

#将蓝灯引脚IO12配置到GPIO0，K210引脚支持任意配置
fm.register(12, fm.fpioa.GPIO0,force=True)
LED_B = GPIO(GPIO.GPIO0, GPIO.OUT,value=1) #构建LED对象
KEY_NODE = 1

i2c = I2C(I2C.I2C0, freq=400000, scl=30, sda=31)
ts.init(i2c)
lcd.init()
lv.init()

#LCD参数配置
disp_buf1 = lv.disp_buf_t()
buf1_1 = bytearray(320*10)
lv.disp_buf_init(disp_buf1,buf1_1, None, len(buf1_1)//4)
disp_drv = lv.disp_drv_t()
lv.disp_drv_init(disp_drv)
disp_drv.buffer = disp_buf1
disp_drv.flush_cb = lv_h.flush

disp_drv.hor_res = 320
disp_drv.ver_res = 240

lv.disp_drv_register(disp_drv)

#触摸屏参数配置
indev_drv = lv.indev_drv_t()
lv.indev_drv_init(indev_drv)
indev_drv.type = lv.INDEV_TYPE.POINTER
indev_drv.read_cb = lv_h.read
lv.indev_drv_register(indev_drv)

#按钮回调函数
def event_handler(obj, event):
    global KEY_NODE
    if event == lv.EVENT.CLICKED:
        print("Clicked")
        KEY_NODE=not KEY_NODE
        LED_B.value(KEY_NODE) #蓝色LED状态翻转

#按钮初始化
btn1 = lv.btn(lv.scr_act())
btn1.set_event_cb(event_handler)
btn1.align(None, lv.ALIGN.CENTER, 0, 0)

label = lv.label(btn1)
label.set_text("LED_B")

#定时器,系统需要周期执行
def on_timer(timer):
    lv.tick_inc(5)
    lv.task_handler()

timer = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC, period=5, unit=Timer.UNIT_MS, callback=on_timer, arg=None)

while True:
    pass
