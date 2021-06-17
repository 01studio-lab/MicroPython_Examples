# 快速线性回归例程
#
#本例程展示了如何在OpenMV Cam上使用get_regression()方法
#得到ROI的线性回归。使用此方法可以轻松构建
#一种机器人，它可以跟踪所有方向相同的线，在适当的线上使用find_blobs() ，以获得更好的过滤选项和控制。
#
#这方法被称为快速线性回归，因为我们使用了最小二乘
#方法来拟合直线。但是，这种方法并非适用于任何图像
#有很多异常点会破坏线的识别。
#
#翻译：01Studio

THRESHOLD = (0, 100)  # 黑白图像的灰度阈值
BINARY_VISIBLE = True # 使用二值化图像你可以看到什么是线性回归。
                      # 这可能降低 FPS（每秒帧数）.

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):

    clock.tick()

    #image.binary([THRESHOLD])将灰度值在THRESHOLD范围变成了白色
    img = sensor.snapshot().binary([THRESHOLD]) if BINARY_VISIBLE else sensor.snapshot()

    # 返回一个类似 find_lines() 和find_line_segments()的对象.
    # 有以下函数使用方法： x1(), y1(), x2(), y2(), length(),
    # theta() (rotation in degrees), rho(), and magnitude().
    #
    # magnitude() 代表线性回归的指令，其值为(0, INF]。
    # 0表示一个圆，INF数值越大，表示线性拟合的效果越好。

    line = img.get_regression([(255,255) if BINARY_VISIBLE else THRESHOLD])

    if (line): img.draw_line(line.line(), color = 127)
    print("FPS %f, mag = %s" % (clock.fps(), str(line.magnitude()) if (line) else "N/A"))

# 有关 rho 负值:
#
#  [theta+0:-rho] 元组和  [theta+180:+rho]是一样的.
