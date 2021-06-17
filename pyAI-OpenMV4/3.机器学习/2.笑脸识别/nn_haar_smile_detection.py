# 笑脸识别示例（ Haar Cascade + CNN 模型）.
#
#翻译和注释：01Studio

import sensor, time, image, os, nn

#设置摄像头
sensor.reset()                          # Reset and initialize the sensor.
sensor.set_contrast(2)
sensor.set_pixformat(sensor.RGB565)     # Set pixel format to RGB565
sensor.set_framesize(sensor.QVGA)       # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)
sensor.set_auto_gain(False)

# 加载笑脸识别神经网络模型
net = nn.load('/smile.network')

# 加载人脸识别模型 Haar Cascade
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

# FPS clock
clock = time.clock()
while (True):
    clock.tick()

    # Capture snapshot
    img = sensor.snapshot()

    # 找出图像中的人脸.
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

    # 识别笑脸
    for r in objects:

        # 重新构建识别的位置，缩小识别区域至人脸位置
        r = [r[0]+10, r[1]+25, int(r[2]*0.70), int(r[2]*0.70)]
        img.draw_rectangle(r)
        out = net.forward(img, roi=r, softmax=True)
        img.draw_string(r[0], r[1], ':)' if (out[0] > 0.8) else ':(', color=(255), scale=2)

    print(clock.fps())
