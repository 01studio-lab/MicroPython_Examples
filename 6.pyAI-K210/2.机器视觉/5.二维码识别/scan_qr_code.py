#实验名称：二维码识别
#版本：v1.0
#日期：2019-12-23
#翻译和注释：01Studio

import sensor,lcd,time

#摄像头模块初始化
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)     #后置模式
sensor.skip_frames(30)

#lcd初始化
lcd.init()

clock = time.clock()

while True:

    clock.tick()

    img = sensor.snapshot()
    res = img.find_qrcodes() #寻找二维码

    if len(res) > 0: #在图片和终端显示二维码信息
        img.draw_rectangle(res[0].rect())
        img.draw_string(2,2, res[0].payload(), color=(0,128,0), scale=2)
        print(res[0].payload())

    lcd.display(img)
    print(clock.fps())
