# 线段识别例程
#
# 该例程演示了如何在图像中找出线段，每个被找出的线段都会返回一个对象，包括线段的线路定位。

# 使用 find_lines() 找直线 (速度比较慢).
# 使用 find_line_segments() 找线段 (速度比较快).
#
#翻译：01Studio

enable_lens_corr = False # 打开以获得更直的线段

import sensor, image, time

#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale 灰度图像处理速度更快
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# 所有线段对象都可以通过 `x1()`, `y1()`, `x2()`, and `y2()` 方法获取其端点，当然
# 也可以使用`line()` 获取上面4个值以用于 `draw_line()`画线.

while(True):

    clock.tick()

    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    # `merge_distance` 控制相近的线段是否合并.  数值 0 (默认值)表示不合并。数值为1时候
    # 表示相近1像素的线段被合并。因此你可以通过改变这个参数来控制检测到线段的数量。

    # `max_theta_diff` 控制相差一定角度的线段合并，默认是15度，表示15度内的线段都会合并

    for l in img.find_line_segments(merge_distance = 0, max_theta_diff = 5):
        img.draw_line(l.line(), color = (255, 0, 0))
        #print(l)

    print("FPS %f" % clock.fps())
