# 移动物体 GIF 视频录制例程
#
# 提示: 你需要插入SD卡来运行此程序.
#
# 你可以使用OpenMV来录制gif文件. 可以选择性录制RGB565或灰度图像.
# 使用像GIMP这样的照片编辑软件来压缩和优化Gif，然后再上传到web。
#
# 本示例是通过帧差异来检测移动物体。检测到移动物体后拍摄视频并保存。
#
#翻译和注释：01Studio

import sensor, image, time, gif, pyb, os

RED_LED_PIN = 1
BLUE_LED_PIN = 3

#摄像头初始化
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
sensor.set_auto_whitebal(False) # Turn off white balance.

if not "temp" in os.listdir(): os.mkdir("temp") # 新建一个temp文件夹存放视频

while(True):

    pyb.LED(RED_LED_PIN).on()
    print("About to save background image...")
    sensor.skip_frames(time = 2000) # Give the user time to get ready.

    pyb.LED(RED_LED_PIN).off()
    sensor.snapshot().save("temp/bg.bmp")
    print("Saved background image - Now detecting motion!")
    pyb.LED(BLUE_LED_PIN).on()

    diff = 10 # 连续测试10帧，减少误判.
    while(diff):
        img = sensor.snapshot()
        img.difference("temp/bg.bmp")
        stats = img.statistics()
        #下面Stats[5] 返回RGB5656 LAB 中L的最大值(0-255) (int)，大于20判定为图片变化，即物体移动.
        if (stats[5] > 20):
            diff -= 1

    g = gif.Gif("example-%d.gif" % pyb.rng(), loop=True)

    clock = time.clock() # Tracks FPS.
    print("You're on camera!")
    for i in range(100):
        clock.tick()
        # clock.avg() returns the milliseconds between frames - gif delay is in
        g.add_frame(sensor.snapshot(), delay=int(clock.avg()/10)) # centiseconds.
        print(clock.fps())

    g.close()
    pyb.LED(BLUE_LED_PIN).off()
    print("Restarting...")
