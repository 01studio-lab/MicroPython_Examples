# GIF视频录制示例
#
# 提示: 你需要插入SD卡来运行此程序.
#
# 你可以使用OpenMV来录制gif文件. 可以选择性录制RGB565或灰度图像.
# 使用像GIMP这样的照片编辑软件来压缩和优化Gif，然后再上传到web。
#
#翻译和注释：01Studio

import sensor, image, time, gif, pyb

RED_LED_PIN = 1
BLUE_LED_PIN = 3

#摄像头初始化
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # or sensor.GRAYSCALE
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock() # Tracks FPS.

pyb.LED(RED_LED_PIN).on()
sensor.skip_frames(time = 2000) # Give the user time to get ready.

pyb.LED(RED_LED_PIN).off()
pyb.LED(BLUE_LED_PIN).on()

#创建GIF对象
g = gif.Gif("example.gif", loop=True)

print("You're on camera!")
for i in range(100):
    clock.tick()
    # clock.avg() 返回每帧平均运行时间，单位ms - gif 的延时是厘秒级别（百分之一秒）
    g.add_frame(sensor.snapshot(), delay=int(clock.avg()/10))
    print(clock.fps())

g.close()
pyb.LED(BLUE_LED_PIN).off()
print("Done! Reset the camera to see the saved recording.")
