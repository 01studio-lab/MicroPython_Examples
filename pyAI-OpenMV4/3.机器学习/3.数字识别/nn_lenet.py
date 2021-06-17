# lenet模型数字识别例程
#
#翻译和注释：01Studio
import sensor, image, time, os, nn

#摄像头初始化
sensor.reset()                         # Reset and initialize the sensor.
sensor.set_contrast(3)
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)      # Set frame size to QVGA (320x240)
sensor.set_windowing((128, 128))       # Set 128x128 window.
sensor.skip_frames(time=100)
sensor.set_auto_gain(False)
sensor.set_auto_exposure(False)

# 加载 lenet 神经网络模型
net = nn.load('/lenet.network')
labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

clock = time.clock()                # Create a clock object to track the FPS.
while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.

    #copy()表示创建一个图像副本储存在MicroPython堆中而不是帧缓冲区
    #二值化是为了方便处理，阈值可以自己设定。
    out = net.forward(img.copy().binary([(150, 255)], invert=True))
    max_idx = out.index(max(out))
    score = int(out[max_idx]*100)

    #大于70分认为识别可信
    if (score < 70):
        score_str = "??:??%"
    else:
        score_str = "%s:%d%% "%(labels[max_idx], score)
    img.draw_string(0, 0, score_str)

    print(clock.fps())             # Note: OpenMV Cam runs about half as fast when connected
                                   # to the IDE. The FPS should increase once disconnected.
