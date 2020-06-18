# 瞳孔追踪示例
#
#这个例子展示了如何找到眼睛的注视(瞳孔检测)
#图像中的眼睛。此脚本使用find_eyes函数来确定
#应该包含瞳孔的感兴趣区域的中心点。它基本上是这样做的
#找到眼睛最黑区域的中心，也就是瞳孔中心。
#
#注意:这个脚本不是先检测人脸，而是用长焦镜头。所以请将摄像头直接对准眼睛。
#
#翻译和注释：01Studio

import sensor, time, image

# Reset sensor
sensor.reset()

# Sensor settings
sensor.set_contrast(3)
sensor.set_gainceiling(16)

# Set resolution to VGA.
sensor.set_framesize(sensor.VGA)

# 裁剪图像到200x100，这提供了更多的细节和更少的数据要处理
sensor.set_windowing((220, 190, 200, 100))

sensor.set_pixformat(sensor.GRAYSCALE)

# 加载 Haar Cascade 模型
# 使用默认参数步骤
eyes_cascade = image.HaarCascade("eye", stages=24)
print(eyes_cascade)

# FPS clock
clock = time.clock()

while (True):
    clock.tick()
    # Capture snapshot
    img = sensor.snapshot()
    # 找眼睛 !
    # 提示: 使用一个较大的 threshold 值 (识别更多) 和 较小的 scale值 (寻找较小区域的对象)
    eyes = img.find_features(eyes_cascade, threshold=0.5, scale_factor=1.5)

    # 找瞳孔
    for e in eyes:
        iris = img.find_eye(e)
        print(iris)
        img.draw_rectangle(e)
        img.draw_cross(iris[0], iris[1])#瞳孔中心坐标x,y

    # Print FPS.
    # Note: Actual FPS is higher, streaming the FB makes it slower.
    print(clock.fps())
