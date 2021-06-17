'''
实验名称：thread（多线程）
版本： v1.0
日期： 2021.5
翻译和注释： 01Studio
说明：通过编程实现多线程。
'''

import _thread #导入线程模块
import time

#线程函数
def func(name):
    while True:
        print("thread {}".format(name))
        time.sleep(1)

_thread.start_new_thread(func,("1",)) #开启线程1,参数必须是元组
_thread.start_new_thread(func,("2",)) #开启线程2，参数必须是元组

while True:
    pass

