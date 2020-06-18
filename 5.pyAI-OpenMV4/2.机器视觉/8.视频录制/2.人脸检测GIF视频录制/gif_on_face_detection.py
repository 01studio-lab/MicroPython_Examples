# 人脸检测GIF视频录制例程
#
# 提示: 此程序需要使用SD卡.
#
# 你可以使用OpenMV来录制gif文件. 可以选择性录制RGB565或灰度图像.
# 使用像GIMP这样的照片编辑软件来压缩和优化Gif，然后再上传到web。
#
# 这个例程是实现当检测到人脸时候自动录制GIF视频
#
#翻译和注释：01Studio

import sensor, image, time, gif, pyb

RED_LED_PIN = 1
BLUE_LED_PIN = 3

#摄像头初始化
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.
sensor.set_framesize(sensor.QQVGA) # or sensor.HQVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.

# 人脸检测是通过在图像上使用Haar Cascade特征检测器来实现的。
# 一个 Haar Cascade 是一系列简单区域的对比检查.
# 人脸识别有25个阶段，每个阶段有几百次检测。Haar Cascades 运行很快因为是逐个阶段
# 递进检测的。 此外，OpenMV Cam使用一种称为积分图像的数据结构来在恒定时间内快速
#执行每个区域的对比度检查(特征检测需要用灰度图像的原因是因为图像积分需要更多空间)。

face_cascade = image.HaarCascade("frontalface", stages=25)

while(True):

    pyb.LED(RED_LED_PIN).on()
    print("About to start detecting faces...")
    sensor.skip_frames(time = 2000) # Give the user time to get ready.

    pyb.LED(RED_LED_PIN).off()
    print("Now detecting faces!")
    pyb.LED(BLUE_LED_PIN).on()

    diff = 10 # 重复检测10帧，确认人脸.
    while(diff):
        img = sensor.snapshot()
        # threshold和scale_factor两个参数控制着识别的效率和准确性.
        faces = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5)

        if faces:
            diff -= 1
            for r in faces:
                img.draw_rectangle(r)

    #创建GIF对象，pyb.rng()随机返回一个30位的二进制数值，最终文件名转换成10进制。
    g = gif.Gif("example-%d.gif" % pyb.rng(), loop=True)

    clock = time.clock() # Tracks FPS.
    print("You're on camera!")
    for i in range(100):
        clock.tick()
        # clock.avg() 返回每帧平均运行时间，单位ms - gif 的延时是厘秒级别（百分之一秒）
        g.add_frame(sensor.snapshot(), delay=int(clock.avg()/10))
        print(clock.fps())

    g.close()
    pyb.LED(BLUE_LED_PIN).off()
    print("Restarting...")
