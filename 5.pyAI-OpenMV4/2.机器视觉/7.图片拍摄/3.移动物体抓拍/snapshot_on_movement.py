# 移动物体抓拍示例
#
# 提示: 本实验需要插入SD卡.
#
# 本示例是通过帧差异来检测移动物体。检测到移动物体后拍摄图片并保存。
#
#翻译和注释：01Studio

import sensor, image, pyb, os

RED_LED_PIN = 1
BLUE_LED_PIN = 3

#摄像头初始化
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QVGA) # or sensor.QQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_auto_whitebal(False) # Turn off white balance.

if not "temp" in os.listdir(): os.mkdir("temp") # 建立temp文件夹

while(True):

    pyb.LED(RED_LED_PIN).on()
    print("About to save background image...")
    sensor.skip_frames(time = 2000) # 给一定时间用户做测试准备.

    pyb.LED(RED_LED_PIN).off()
    sensor.snapshot().save("temp/bg.bmp")
    print("Saved background image - Now detecting motion!")
    pyb.LED(BLUE_LED_PIN).on()

    diff = 10 # 连续测试10帧，减少误判.

    while(diff):
        img = sensor.snapshot()
        img.difference("temp/bg.bmp") #和开始拍摄图片对比，不变时界面全黑色，返回图像对象。
        stats = img.statistics()
        # 下面Stats[5] 返回RGB5656 LAB 中L的最大值(0-255) (int)，大于20判定为图片变化，即物体移动.
        if (stats[5] > 20):
            diff -= 1

    pyb.LED(BLUE_LED_PIN).off()
    print("Movement detected! Saving image...")
    sensor.snapshot().save("temp/snapshot-%d.jpg" % pyb.rng()) # 保存图片.
