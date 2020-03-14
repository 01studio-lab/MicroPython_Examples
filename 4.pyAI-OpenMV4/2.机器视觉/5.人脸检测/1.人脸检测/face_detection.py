# 人脸检测例程
#
# 这个例子展示了OpenMV内置的人脸检测功能。
#
# 人脸检测是通过在图像上使用Haar Cascade特征检测器来实现的。
# 一个 Haar Cascade 是一系列简单区域的对比检查.
# 人脸识别有25个阶段，每个阶段有几百次检测。Haar Cascades 运行很快因为是逐个阶段
# 递进检测的。 此外，OpenMV Cam使用一种称为积分图像的数据结构来在恒定时间内快速
#执行每个区域的对比度检查(特征检测需要用灰度图像的原因是因为图像积分需要更多空间)。
#
#翻译和注释：01Studio

import sensor, time, image

# Reset sensor
sensor.reset()

# Sensor settings
sensor.set_contrast(1) #设置相机图像对比度为1
sensor.set_gainceiling(16) #设置相机图像增益上限为16
# HQVGA 和 GRAYSCALE 是人脸检测最佳配置.
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)

# 加载 Haar Cascade 模型
# 默认使用25个步骤，减少步骤会加快速度但会影响识别成功率.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

# FPS clock
clock = time.clock()

while (True):
    clock.tick()

    # Capture snapshot
    img = sensor.snapshot()

    # 找人脸对象.
    # threshold和scale_factor两个参数控制着识别的效率和准确性.
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

    # 画图展示对象（将人脸用矩形展示出来）
    for r in objects:
        img.draw_rectangle(r)

    # Print FPS.
    # 注意: 连接电脑会降低FPS.
    print(clock.fps())
