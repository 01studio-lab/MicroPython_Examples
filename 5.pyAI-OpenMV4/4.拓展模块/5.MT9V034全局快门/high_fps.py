# 高FPS(每秒帧率)例程
#
#这个例程展示了全局快门的高帧率测试。你可以通过改变图像像素和曝光时间来调整帧率。
#
# 图像大小从VGA到QVGA，FPS提升2倍，从QVGA到QQVGA，FPS再提升2倍。
#
# 除此之前你也可以降低曝光时间来提供FPS，但这样拍摄出来的图像会非常暗。因此你需要额外补充光源。
#
#翻译和注释：01Studio

import sensor, image, time

#摄像头初始化
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to GRAYSCALE
sensor.set_framesize(sensor.QQVGA)  # 可以测试VGA/QVGA/QQVG 对比FPS效果
sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

sensor.set_auto_exposure(True, exposure_us=5000) # 曝光时间，使用小的值提高速度。

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    print(clock.fps())              # 使用IDE运行会降低FPS。

