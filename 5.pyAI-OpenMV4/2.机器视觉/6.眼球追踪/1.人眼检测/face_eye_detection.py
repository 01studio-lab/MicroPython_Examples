# 人眼检测例程
#
# 这个程序是先利用人脸检测确定人的脸位置，然后在检测眼球位置。
# 如果你想检测瞳孔，请参考 iris_detection 例程.
#
#翻译和注释：01Studio

import sensor, time, image

# Reset sensor
sensor.reset()

# Sensor settings
sensor.set_contrast(1)
sensor.set_gainceiling(16)
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)

# 加载 Haar Cascade 模型
# 默认使用全部stages,提高识别的准确率.
face_cascade = image.HaarCascade("frontalface", stages=25) #定义人脸模型
eyes_cascade = image.HaarCascade("eye", stages=24) #定义眼球模型
print(face_cascade, eyes_cascade)

# FPS clock
clock = time.clock()

while (True):
    clock.tick()

    # Capture snapshot
    img = sensor.snapshot()

    # 人脸检测
    objects = img.find_features(face_cascade, threshold=0.5, scale_factor=1.5)

    # 画出人脸方框
    for face in objects:
        img.draw_rectangle(face)
        # 在人脸中寻找眼球.
        # 提示:使用一个较大的 threshold 值 (识别更多) 和 较小的 scale值 (寻找较小区域的对象)
        eyes = img.find_features(eyes_cascade, threshold=0.5, scale_factor=1.2, roi=face)
        for e in eyes:
            img.draw_rectangle(e)

    # Print FPS.
    # Note: Actual FPS is higher, streaming the FB makes it slower.
    print(clock.fps())
