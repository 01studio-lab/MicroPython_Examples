# 找圆形例程
#
# 这个例程使用Hough算法（霍夫变换）
# 参考链接： https://en.wikipedia.org/wiki/Circle_Hough_Transform
#
# 需要注意的是该例程只适用于识别在图像内部完整的圆形，超出图像或者识别区域（roi）的无效。
#
#翻译：01Studio

import sensor, image, time

#摄像头模块初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # 使用grayscale灰度图像处理速度会更快
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):

    clock.tick()

    #lens_corr为了去除畸变，1.8是默认参数，可以根据自己实际情况调整
    img = sensor.snapshot().lens_corr(1.8)

    # 圆形类有4个参数值： 圆心(x, y), r (半径)和magnitude（量级）；
    # 量级越大说明识别到的圆可信度越高。

    # `threshold` 参数控制找到圆的数量，数值的提升会降低识别圆形的总数。

    # `x_margin`, `y_margin`, and `r_margin`控制检测到接近圆的合并调节.

    # r_min, r_max, and r_step 用于指定测试圆的半径范围。

    for c in img.find_circles(threshold = 2000, x_margin = 10, y_margin = 10, r_margin = 10,
            r_min = 2, r_max = 100, r_step = 2):

        #画红色圆做指示
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))
        print(c)

    print("FPS %f" % clock.fps()) #打印FPS（每秒采集帧数）
