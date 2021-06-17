# 垂直反转 - 水平镜像 - 转置
#
# 这个示例展示了如何将图像实现 垂直反转 - 水平镜像 - 转置
# 具体参数如下：3个参数一共有8中情况,以下罗列了4种无镜像情况
#
# vflip=False, hmirror=False, transpose=False -> 0 degree rotation
# vflip=True,  hmirror=False, transpose=True  -> 90 degree rotation
# vflip=True,  hmirror=True,  transpose=False -> 180 degree rotation
# vflip=False, hmirror=True,  transpose=True  -> 270 degree rotation
#
#翻译和注释：01Studio

import sensor, image, time, pyb

#摄像头初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
clock = time.clock()

mills = pyb.millis()
counter = 0

while(True):
    clock.tick()


    img = sensor.snapshot().replace(vflip=(counter//2)%2,
                                    hmirror=(counter//4)%2,
                                    transpose=(counter//8)%2)

   # 也可以手动修改参数观察图像变化情况。
   #img = sensor.snapshot().replace(vflip=False,
   #                                   hmirror=False,
   #                                    transpose=False)

    if (pyb.millis() > (mills + 1000)):
        mills = pyb.millis()
        counter += 1

    print(clock.fps())
