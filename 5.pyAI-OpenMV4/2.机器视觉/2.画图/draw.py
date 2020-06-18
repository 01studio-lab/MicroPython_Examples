'''
实验名称：画各种图形和写字符
版本：v1.0
日期：2019.10
作者：01Studio
'''

import sensor, image, time, pyb

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # or GRAYSCALE...
sensor.set_framesize(sensor.QVGA) # or QQVGA...
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):

    clock.tick()

    img = sensor.snapshot()

    # 画线段：从x0, y0 到 x1, y1坐标的线段，颜色红色，线宽度2。
    img.draw_line(20, 20, 100, 20, color = (255, 0, 0), thickness = 2)

    #画矩形：绿色不填充。
    img.draw_rectangle(150, 20, 100, 30, color = (0, 255, 0), thickness = 2, fill = False)

    #画圆：蓝色不填充。
    img.draw_circle(60, 120, 30, color = (0, 0, 255), thickness = 2, fill = False)

    #画箭头：白色。
    img.draw_arrow(150, 120, 250, 120, color = (255, 255, 255), size = 20, thickness = 2)

    #画十字交叉。
    img.draw_cross(60, 200, color = (255, 255, 255), size = 20, thickness = 2)

    #写字符。
    img.draw_string(150, 200, "Hello 01Studio!", color = (255, 255, 255), scale = 2,
                    mono_space = False)

    print(clock.fps())
