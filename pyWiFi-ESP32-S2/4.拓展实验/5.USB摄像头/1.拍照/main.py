'''
实验名称：拍照并保存
版本：v1.0
日期：2021.8
作者：01Studio
说明：编程实现录拍摄图片并保存。
'''


from machine import Pin
import esp_usb,time

KEY=Pin(0,Pin.IN,Pin.PULL_UP) #构建KEY对象

#摄像头初始化,默认帧大小 QVGA 320X240
cam = esp_usb.CAM(framesize = esp_usb.CAM.QVGA)
cam.display() #LCD显示

num=0 #用于命名图片
cam_flag = 0 #拍照标志位

##############################
#      USR按键  拍照并保存
##############################
def fun(KEY):
    global cam_flag
    cam_flag = 1

#中断初始化
KEY.irq(fun,Pin.IRQ_FALLING) #定义中断，下降沿触发

while True:

    #收到拍照命令
    if cam_flag == 1:

        #拍照并保存图片
        cam.snapshot("/"+str(num)+".jpg")

        num=num+1  #照片名称
        cam_flag=0 #清空标志位
