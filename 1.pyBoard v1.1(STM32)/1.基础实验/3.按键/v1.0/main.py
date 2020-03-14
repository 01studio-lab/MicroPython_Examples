'''
实验名称：按键
版本：v1.0
日期：2019.4
作者：01Studio
'''

from pyb import LED,Switch

def fun1():
    LED(4).toggle()

sw = Switch()     #定义按键对象名字为sw
sw.callback(fun1) #当按键被按下时，执行函数fun1(),即LED(4)状态反转
