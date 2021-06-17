'''
实验名称：拍照并保存
版本：v1.0
日期：2020.12
作者：01Studio
说明：编程实现录拍摄图片并保存。
'''


from pyb import Switch
import sensor,time

#摄像头初始化
cam = sensor.OV2640()
cam.reset()
cam.set_framesize(sensor.VGA) #640*480分辨率
cam.display() #LCD显示

num=0 #用于命名图片
cam_flag = 0 #拍照标志位

##############################
#      USR按键  拍照并保存
##############################
def fun():
    global cam_flag
    cam_flag = 1

#USR按键初始化
sw = Switch()
sw.callback(fun)

while True:

    #收到拍照命令
    if cam_flag == 1:

        #拍照并保存图片
        cam.snapshot("/flash/"+str(num)+".jpg")

        num=num+1  #照片名称
        cam_flag=0 #清空标志位
