# 使用Canny算法做边缘检测:
#
# 这个例子演示了Canny边缘检测器.
#
#翻译：01Studio

import sensor, image, time

#初始化摄像头
sensor.reset() # 初始化摄像头模块.
sensor.set_pixformat(sensor.GRAYSCALE) # 或者使用 sensor.RGB565 彩色
sensor.set_framesize(sensor.QQVGA) # 或者使用 sensor.QVGA (or others)
sensor.skip_frames(time = 2000) #延时让摄像头文稳定.
sensor.set_gainceiling(8) #设置增益，这是官方推荐的参数

clock = time.clock() # Tracks FPS.

while(True):

    clock.tick() # 用于计算FPS（每秒帧数）.
    img = sensor.snapshot() # 拍摄并返回图像.

    #使用 Canny 边缘检测器
    img.find_edges(image.EDGE_CANNY, threshold=(50, 80))

    # 也可以使用简单快速边缘检测，效果一般，配置如下
    #img.find_edges(image.EDGE_SIMPLE, threshold=(100, 255))

    print(clock.fps()) #显示FPS（每秒帧数）
