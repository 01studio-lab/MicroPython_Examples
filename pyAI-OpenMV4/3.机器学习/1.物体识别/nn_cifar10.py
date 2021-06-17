# CIFAR10 物体识别示例
#
#翻译和注释：01Studio

import sensor, image, time, os, nn

#摄像头初始化
sensor.reset()                         # Reset and initialize the sensor.
sensor.set_contrast(3)
sensor.set_pixformat(sensor.RGB565)    # Set pixel format to RGB565
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((128, 128))       # Set 128x128 window.
sensor.skip_frames(time=1000)
sensor.set_auto_gain(False)
sensor.set_auto_exposure(False)

# 加载 cifar10 神经网络
net = nn.load('/cifar10.network')

# 更快、更小和计算量少
#net = nn.load('/cifar10_fast.network')

#10种物体标签：“飞机”、“汽车”、“鸟”、“猫”、“鹿”、“狗”、“青蛙”,“马”,“船”,“卡车”
labels = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

clock = time.clock()                # Create a clock object to track the FPS.
while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.

    #在当前图像运行神经网络，返回浮点值列表。列表共10个值，范围：0-1
    out = net.forward(img)

    #挑选列表中最大值
    max_idx = out.index(max(out))

    #将列表值乘以100，方便计算，范围变成：0-100
    score = int(out[max_idx]*100)

    #70分以上才认为识别成功
    if (score < 70):
        score_str = "??:??%"
    else:
        score_str = "%s:%d%% "%(labels[max_idx], score)

    #图像显示字符提示
    img.draw_string(0, 0, score_str, color=(255, 0, 0))

    print(clock.fps())             # Note: OpenMV Cam runs about half as fast when connected
                                   # to the IDE. The FPS should increase once disconnected.
