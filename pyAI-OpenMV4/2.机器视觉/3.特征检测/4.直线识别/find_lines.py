# 直线识别例程
#
# 该例程演示了如何在图像中找出直线，每个被找出的直线都会返回一个对象，包括直线的线路定位。
#
# 直线识别使用了霍夫转换算法:
# 参考链接：http://en.wikipedia.org/wiki/Hough_transform
# 你可以从上面链接更深入了解  `theta` 和 `rho` 参数的概念.
#
# 使用 find_lines() 找直线 (速度比较慢).
# 使用 find_line_segments() 找线段 (速度比较快).
#
#翻译：01Studio


enable_lens_corr = False # 打开以获得更直的线段

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

# 所有直线都可以通过 `theta()` 函数来获取跟水平线的夹角。
# 你也可以通过滤波算法来平滑角度.

min_degree = 0
max_degree = 179

# 所有直线对象都可以通过 `x1()`, `y1()`, `x2()`, and `y2()` 方法获取其端点，当然
# 也可以使用`line()` 获取上面4个值以用于 `draw_line()`画线.

while(True):

    clock.tick()
    img = sensor.snapshot()
    if enable_lens_corr: img.lens_corr(1.8) # for 2.8mm lens...

    # `threshold` 参数控制找到直线的数量，数值的提升会降低识别直线的总数。

    # `threshold` 参数控制找到圆的数量，数值的提升会降低识别圆形的总数。

    # `theta_margin` and `rho_margin` 控制直线是否合并。若少于预设值则合并

    for l in img.find_lines(threshold = 1000, theta_margin = 25, rho_margin = 25):
        if (min_degree <= l.theta()) and (l.theta() <= max_degree): #直线角度在0至180度范围内
            img.draw_line(l.line(), color = (255, 0, 0))
            print(l)

    print("FPS %f" % clock.fps())

# 关于 rho 出现负数:
#
# [theta+0:-rho] 元组与 [theta+180:+rho]相同.
