# Hello World 例程

# 欢迎使用 Maixpy IDE!
#
# 1. 将开发板连接到电脑；
# 2. 在工具->选择开发板下选择合适的开发板；
# 3. 点击连接并选择串口；
# 4. 连接成功后点击绿色按钮开始运行!
#
#翻译和注释：01Studio

import sensor, image, time, lcd

lcd.init(freq=15000000)             #初始化LCD
sensor.reset()                      #复位和初始化摄像头，执行sensor.run(0)停止。
#sensor.set_vflip(1)                 #将摄像头设置成后置方式（所见即所得）


sensor.set_pixformat(sensor.RGB565) # 设置像素格式为彩色 RGB565 (或灰色)
sensor.set_framesize(sensor.QVGA)   # 设置帧大小为 QVGA (320x240)
sensor.skip_frames(time = 2000)     # 等待设置生效.
clock = time.clock()                # 创建一个时钟来追踪 FPS（每秒拍摄帧数）

while(True):
    clock.tick()                    # 更新 FPS 时钟.
    img = sensor.snapshot()         # 拍摄一个图片并保存.
    lcd.display(img)                # 在LCD上显示
    print(clock.fps())              # 注意: 当 K210 连接到 IDE 时候，运行速度减
                                    #半，因此当断开 IDE 时 FPS 会提升。
