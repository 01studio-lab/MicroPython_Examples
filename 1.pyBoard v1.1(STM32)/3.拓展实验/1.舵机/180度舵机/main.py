'''
实验名称：舵机(Servo)-180°
版本：v1.0
日期：2019.7
作者：01Studio
说明：通过USER按键让让舵机旋转不同角度。
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

#定义5组角度：-90、-45、0、45、90
angle=[-90,-45,0,45,90]

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
oled.text('Servo-180', 0, 15)  # 次行显示实验名称
oled.text(str(angle[i]) , 0, 35)  # 显示当前角度
oled.text('Pls Press USER', 0, 55)  #提示按按键
oled.show()

#X1指定角度,启动时i=0，默认-90°
s1.angle(angle[i])

while True:

    if key_node==1: #按键被按下
        i = i+1
        if i == 5:
            i = 0
        key_node = 0 #清空按键标志位

        #X1指定角度
        s1.angle(angle[i])

        #显示当前频率
        oled.fill(0)  # 清屏显示黑色背景
        oled.text('01Studio', 0, 0)  # 首行显示01Studio
        oled.text('Servo-180', 0, 15)  # 次行显示实验名称
        oled.text(str(angle[i]) , 0, 35)  # 显示当前角度
        oled.text('Pls Press USER', 0, 55)  #提示按按键
        oled.show()
