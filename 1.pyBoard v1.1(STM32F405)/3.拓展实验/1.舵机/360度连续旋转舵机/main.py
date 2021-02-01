'''
实验名称：舵机(Servo)-360°连续旋转
版本：v1.0
日期：2019.7
作者：01Studio
说明：通过USER按键让舵机实现不同速度旋转。
'''

#导入相关模块
from pyb import Servo,Switch
from machine import Pin,I2C
from ssd1306 import SSD1306_I2C

#初始化相关模块
i2c = I2C(sda=Pin("Y8"), scl=Pin("Y6"))
oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)

sw = Switch()     #定义按键对象名字为sw
s1 = Servo(1)     #构建舵机对象s1，输出引脚为X1

#定义5组速度值
speed=[-100,-50,0,50,100]

key_node = 0  #按键标志位
i = 0         #用于选择角度

##############################################
#  按键和其回调函数
##############################################
def key():
    global key_node
    key_node = 1

sw.callback(key)  #当按键被按下时，执行函数key()

##############################################
#  OLED初始显示
##############################################
oled.fill(0)  # 清屏显示黑色背景
oled.text('01Studio', 0, 0)  # 首行显示01Studio
oled.text('Servo-360', 0, 15)  # 次行显示实验名称
oled.text(str(speed[i]) , 0, 35)  # 显示当前速度值
oled.text('Pls Press USER', 0, 55)  #提示按按键
oled.show()

#X1指定角度,启动时i=0，默认-90°
s1.speed(speed[i])

while True:

    if key_node==1: #按键被按下
        i = i+1
        if i == 5:
            i = 0
        key_node = 0 #清空按键标志位

        #X1指定角度
        s1.speed(speed[i])

        #显示当前频率
        oled.fill(0)  # 清屏显示黑色背景
        oled.text('01Studio', 0, 0)  # 首行显示01Studio
        oled.text('Servo-360', 0, 15)  # 次行显示实验名称
        oled.text(str(speed[i]) , 0, 35)  # 显示当前速度值
        oled.text('Pls Press USER', 0, 55)  #提示按按键
        oled.show()
