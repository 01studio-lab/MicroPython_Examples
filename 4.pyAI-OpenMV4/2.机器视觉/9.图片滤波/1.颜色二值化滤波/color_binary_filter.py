# 颜色二值化滤波示例
#
# 这个程序展示了图像二值化滤波. 你可以自定义任何阈值来分割不同颜色的图像。
#
#翻译和注释：01Studio

import sensor, image, time

sensor.reset()
sensor.set_framesize(sensor.QVGA)
sensor.set_pixformat(sensor.RGB565)
sensor.skip_frames(time = 2000)
clock = time.clock()

# 可以使用  工具-> 机器视觉 -> 阈值编辑器 来调整阈值.
red_threshold = (0,100,   0,127,   0,127) # L A B
green_threshold = (0,100,   -128,0,   0,127) # L A B
blue_threshold = (0,100,   -128,127,   -128,0) # L A B

while(True):

    # 测试红色
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([red_threshold])
        print(clock.fps())

    '''
    # Test green threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([green_threshold])
        print(clock.fps())

    # Test blue threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([blue_threshold])
        print(clock.fps())
    '''
    # 测试非红色（invert=1）
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([red_threshold], invert = 1)
        print(clock.fps())
    '''
    # Test not green threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([green_threshold], invert = 1)
        print(clock.fps())

    # Test not blue threshold
    for i in range(100):
        clock.tick()
        img = sensor.snapshot()
        img.binary([blue_threshold], invert = 1)
        print(clock.fps())
    '''
