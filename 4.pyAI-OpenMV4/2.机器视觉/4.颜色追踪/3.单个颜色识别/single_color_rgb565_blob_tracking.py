# 单个颜色块识别例程
#
# 这个例程使用OpenMV来识别单种颜色。
#
#翻译：01Studio

import sensor, image, time, math

threshold_index = 0 # 0 红色, 1 绿色, 2 蓝色

# 颜色识别阈值 (L Min, L Max, A Min, A Max, B Min, B Max) LAB模型
# 下面的阈值元组是用来识别 红、绿、蓝三种颜色，当然你也可以调整让识别变得更好。
thresholds = [(30, 100, 15, 127, 15, 127), # 红色阈值
              (30, 100, -64, -8, -32, 32), # 绿色阈值
              (0, 30, 0, 64, -128, 0)] # 蓝色阈值

#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # 摄像头必须关闭自动增益
sensor.set_auto_whitebal(False) # 摄像头必须关闭白平衡
clock = time.clock()

# "pixel_threshold" 和 "area_threshold" 参数用于控制返回确定色块的数量。
# "merge=True" 用于合并找到的色块。

while(True):

    clock.tick()
    img = sensor.snapshot()

    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=200, merge=True):
        # blob.elongation() > 0.5 来判断颜色块不是圆形的时候.
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        # 下面这些画图展示一直会出现.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # 颜色块旋转角度只有 0-180 度.
        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
        print(int(math.degrees(blob.rotation())))
    print(clock.fps())
