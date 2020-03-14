# 锐化滤波示例
#
# 这个例子展示了如何使用拉普拉斯滤波器来锐化图像。
#
#翻译和注释:01Studio

import sensor, image, time

#摄像头初始化
sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # or sensor.RGB565
sensor.set_framesize(sensor.QQVGA) # or sensor.QVGA (or others)
sensor.skip_frames(time = 2000) # Let new settings take affect.
clock = time.clock() # Tracks FPS.

while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot() # Take a picture and return the image.

    # 运行拉普拉斯内核.
    img.laplacian(1, sharpen=True)

    print(clock.fps()) #打印FPS
