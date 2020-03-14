# Hello World 例程
# 欢迎使用OpenMV IDE! 点击左下方绿色按钮运行程序。

import sensor, image, time

sensor.reset()                    #复位和初始化摄像头设备
sensor.set_pixformat(sensor.RGB565) # 设置像素格式为彩色RGB565 (或灰色)
sensor.set_framesize(sensor.QVGA)   # 设置帧大小为 QVGA (320x240)
sensor.skip_frames(time = 2000)     # 等待设置生效
clock = time.clock()                # 创建一个时钟来追踪FPS（每秒拍摄帧数）

while(True):
    clock.tick()                    # 更新 FPS 时钟.
    img = sensor.snapshot()         # 拍摄一个图片并保存
    print(clock.fps())         # 注意: 当OpenMV连接到IDE时候，运行速度减半，因此当断开IDE时FPS会提升。
