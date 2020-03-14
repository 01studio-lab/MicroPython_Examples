
'''
实验名称：按键
版本：v2.0
日期：2019.4
作者：01Studio
'''

from pyb import LED,Switch

sw = Switch()     #定义按键对象名字为sw
sw.callback(lambda:LED(4).toggle())   #当按键被按下时，LED(4)状态反转
