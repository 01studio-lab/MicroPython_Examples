# TCP客户端（Socket通信） 实验
#
# 通过WiFi模块编程实现K210的Socket通信，数据收发.
#
#作者：01Studio

import network,usocket,time
from machine import UART,Timer
from Maix import GPIO
from fpioa_manager import fm

SSID='01Studio' # WiFi 账号
KEY='88888888'  # WiFi 密码

#socket数据接收中断标志位
socket_node = 0

###### WiFi模块初始化 ######
#使能引脚初始化
fm.register(8, fm.fpioa.GPIOHS0, force=True)
wifi_en=GPIO(GPIO.GPIOHS0, GPIO.OUT)

#串口初始化
fm.register(7, fm.fpioa.UART2_TX, force=True)
fm.register(6, fm.fpioa.UART2_RX, force=True)
uart = UART(UART.UART2,115200,timeout=1000,read_buf_len=4096)

#WiFi使能函数
def wifi_enable(en):
    global wifi_en
    wifi_en.value(en)

#WiFi对象初始化，波特率需要修改
def wifi_init():
    global uart
    wifi_enable(0)
    time.sleep_ms(200)
    wifi_enable(1)
    time.sleep(2)
    uart = UART(UART.UART2,115200,timeout=1000, read_buf_len=4096)
    tmp = uart.read()
    uart.write("AT+UART_CUR=921600,8,1,0,0\r\n")
    print(uart.read())
    uart = UART(UART.UART2,921600,timeout=1000, read_buf_len=10240) #实测模块波特率太低或者缓存长度太短会导致数据丢失。
    uart.write("AT\r\n")
    tmp = uart.read()
    print(tmp)
    if not tmp.endswith("OK\r\n"):
        print("reset fail")
        return None
    try:
        nic = network.ESP8285(uart)
    except Exception:
        return None
    return nic

############################
#########  主程序  ##########
############################

#构建WiFi对象并使能
wlan = wifi_init()

#正在连接印提示
print("Trying to connect... (may take a while)...")

#连接网络
wlan.connect(SSID,KEY)

#打印IP相关信息
print(wlan.ifconfig())

#创建socket连接，连接成功后发送“Hello 01Studio！”给服务器。
client=usocket.socket()

addr=('192.168.1.111',10000) #服务器IP和端口
client.connect(addr)
client.send('Hello 01Studio!')
client.settimeout(0.1)

#定时器回调函数
def fun(tim):
    global socket_node
    socket_node = 1 #改变socket标志位

#定时器0初始化，周期100ms
tim = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PERIODIC,
            period=100, callback=fun)

while True:
    if socket_node:

        try:
            data = client.recv(256)
        except OSError:
            data = None

        if data:
            print("rcv:", len(data),data)

        socket_node = 0
    else: pass
