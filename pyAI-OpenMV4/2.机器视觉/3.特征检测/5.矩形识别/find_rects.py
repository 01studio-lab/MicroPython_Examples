# 矩形识别例程
#
#这个例子演示了如何使用 quad 阈值在图像中找到矩形
#四元阈值检测算法检测矩形使用鲁棒的方式，是远远好于霍夫
#转换的方法。例如，它仍然可以检测矩形，即使镜头
#扭曲会使这些矩形看起来弯曲。所以圆角矩形是没有问题的!
#(鉴于此，代码也将检测小半径圆)…
#
#翻译：01Studio

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.RGB565) # grayscale is faster (160x120 max on OpenMV-M7)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()

    # `threshold` 需要设置一个比价大的值来过滤掉噪声。
    #这样在图像中检测到边缘亮度较低的矩形。矩形
    #边缘量级越大，对比越强…

    for r in img.find_rects(threshold = 10000):
        img.draw_rectangle(r.rect(), color = (255, 0, 0)) #画矩形显示
        for p in r.corners(): img.draw_circle(p[0], p[1], 5, color = (0, 255, 0))#四角画小圆形
        print(r)

    print("FPS %f" % clock.fps())
